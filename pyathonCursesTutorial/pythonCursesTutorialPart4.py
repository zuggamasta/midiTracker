import curses
from curses import wrapper

import time

def main(stdscr):
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_YELLOW)
    RED_YELLOW = curses.color_pair(1)
    YELLOW_RED = curses.color_pair(2)

    x,y = 0, 0

    while True:
        key = stdscr.getkey()
        if key == "KEY_DOWN":
            y += 1
            
        elif key == "KEY_UP":
            y -=1

        stdscr.clear()
        stdscr.addstr(y,x, "1")
        stdscr.refresh()

    
        
wrapper(main)