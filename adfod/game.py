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

__all__ = ['Game']

from .dungeon import generate_dungeon
from typing import List, Union
from . import constants as c


class Game:

    exit_actions = {
        c.QUIT: c.QUIT_,
        c.START: c.RESTART_
    }

    move_actions = [c.LEFT, c.RIGHT, c.UP, c.STRAIGHT]

    def __init__(self,
                 random_seed=None,
                 max_depth=5,
                 prob_three_paths=0.5,
                 prob_room=0.75,
                 max_off_path_depth=2):

        self.random_seed = random_seed
        self.next_play = c.CONTINUE_
        self.max_depth = max_depth
        self.prob_three_paths = prob_three_paths
        self.prob_room = prob_room
        self.max_off_path_depth = max_off_path_depth
        self.dungeon = generate_dungeon(
                self.max_depth,
                self.max_off_path_depth,
                self.prob_three_paths,
                self.prob_room,
                self.random_seed
        )
        self.entrance = self.dungeon.content
        self.current_level = self.entrance
        self.current_depth = 1
        self.current_level.visited = True
        self.parent_corridors = []
        self.exit_code = None

    def go_up(self) -> None:
        if self.current_level is self.entrance:
            print("You are already at the entrance.")
        else:
            self.current_depth -= 1
            self.current_level = self.parent_corridors.pop()

    @property
    def num_options(self) -> int:
        return len(self.current_level.content)

    @property
    def move_options(self) -> List[str]:
        if self.next_play == c.TAKE_TREASURE_:
            return [c.TAKE]

        not_at_entrance = self.current_level is not self.entrance
        up_option = [c.UP] * not_at_entrance
        num_options = self.num_options

        # switch lol
        if num_options == 0:
            move_options = [c.FIGHT, c.ESCAPE]
        elif num_options == 1:
            move_options = [c.STRAIGHT] + up_option
        elif num_options == 2:
            move_options = [c.LEFT, c.RIGHT] + up_option
        elif num_options == 3:
            move_options = [c.LEFT, c.STRAIGHT, c.RIGHT] + up_option
        else:
            raise ValueError("number of move options exceeds 3")

        return move_options

    def move_sideways(self, direction: str) -> None:
        self.parent_corridors.append(self.current_level)
        content_direction = self.move_options.index(direction)
        self.current_level = self.current_level.content[content_direction]
        self.current_depth += 1
        self.current_level.visited = True

    def move_level(self, direction: str) -> None:
        """Modify game state using one of LEFT, RIGHT, UP, or STRAIGHT"""
        if direction in [c.UP, c.ESCAPE]:
            self.go_up()
        else:
            self.move_sideways(direction)

    @property
    def current_state(self) -> int:
        if self.current_level.is_room:
            return c.IN_ROOM_
        elif self.current_level.is_corridor:
            return c.IN_CORRIDOR_
        else:
            msg = f"Current level not understood: {self.current_level}"
            raise ValueError(msg)

    def handle(self, key: Union[str, int]) -> None:
        if ((key in self.exit_actions)
                or (self.next_play == c.DIE_)
                or (self.next_play == c.KILLED_BY_TREASURE_)):
            self.next_play = c.QUIT_
            self.exit_code = self.exit_actions[key]
            return
        elif key == c.TAKE:
            self.next_play = c.KILLED_BY_TREASURE_
            return
        elif key == c.FIGHT:
            self.next_play = c.DIE_
            return

        self.move_level(key)

        if self.current_state == c.IN_ROOM_:
            if self.current_level.content.is_treasure:
                self.next_play = c.TAKE_TREASURE_
            else:
                self.next_play = c.FIGHT_OR_ESCAPE_
        elif self.current_state == c.IN_CORRIDOR_:
            self.next_play = c.CONTINUE_
        else:
            raise ValueError(f"No action matching given state: key={key},"
                             f" state={self.current_state}")
