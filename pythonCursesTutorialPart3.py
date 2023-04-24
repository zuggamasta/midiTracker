import curses
from curses import wrapper

import time

def main(stdscr):
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_YELLOW)
    RED_YELLOW = curses.color_pair(1)
    YELLOW_RED = curses.color_pair(2)

    counter_win = curses.newwin(1, 20, 10, 10)
    stdscr.addstr( 10, 20,"hello world")
    stdscr.refresh()

    for i in range(16):
        counter_win.clear()
        color = RED_YELLOW

        if i % 2 == 0:
            color = YELLOW_RED
        
        counter_win.addstr(f"Count: {i}",color)
        counter_win.refresh()
        time.sleep(0.33)
    
    stdscr.getch()

wrapper(main)