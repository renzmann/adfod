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

__all__ = ("Demon", "Treasure", "Corridor", "Room", "Location")

from typing import Union, Iterable
from .constants import (
        CORRIDOR_NAME, DEMON_NAME, TREASURE_NAME,
        STAIRWAY_DESC, ROOM_NAME
)


class Named:
    name = None

    @property
    def is_treasure(self):
        return False

    def __len__(self):
        return 0


class Demon(Named):
    """Watch out for these."""
    name = DEMON_NAME


class Treasure(Named):
    """You want to find this."""
    name = TREASURE_NAME

    def __init__(self, value=0.0):
        self.value = value

    @property
    def is_treasure(self):
        return True


class Location(Named):
    content = None
    visited = False
    on_path = False
    level = 1

    @property
    def is_room(self):
        return self.name == ROOM_NAME

    @property
    def is_corridor(self):
        return self.name == CORRIDOR_NAME

    def look(self):
        if self.is_room:
            return f"You are in {str(self).lower()}"
        else:
            return f"There is a {str(self).lower()}"


class Corridor(Location):
    """Can lead to rooms or more corridors"""

    name = "corridor"

    def __init__(self,
                 content: Union[Location, Iterable[Location]],
                 on_path: bool = False):

        cont_iter = [content] if not isinstance(content, Iterable) else content
        self.content = list(cont_iter)
        self.on_path = on_path
        self.visited = False

        if len(self.content) > 3:
            raise ValueError(f"{CORRIDOR_NAME} can't have more than 3 paths.")

    def __str__(self):
        content_size = len(self.content)
        out_string = "A corridor with "

        if content_size == 1:
            location = self.content[0]
            nother = "nother" * location.is_corridor * location.visited
            out_string += f"a{nother} {description(location)} straight ahead."
            return out_string
        elif content_size == 2:
            left, right = self.content
            out_string += f"a {description(left)} to the left "
        else:
            left, middle, right = self.content
            out_string += f"a {description(left)} to the left, "
            out_string += f"a {description(middle)} straight ahead, "

        nother = "nother" * right.is_corridor * right.visited
        out_string += f"and a{nother} {description(right)} to the right."

        return out_string


class Room(Location):
    """Contains either the treasure or a demon."""

    name = "room"

    def __init__(self, content: Union[Demon, Treasure]):
        self.content = content
        self.visited = False

    @property
    def on_path(self):
        return isinstance(self.content, Treasure)

    def __str__(self):
        if self.content.name == DEMON_NAME:
            return f"A room with a {DEMON_NAME}."
        return f"A room full of {TREASURE_NAME}."


def description(location: Location):
    return location.name if location.visited else STAIRWAY_DESC
