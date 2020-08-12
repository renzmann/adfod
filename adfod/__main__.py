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

import curses
from .game import Game
from .screen import Screen
from .constants import QUIT, QUIT_, CONTINUE_, load_configuration


def build_game_from_config() -> Game:
    cfg = load_configuration()
    opts = cfg['DUNGEON']
    game = Game(
        max_depth=int(opts['MAX_DEPTH']),
        prob_three_paths=float(opts['PROB_THREE_PATHS']),
        prob_room=float(opts['PROB_ROOM']),
        max_off_path_depth=int(opts['MAX_OFF_PATH_DEPTH']))
    return game


def game_loop(sc: Screen) -> int:
    key = sc.greeting()
    if key == QUIT:
        return QUIT_

    game = build_game_from_config()

    while game.next_play:
        keypress = sc.prompt(game)
        game.handle(keypress)

    return game.exit_code


def main(screen):
    sc = Screen(screen)
    sc.redraw()
    sc.intro()
    sc.redraw()
    exit_code = CONTINUE_
    while exit_code:
        exit_code = game_loop(sc)


def run():
    curses.wrapper(main)


if __name__ == '__main__':
    curses.wrapper(main)
