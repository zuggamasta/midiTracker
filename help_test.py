#v0.3
import time

import curses
from curses import wrapper

cc_scroll = 0
running = True

def update_input(scr):
	global cc_scroll

	try:
			key = scr.getkey()
	except:
			key = None
			is_dirty = False
	
	if key == "KEY_UP":
		cc_scroll -= 1
	if key == "KEY_DOWN":
		cc_scroll += 1
	
	if cc_scroll < 0: cc_scroll = 0


def main(stdscr):

	global cc_scroll

	HEIGHT,WIDTH = stdscr.getmaxyx()

	with open('help/rample_midi.txt') as f:
		info_rample = f.read()
		f.close()

	pad = curses.newpad(50,120)
	pad.addstr(info_rample)
	stdscr.refresh()

	while running:
		pad.refresh(cc_scroll,0,0,0,HEIGHT-1,WIDTH-1)
		time.sleep(0.03)

		update_input(stdscr)



wrapper(main)