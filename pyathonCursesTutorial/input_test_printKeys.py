import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
import time

def main(stdscr):

    win = curses.newwin(18,48,0,0)
    box = Textbox(win)

    stdscr.border()
    stdscr.refresh()

    
    stdscr.getch()

wrapper(main)