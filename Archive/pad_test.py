import curses
from curses import wrapper
import time
ANIMATION_START = 16
def main(stdscr):
	curses.noecho()
	curses.curs_set(0)
	stdscr.keypad(False)
	stdscr.addstr("v0.1")
	HEIGHT,WIDTH = stdscr.getmaxyx()
	INTRO_TEXT = ("                                        oo          dP    oo\n                                                    88      \n                          88d8b.d8b.    dP    .d888b88    dP\n                          88'`88'`88    88    88'  `88    88\n                          88  88  88    88    88.  .88    88\n                          dP  dP  dP    dP    `88888P8    dP\n                                                            \n  dP                              dP                        \n  88                              88                        \nd8888P 88d888b. .d8888b. .d8888b. 88  .dP  .d8888b. 88d888b.\n  88   88'  `88 88\'  `88 88\'  `\"\" 88888\"   88ooood8 88'  `88\n  88   88       88.  .88 88.  ... 88  `8b. 88.  ... 88      \n  dP   dP       `8888'P8 `88888P' dP   `YP `88888P' dP      \n ")
	pad = curses.newpad(16,68)
	pad.addstr(INTRO_TEXT)
	for i in range(ANIMATION_START):
		pad.refresh(0,0,0,ANIMATION_START-1-i,HEIGHT-1,WIDTH-1)
		stdscr.addstr(0,0,"v0.1")
		stdscr.refresh()
		time.sleep(0.033)
	time.sleep(0.033)	
	# while True:
	# 	try:
	# 		key = stdscr.getkey()
	# 	except:
	# 		key = None
	# 	stdscr.addstr(f"{key}")
	# 	stdscr.refresh()

wrapper(main)