import time

import curses
from curses import wrapper

i = 0

def main(stdscr):

	global i

	height,width = stdscr.getmaxyx()


	with open('help/rample_midi.txt') as f:
		info_rample = f.read()
		f.close()

	pad = curses.newpad(50,120)
	pad.addstr(info_rample)
	
	stdscr.refresh()
	while i < 100:
		pad.refresh(i,0,0,0,height-1,width-1)
		i += 1;
		time.sleep(0.33)


	stdscr.getch()

wrapper(main)