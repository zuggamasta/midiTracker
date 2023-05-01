# utilities
import sys
import time

# midi libs
import mido
from mido import Message

# UI libs
import curses
from curses import wrapper

#CONSTANTS
SCENES = ["song","chain","phrase","config"]
NOTES_LOOKUP = ['C ','C#','D ','Eb','E ','F ','F# ','G ','G#','A ','Bb','B ' ]
SLOT_WIDTH = 4

MAX_CHANNELS = 6


pos = [0,0]


is_song_playing = True

bpm = 120

# scene infos
current_scene = 0
active_data = []

# Generates empty CHAIN slots for Song 
current_song = 0
song0 = [[None for _ in range(16)] for _ in range(6)]

song0[0][0] = 0x00

song_data = []
song_data.append(song0)

current_chain = 0
chain_data = []
chain0 =    [[0x01,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],  # PHRASES
             [0x10,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]   # TRANSPOSE
chain_data.append(chain0)

current_phrase = 0
phrase_data = []
phrase0 =  [[0x5c,None,None,None,None,None,None,None, # NOTES
             0x5c,None,None,None,None,None,None,None],
            [0x5c,None,None,None,None,None,None,None, # CMD
             0x5c,None,None,None,None,None,None,None]]

phrase1 =  [[0x5c,None,None,None,None,None,None,None, # NOTES
             0x5c,0xff,0xff,0xff,0xff,0xff,None,None],
            [0x5c,None,None,None,None,None,None,None, # CMD
             0x5c,None,None,None,None,None,None,None]]
  
phrase_data.append(phrase0)

phrase_data.append(phrase1)

phrase2 =  [[0x5c,None,None,None,None,None,None,None, # NOTES
             0x5c,0xff,0xff,0xff,0xff,0xff,None,None],
            [0x5c,None,None,None,None,None,None,None, # CMD
             0x5c,None,None,None,None,None,None,None]]

phrase_data.append(phrase2)




config_data = []
config=  [[0x00,None,0xff,0xab]   ]  
config_data.append(config)

def updateInput(scr,data,max_column,max_row):

    global pos
    global current_scene
    global current_song
    global current_chain
    global current_phrase
    global active_data

    if current_scene == 0:
        active_data = current_song
    elif current_scene == 1:
        active_data = current_chain
    elif current_scene == 2:
        active_data = current_phrase
    elif current_scene == 3:
        active_data == 0
    

    try:
        key = scr.getkey()
    except:
        key = None



    # SWITCH SCENE 
    if key == "kRIT5":
        current_scene += 1
    elif key == "kLFT5":
        current_scene -= 1

     # SWITCH CHAIN / SONG / PHRASE  kUP5 kDN5
    elif key == "kUP5":
        current_phrase += 1
    elif key == "kDN5":
        current_phrase -= 1
 
    elif key == " ":
        play_chain(0,0,scr)

    # MODIFY DATA
    elif key == "KEY_SR":
        if data[active_data][pos[0]][pos[1]] == None:
            data[active_data][pos[0]][pos[1]] = 0x0
        else:
            data[active_data][pos[0]][pos[1]] += 0x1
    elif key == "KEY_SF":
        if data[active_data][pos[0]][pos[1]] == None:
            data[active_data][pos[0]][pos[1]] = 0x0
        else:
            data[active_data][pos[0]][pos[1]] -= 0x1
    elif key == "KEY_SRIGHT":
        if data[active_data][pos[0]][pos[1]] == None:
            data[active_data][pos[0]][pos[1]] = 0x0
        else:
            data[active_data][pos[0]][pos[1]] += 12
    elif key == "KEY_SLEFT":
        if data[active_data][pos[0]][pos[1]] == None:
            data[active_data][pos[0]][pos[1]] = 0x0
        else:
            data[active_data][pos[0]][pos[1]] -= 12
    elif key == "x":
        if data[active_data][pos[0]][pos[1]] == None:
            pass
        else:
            data[active_data][pos[0]][pos[1]] = None

    # MOVE CURSOR
    elif key == "KEY_UP":
        pos[1] -= 1
    elif key == "KEY_DOWN":
        pos[1] += 1
    elif key == "KEY_RIGHT":
        pos[0] += 1
    elif key == "KEY_LEFT":
        pos[0] -= 1
    
    # QUIT APPLICATION

    elif key == "q":
            quit()
    else:
        pass
    
    # WRAP SCENE AROUND
    if current_scene > 3:
        current_scene = 0
    if current_scene < 0:
        current_scene = 3
    
    # WRAP CURSOR AROUND
    if pos[0] < 0:
        pos[0] = max_column-1
    if pos[1] < 0:
        pos[1] = max_row-1
    if pos[0] >= max_column:
        pos[0] = 0
    if pos[1] >= max_row:
        pos[1] = 0

    if data[active_data][pos[0]][pos[1]] != None:
        if data[active_data][pos[0]][pos[1]] < 0:
            data[active_data][pos[0]][pos[1]] = 255
        if data[active_data][pos[0]][pos[1]] > 255:
            data[active_data][pos[0]][pos[1]] = 0

    scr.refresh()

    return pos

def drawData(scr,data,max_column,max_row,is_note):
    data_win = curses.newwin(16,6*4+1,3,2)

    for column in range(max_row):
        for row in range(max_column):
            slot = data[active_data][row][column]
            note = 0x0
            render_slot = ""
            if slot == None:
                render_slot = " -- "
            else:
                if is_note:
                    note = NOTES_LOOKUP[int(slot)%12]
                    render_slot = f" {note}{round(int(slot/12)%12)+1}"
                else:
                    render_slot = f" {slot:02x} "

            if column == pos[1] and row == pos[0]:
                data_win.addstr(column,row*SLOT_WIDTH,render_slot, curses.A_REVERSE | curses.A_BOLD)
            else:
                data_win.addstr(column,row*SLOT_WIDTH,render_slot, curses.A_BOLD)

    scr.refresh()
    data_win.refresh()


song_step = 0

def play_song():
    global song_step
    for channel in range(MAX_CHANNELS):
        active_chain_no = song_data[current_song][channel][song_step]
        play_chain(active_chain_no,channel)
        pass
    song_step += 1 
    pass 

# CHAIN_DATA[chain_number][0=phrase,1=transpose][chain_step]
def play_chain(chain_no,channel,scr):
    chain_step = 0
      
    if chain_data[chain_no][0][chain_step] != None:
        scr.addstr(3,36,f"debug: {chain_data[chain_no][0][chain_step]:02x}", curses.A_ITALIC)
        
        pass
    pass

def note_on(data,active_data,max_column,max_row):
    global last_notes
    last_notes = [None,None,None,None,None,None]
    
    for column in range(max_row):
        for row in range(max_column):
            slot = data[active_data][row][column]
            
            if slot == None:
                # not a musical note
                pass
            else:
                # set musical note to channel message
                # output note on

                pass

            ## TODO: implement preliste if is_song_playing  == false

            if column == pos[1] and row == pos[0]:
                # prelisten ?
                # set musical note to channel message
                # output note on
                pass




def drawColumNumbers(scr):

    header_win = curses.newwin(17,2,3,0)
    for frame in range(16):
        header_win.addstr(frame, 0, f"{frame:02}", curses.A_REVERSE)

    scr.refresh()
    header_win.refresh()

def main(stdscr):

    # CURSES SETUP
    stdscr.keypad(True)
    stdscr.nodelay(True)
    # HIDE CURSES CURSOR
    curses.curs_set(0)

    stdscr.addstr("aMidiTracker v.01 ")

    while 1:

        outport = None

        if outport == None:
            available_ports = mido.get_input_names()

            outport = mido.open_output()

        stdscr.addstr(0,13,f"{available_ports}")

        match current_scene:
            
            case 0:
                # SONG VIEW
                # Header
                stdscr.addstr(1,2,f"{SCENES[current_scene]} {current_song:02}      ")
                stdscr.addstr(2,2,f"Trk1Trk2Trk3Trk4Trk5Trk6",curses.A_REVERSE)
                
                # DATA
                channels = 6
                steps = 16
                updateInput(stdscr,song_data,channels,steps)
                drawColumNumbers(stdscr)
                drawData(stdscr,song_data,channels,steps,is_note=False)
            case 1:
                # CHAIN VIEW
                # Header
                stdscr.addstr(1,2,f"{SCENES[current_scene]} {current_chain:02}      ")
                stdscr.addstr(2,2,f"PhrsTrsp",curses.A_REVERSE)
                stdscr.addstr("                          ")

                # DATA
                channels = 2
                steps = 16
                updateInput(stdscr,chain_data,channels,steps)
                drawColumNumbers(stdscr)
                drawData(stdscr,chain_data,channels,steps,is_note=False)
            case 2:
                # PHRASE VIEW
                # Header
                stdscr.addstr(1,2,f"{SCENES[current_scene]} {current_phrase:02}      ")
                stdscr.addstr(2,2,f"Note CMD",curses.A_REVERSE)
                stdscr.addstr("                          ")

                # DATA
                channels = 2
                steps = 16
                updateInput(stdscr,phrase_data,channels,steps)
                drawColumNumbers(stdscr)
                drawData(stdscr,phrase_data,channels,steps,is_note=True)
            case 3:
                # CONFIG VIEW
                # Header
                stdscr.addstr(1,2,f"{SCENES[current_scene]} ")
                stdscr.addstr(2,2,f"Val Key",curses.A_REVERSE)

                # clear line
                stdscr.addstr("                                      ")
                # clear vertical line
                for i in range(16):
                    stdscr.addstr(i+3,0,"  ")

                # DATA
                channels = 1
                steps = 4
                updateInput(stdscr,config_data,channels,steps)
                drawData(stdscr,config_data,channels,steps,is_note=False)
                pass

            case _:
            
                pass
        stdscr.refresh()

wrapper(main)

