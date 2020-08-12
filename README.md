# ADFOD: A Dungeon Full of Demons!

Welcome to my small personal project for learning python's built-in
[`curses`](https://docs.python.org/3/library/curses.html) library. This
game will take you on an adventure through a procedurally generated
dungeon full of demons, who you will have to fight or evade until you
discover the treasure. To play the game, all you need is python >= 3.6.


## How to play

We assume you are already familiar with terminals, command prompts, and how to 
run python from
them. Before playing adfod, make sure you have python >= 3.6 installed, and the
`python` or `python3` commands are available to you from your prompt. I have
personally only tested python versions 3.6, 3.7, and 3.8, although it may work
on earlier python 3 versions. If you try to use python 2, it will almost
certainly break.


### Running with python

#### Windows
Windows requires a special version of `curses`, so you need to get 
`windows-curses` from the python package index before you can play.

```
> pip install windows-curses
> python -m adfod
```

___
**Note**
Microsoft has started redirecting the `python` and `python3` commands to the
Microsoft store for whatever reason. You must be sure that an installation of
python 3 is available from the command prompt. 
___


#### Linux/osX
`curses` works out-of-the-box on \*nix systems, so just run
`python3 -m adfod`.


## What this game's about

This "game" has very little meat on its bones from a gameplay perspective.
Instead, this project is primarily meant to demonstrate how to create
a fully functional terminal user interface. That is, it must be capable of
accepting user input, displaying the game state, and keeping text within
the boundaries of the terminal window as we resize it. Of course, we do
still need to have *some* content to play with, and so I've used a very
simply designed game:

1. You play an adventurer set to discover the treasure at the bottom of
   a dungeon full of demons. Each playthrough is a new, random dungeon.
2. The dungeon consists of corridors and rooms. A room may contain either
   a demon or the treasure. Corridors will lead either to other corridors
   or to rooms.
3. Each time you advance from one corridor to the next, you move deeper
   into the dungeon.
4. When facing a demon, you can either try to fight, or try to flee.

This just leaves the game's implementation, which this repository answers
with python's very easy to use wrapper around `curses`.

**Why use a curses interface instead of a GUI?**. Simple: text adventure
games are awesome. The [ncurses](https://en.wikipedia.org/wiki/Ncurses)
library provides a high level interface to the terminal that is readily
ported across platforms, and by keeping our program's palette limited to
text, we have to paint a more vivid picture using words. The player's
imagination will fill in the details that we can't.


## How do I change the game settings?

The `settings.ini` file has all the options you can configure about the game.
This includes parameters that are passed to the dungeon creation algorithm, so
you can make it as deep or wide as you wish.


## Future plans

Over time, I will likely update this repository when I need to learn
something new, or am preparing materials that document the process of
creating the game engine. It's unlikely there will be large structural
changes to the game itself. However, if you have suggestions, issues, or
comments, feel free to tag them on the "issues" page!


## License
This project is released under GPLv2 as an educational resource. Feel free
to copy, modify, and redistribute as you wish, as long as the derivative
work also remains free. See the LICENSE.txt for more details.


