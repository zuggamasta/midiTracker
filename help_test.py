#v0.3
import time

import curses
from curses import wrapper

cc_scroll = 0

def main(stdscr):

	global cc_scroll

	HEIGHT,WIDTH = stdscr.getmaxyx()

	with open('help/rample_midi.txt') as f:
		info_rample = f.read()
		f.close()

	pad = curses.newpad(50,120)
	pad.addstr(info_rample)
	
	stdscr.refresh()
	while cc_scroll < 100:
		pad.refresh(cc_scroll,0,0,0,HEIGHT-1,WIDTH-1)
		cc_scroll += 1;
		time.sleep(0.03)


	stdscr.getch()

wrapper(main)