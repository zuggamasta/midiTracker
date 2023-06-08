import curses
from curses import wrapper


def main(stdscr):

	height,width = stdscr.getmaxyx()


	with open('help/rample_midi.txt') as f:
		info_rample = f.read()
		f.close()

	pad = curses.newpad(50,120)
	pad.addstr(info_rample)
	
	stdscr.refresh()

	pad.refresh(0,0,0,0,height-1,width)

	stdscr.getch()

wrapper(main)