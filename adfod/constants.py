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

from os.path import abspath, join, dirname
import configparser


# Pull info from the configuration file
config_path = abspath(join(dirname(__file__), '..', 'settings.ini'))


def load_configuration():
    cfg_ = configparser.ConfigParser()
    with open(config_path) as f:
        cfg_.read_file(f)

    return cfg_


# String constants are ALLCAPS single words with no leading or trailing flag
cfg = load_configuration()
TAB = '    '  # for consistency with terminal tab lengths
START = ' '
keybindings_ = cfg['KEYBINDINGS']
LEFT = keybindings_['LEFT']
RIGHT = keybindings_['RIGHT']
STRAIGHT = keybindings_['STRAIGHT']
UP = keybindings_['UP']
QUIT = keybindings_['QUIT']
FIGHT = keybindings_['FIGHT']
ESCAPE = keybindings_['ESCAPE']
TAKE = keybindings_['TAKE']

KEY_DESCRIPTIONS = {
    LEFT: "go left",
    RIGHT: "go right",
    STRAIGHT: "go straight",
    UP: "go up",
    QUIT: "quit",
    FIGHT: "fight",
    ESCAPE: "escape",
    START: "SPACE" if START == ' ' else START,
    TAKE: "take treasure",
}


# Integer constants end with a '_' flag
QUIT_ = 0
CONTINUE_ = 1
DIE_ = 2
IN_ROOM_ = 3
IN_CORRIDOR_ = 4
FIGHT_OR_ESCAPE_ = 5
RESTART_ = 6
TAKE_TREASURE_ = 7
KILLED_BY_TREASURE_ = 8
RESERVED_ = 666


# Media and prompts
LOGO_PATH = abspath(join(dirname(__file__), '../resources/logo.txt'))

GREETING = f"""
    Welcome to ADFOD! Hit ``{QUIT}`` at any time to exit.

Press {KEY_DESCRIPTIONS[START]} to generate a new dungeon and begin the game
"""

KILL_SCREEN = f"""
    You foolishly attempt to fight the demon and it swallows you whole.

            Press {KEY_DESCRIPTIONS[START]} to try again or {QUIT} to quit
"""

TREASURE_SCREEN = f"""
  The treasure reveals itself as yet another demon, and it swallows you whole.

        Press {KEY_DESCRIPTIONS[START]} to try again or {QUIT} to quit
"""

ESCAPE_SCREEN = "You escape the clumsy demon's grasp."

# Names and descriptions
DEMON_NAME = "demon"
TREASURE_NAME = "treasure"
ROOM_NAME = "room"
CORRIDOR_NAME = "corridor"
STAIRWAY_DESC = "downward stairway"
