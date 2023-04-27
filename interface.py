# utilities
import sys
import time

# midi libs
import mido
from mido import Message

# UI libs
import curses
from curses import wrapper

pos = [0,0]

MAX_CHANNEL_AMOUNT = 6
MAX_SCREEN_LENGTH = 16
current_chain = 0

is_song_playing = True

bpm = 120

# scene infos
SCENES = ["## Song ##","## Chain ##","## Pattern ##","## Config ##"]
current_scene = 0

# Generates empty CHAIN slots for Song 
song_data = [[None for _ in range(16)] for _ in range(6)]

def updateCursor(scr):
    try:
        key = scr.getkey()
    except:
        key = None

    global pos
    global song_data

    if key == "KEY_SR":
        if song_data[pos[0]][pos[1]] == None:
            song_data[pos[0]][pos[1]] = 0x0
        else:
            song_data[pos[0]][pos[1]] += 0x1
    if key == "KEY_SF":
        if song_data[pos[0]][pos[1]] == None:
            song_data[pos[0]][pos[1]] = 0x0
        else:
            song_data[pos[0]][pos[1]] -= 0x1
    elif key == "KEY_UP":
        pos[1] -= 1
    elif key == "KEY_DOWN":
        pos[1] += 1
    elif key == "KEY_RIGHT":
        pos[0] += 1
    elif key == "KEY_LEFT":
        pos[0] -= 1
    else:
        pass
    
    if pos[0] < 0:
        pos[0] = 0

    if pos[1] < 0:
        pos[1] = 0

    return pos
    
        

def drawData(scr,data,cursor):

    

    data_win = curses.newwin(16,6*4+1,3,1)

    for column in range(MAX_SCREEN_LENGTH):
        for row in range(MAX_CHANNEL_AMOUNT):
            slot = data[row][column]
            if slot == None:
                data_win.addstr(column,row*4,f" -- ")
            else:
                data_win.addstr(column,row*4,f"{slot}")

    data_win.move(cursor[1],cursor[0]*4+2)

    scr.refresh()
    data_win.refresh()


def songView(scr):

    scr.addstr(1,0,f"{SCENES[0]}")

    header_win = curses.newwin(17,2,3,0)
    for frame in range(16):
        header_win.addstr(frame, 0, f"{frame:02}", curses.A_REVERSE)

    scr.refresh()
    header_win.refresh()



def main(stdscr):

    stdscr.keypad(True)
    stdscr.addstr("aMidiTracker")


    while 1:
        songView(stdscr)
        drawData(stdscr,song_data, updateCursor(stdscr))

        try:
            key = stdscr.getkey()
        except:
            key = None

        if key == "q":
            quit()
        
    stdscr.getch()
    

    


wrapper(main)

