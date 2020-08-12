#  ADFOD: A Dungeon Full of Demons!
#  Copyright (C) 2020 Robert A. Enzmann
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

__all__ = ['Screen']

import curses
from . import constants as c
from .game import Game
from typing import Union, List, Callable


def guard(string: str, width_or_length: int) -> str:
    return string[:max(width_or_length - 1, 0)]


def load_logo() -> str:
    with open(c.LOGO_PATH) as f:
        logo = "".join(line for line in f.readlines())
    return logo


def wrap_string(s: str, max_line_len: int) -> str:
    """Insert newline characters at word breaks to wrap at `max_line_len`"""

    if len(s) < max_line_len:
        return s

    remainder = s
    out_string = ''

    while remainder != '':

        sub, remainder = remainder[:max_line_len], remainder[max_line_len:]

        if remainder == '':
            out_string += sub
            break

        for i, ch in enumerate(sub[::-1]):
            if ch.isspace():
                space_index = len(sub) - i
                head, tail = sub[:space_index - 1], sub[space_index:]
                out_string += head + '\n'
                remainder = tail + remainder
                break

    return out_string


class Screen:

    def __init__(self, curses_screen):
        self.sc = curses_screen

    def guard_y(self, string: str):
        max_y, _ = self.sc.getmaxyx()
        return guard(string, max_y)

    def guard_x(self, string: str):
        _, max_x = self.sc.getmaxyx()
        return guard(string, max_x)

    def greeting(self) -> str:

        def _greeting() -> str:
            self.draw_lines(c.GREETING.splitlines())
            return self.sc.getkey()

        return self.wait(_greeting, [c.START, c.QUIT])

    def redraw(self) -> None:
        self.sc.clear()
        self.sc.refresh()

    def draw_lines(self, lines: List[str]) -> None:
        self.sc.clear()
        max_y, max_x = self.sc.getmaxyx()

        for i, line in enumerate(lines):
            if i >= max_y - 1:
                break
            self.println(guard(line, max_x), x=0, y=i)

    def print_paragraph(self, paragraph: str) -> None:
        _, max_x = self.sc.getmaxyx()

        def wrap(s):
            return wrap_string(s, max_line_len=max_x)

        # Assuming newline characters already delineate paragraphs, this `map`
        # assures we only wrap those paragraphs that are too long.
        out_string = '\n'.join(map(wrap, paragraph.splitlines()))
        self.draw_lines(out_string.splitlines())

    def screen_updater(self, screen_string: str) -> Callable:

        def _updater():
            self.print_paragraph(screen_string)
            return self.sc.getkey()

        return _updater

    def intro(self) -> str:
        logo = load_logo().splitlines()

        def draw_logo():
            self.sc.clear()
            self.draw_lines(logo)
            max_y, max_x = self.sc.getmaxyx()
            start_prompt = self.guard_x(f"{c.TAB}Press SPACE to start.")
            self.println(start_prompt, x=0, y=max_y - 1)
            return self.sc.getkey()

        return self.wait(draw_logo, c.START)

    def wait(self, update_method: Callable,
             kill_keys: Union[str, List[str]]) -> str:

        key = str(c.RESERVED_)
        while key not in kill_keys:
            y, x = self.sc.getmaxyx()
            if curses.is_term_resized(y, x):
                self.sc.clear()
                curses.resizeterm(y, x)
                self.sc.refresh()
            key = update_method()

        return key

    def println(self, string, x=None, y=None) -> None:
        """
        Print a line beginning on the start of the next line
        from wherever the cursor was last put. The (y, x) convention of curses
        is also fairly annoying, so we make it explicit with this print
        signature.
        """
        _y, _x = curses.getsyx()
        if x is None:
            x = 0
        if y is None:
            y = _y + 1
        self.sc.addstr(y, x, string)
        self.sc.refresh()

    def string_your_options(self, options: List[str]) -> str:
        menu_strings = (
            self.guard_x(f"\n{c.TAB}{c.KEY_DESCRIPTIONS[option]} ({option})")
            for option in options
        )
        return "\n\nYou can:" + "".join(menu_strings) + " \n\n"

    def look_and_react(self, gs: Game, options: List[str] = None) -> str:
        if options is None:
            options = gs.move_options
        if gs.next_play == c.DIE_:
            kill_screen = self.screen_updater(c.KILL_SCREEN)
            return self.wait(kill_screen, [c.START, c.QUIT])
        if gs.next_play == c.KILLED_BY_TREASURE_:
            kill_screen = self.screen_updater(c.TREASURE_SCREEN)
            return self.wait(kill_screen, [c.START, c.QUIT])
        else:
            level = level_string(gs)
            look_string = gs.current_level.look()
            options_list = self.string_your_options(options)
            screen_string = level + look_string + options_list
            options_screen = self.screen_updater(screen_string)
            return self.wait(options_screen, options + [c.QUIT])

    def prompt(self, gs: Game) -> str:
        self.sc.clear()
        return self.look_and_react(gs)


def level_string(gs: Game) -> str:
    if gs.current_level.is_corridor:
        level = f"You are on level {gs.current_depth}\n\n"
    else:
        level = ""
    return level
