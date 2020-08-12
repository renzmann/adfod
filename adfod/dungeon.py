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

__all__ = ["generate_dungeon"]

from random import random, seed, shuffle
from .objects import Location, Room, Corridor, Demon, Treasure
from typing import Union


class LateralGenerator:

    def __init__(self,
                 max_depth: int,
                 max_off_path_depth: int,
                 prob_three_paths: float,
                 prob_room: float,
                 random_seed: int):

        self.max_depth = max_depth
        self.max_off_path_depth = max_off_path_depth
        self.prob_three_paths = prob_three_paths
        self.prob_room = prob_room
        self.random_seed = random_seed

    def room_or_corridor(
            self,
            location: Location,
            depth: int,
            off_path_depth: int) -> Location:

        if bernoulli(self.prob_room, self.random_seed):
            return Room(Demon())

        return self.generate_children(location, depth, off_path_depth)

    def generate_children(
            self,
            location: Location,
            depth: int,
            off_path_depth: int) -> Location:

        if depth == self.max_depth:
            return location

        num_children = 1 + bernoulli(self.prob_three_paths, self.random_seed)
        one_above_bottom = depth >= (self.max_depth - 1)
        one_above_off_depth = off_path_depth >= (self.max_off_path_depth - 1)

        if one_above_bottom or one_above_off_depth:
            demon_rooms = [Room(Demon()) for _ in range(num_children)]
            return Corridor(demon_rooms)

        children = [
            self.room_or_corridor(location, depth + 1, off_path_depth + 1)
            for _ in range(num_children)
        ]

        return Corridor(children)


class DungeonIterator:

    def __init__(self, location: Location):
        self.location = location

    def __next__(self):
        if isinstance(self.location.content, Treasure):
            raise StopIteration()

        next_loc = next(filter(lambda x: x.on_path, self.location.content))
        self.location = next_loc
        return next_loc

    def __iter__(self):
        return self


class Dungeon:

    def __init__(self, location: Location):
        self.content = location

    def __len__(self):
        i = 0
        for _ in iter(self):
            i += 1
        return i

    def __iter__(self):
        return DungeonIterator(self.content)


def generate_dungeon(
        max_depth: int,
        max_off_path_depth: int,
        prob_three_paths: float,
        prob_room: float,
        random_seed: int = None) -> Dungeon:

    dungeon = generate_treasure_path(max_depth, prob_three_paths * max_depth)
    treasure_nodes = list(iter(dungeon))
    treasure_room = treasure_nodes.pop()
    corridor_system = Corridor(treasure_room)
    generator = LateralGenerator(
            max_depth,
            max_off_path_depth,
            prob_three_paths,
            prob_room,
            random_seed
    )

    for i, treasure_path_node in enumerate(treasure_nodes):
        lateral_system = generator.generate_children(treasure_path_node, i, 0)
        level_content = [corridor_system] + lateral_system.content

        if random_seed:
            seed(random_seed)

        shuffle(level_content)
        corridor_system = Corridor(level_content, on_path=True)

    return Dungeon(corridor_system)


def check_is_probability(p: float) -> None:
    if not ((p >= 0.0) & (p <= 1.0)):
        raise ValueError("p must be between 0.0 and 1.0")


def bernoulli(p: float, random_seed: Union[None, int]) -> int:
    """Return ``True`` with probability ``p``"""
    check_is_probability(p)
    if random_seed:
        seed(random_seed)
    return random() <= p


def generate_treasure_path(max_depth: int, treasure_value: float) -> Dungeon:
    """Treasure is always at the deepest point of the dungeon, so a preliminary
    dungeon will just consist of nested lists until hitting max_depth."""
    treasure_path = Room(Treasure(treasure_value))
    for _ in range(max_depth):
        treasure_path = Corridor(treasure_path, on_path=True)
    return Dungeon(treasure_path)
