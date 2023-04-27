from curses import wrapper
from curses.textpad import Textbox, rectangle
import time

def main(stdscr):
    while 1:
        key = stdscr.getkey()
        stdscr.addstr(f"{key} ")


wrapper(main)