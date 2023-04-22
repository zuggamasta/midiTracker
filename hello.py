import curses
from curses import wrapper

import time

import rtmidi

def main(stdscr):
    bpm = 120

    cursor = [3,3]

    stdscr.move(cursor[0],cursor[1])

    offset_x = 3
    offset_y = 3

    data = [
        ["0C","ff","99", "A3", "00", "00", "mod", "00"],
        ["1C","ff","99", "A3", "00", "00", "mod", "00"],
        ["0C","ff","99", "A3", "00", "00", "mod", "00"],
        ["1C","ff","99", "A3", "00", "00", "mod", "00"],
        ["0C","ff","99", "A3", "00", "00", "mod", "00"],
        ["1C","ff","99", "A3", "00", "00", "mod", "00"],
        ["0C","ff","99", "A3", "00", "00", "mod", "00"],
        ["1C","ff","99", "A3", "00", "00", "mod", "00"],
        ["0C","ff","99", "A3", "00", "00", "mod", "00"]]
    
    data.extend(data)

    while(True):

        for i in range(0,64):
            stdscr.erase()
            
            stdscr.addstr(f"BPM: {bpm}")
            stdscr.addstr(2,3,"NoteLengNoteLengNoteLengMod Prm",curses.A_BOLD | curses.A_REVERSE)

            for x in range(0,8):
                for y in range(0,16):
                    stdscr.addstr(y+offset_y, x*4+offset_x, data[y][x])
                    
                    if(i%16 == y):  
                        if(0 == x):
                            stdscr.addstr(y+offset_y, x*3+offset_x, data[y][x], curses.A_REVERSE)

            stdscr.refresh()
            
            time.sleep(60/bpm/8)

    stdscr.getch()

wrapper(main)

