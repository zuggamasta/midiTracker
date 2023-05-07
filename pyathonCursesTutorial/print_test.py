from curses import wrapper
from curses.textpad import Textbox, rectangle
import time

def main(stdscr):
    stdscr.addstr(f"henlo this is range 1: {range(0)} ")
    while 1:
        key = stdscr.getkey()
        stdscr.addstr(f"{key} ")


wrapper(main)