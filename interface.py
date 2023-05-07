# utilities
import sys
import time
import math

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
RENDER_STYLE = ['int','hex','tet','chr']
MAX_CHANNELS = 6

time_step = 0

cursor = [0,0]

is_song_playing = True

bpm = 120

# scene infos
current_scene = 0

active_data = 0 
active_chain = []
active_phrase = []

midi_messages = [None for _ in range(MAX_CHANNELS)]


song_step = 0
chain_step = 0
phrase_step = 0

# SONGS
current_song = 0
song_data = []
song0 = [[None for _ in range(16)] for _ in range(6)]
song_data.append(song0)

# CHAINS
current_chain = 0
chain_data = []
chain0 = [[None for _ in range(16)] for _ in range(2)] # phrase | transpose
chain_data.append(chain0)

current_phrase = 0
# PHRASES
phrase_data = []
phrase0 = [[None for _ in range(16)] for _ in range(2)] # note | CMD
phrase_data.append(phrase0)

current_config = 0
config_data = []
config=  [[0x00,None,0xff,0xab],[0x00,None,0xff,0xab] ]  
config_data.append(config)

def updateInput(scr,data,max_column,max_row):

    global cursor
    global current_scene
    global current_song
    global current_chain
    global current_phrase
    global curret_config
    global active_data
    

    try:
        key = scr.getkey()
    except:
        key = None


    if current_scene == 0:
        active_data = current_song
    elif current_scene == 1:
        active_data = current_chain
    elif current_scene == 2:
        active_data = current_phrase
    elif current_scene == 3:
        active_data == current_config


    # SWITCH SCENE 
    if key == "kRIT5":
        current_scene += 1
    elif key == "kLFT5":
        current_scene -= 1

     # SWITCH CHAIN / SONG / PHRASE  kUP5 kDN5
    elif key == "kUP5":
        # CHAIN SCENE
        if current_scene == 1:
            if current_chain+2 > len(chain_data) :
                chain_data.append([[None for _ in range(16)] for _ in range(2)])
            current_chain += 1
        # PHRASE SCENE
        if current_scene == 2:
            if current_phrase+2 > len(phrase_data) :
                phrase_data.append([[None for _ in range(16)] for _ in range(2)])
            current_phrase += 1
        
    elif key == "kDN5":
        # CHAIN SCENE
        if current_scene == 1:
            current_chain -= 1
            if current_chain < 0:
                current_chain = 0


        # PHRASE SCENE
        if current_scene == 2:
            current_phrase -= 1
            if current_phrase < 0:
                current_phrase = 0
 
    elif key == " ":
        play_chain(0,0,scr)

    # MODIFY DATA
    elif key == "KEY_SR":
        if data[active_data][cursor[0]][cursor[1]] == None:
            data[active_data][cursor[0]][cursor[1]] = 0x0
        else:
            data[active_data][cursor[0]][cursor[1]] += 0x1
    elif key == "KEY_SF":
        if data[active_data][cursor[0]][cursor[1]] == None:
            data[active_data][cursor[0]][cursor[1]] = 0x0
        else:
            data[active_data][cursor[0]][cursor[1]] -= 0x1
    elif key == "KEY_SRIGHT":
        if data[active_data][cursor[0]][cursor[1]] == None:
            data[active_data][cursor[0]][cursor[1]] = 0x0
        else:
            data[active_data][cursor[0]][cursor[1]] += 12
    elif key == "KEY_SLEFT":
        if data[active_data][cursor[0]][cursor[1]] == None:
            data[active_data][cursor[0]][cursor[1]] = 0x0
        else:
            data[active_data][cursor[0]][cursor[1]] -= 12
    elif key == "x":
        if data[active_data][cursor[0]][cursor[1]] == None:
            pass
        else:
            data[active_data][cursor[0]][cursor[1]] = None

    # MOVE CURSOR
    elif key == "KEY_UP":
        cursor[1] -= 1
    elif key == "KEY_DOWN":
        cursor[1] += 1
    elif key == "KEY_RIGHT":
        cursor[0] += 1
    elif key == "KEY_LEFT":
        cursor[0] -= 1

    # QUIT APPLICATION

    elif key == "q":
            sys.exit()
    else:
        pass
    
    # WRAP SCENE AROUND
    if current_scene > 3:
        current_scene = 0
    if current_scene < 0:
        current_scene = 3
    
    # WRAP CURSOR AROUND
    if cursor[0] < 0:
        cursor[0] = max_column-1
    if cursor[1] < 0:
        cursor[1] = max_row-1
    if cursor[0] >= max_column:
        cursor[0] = 0
    if cursor[1] >= max_row:
        cursor[1] = 0

    if current_scene == 4:
        active_data = 0

    if data[active_data][cursor[0]][cursor[1]] != None:
        if data[active_data][cursor[0]][cursor[1]] < 0:
            data[active_data][cursor[0]][cursor[1]] = 255
        if data[active_data][cursor[0]][cursor[1]] > 255:
            data[active_data][cursor[0]][cursor[1]] = 0

    scr.refresh()

    return cursor

def drawData(scr,data,max_column,max_row,render_style):
    data_win = curses.newwin(16,6*4+1,3,2)

    for column in range(max_row):
        for row in range(max_column):
            slot = data[active_data][row][column]
            note = 0x0
            render_slot = ""
            if slot == None:
                render_slot = " -- "
            else:
                if render_style == 'tet':
                    note = NOTES_LOOKUP[int(slot)%12]
                    render_slot = f" {note}{round(int(slot/12)%12)+1}"
                elif render_style == 'hex':
                    render_slot = f" {slot:02x} "
                elif render_style == 'int':
                    render_slot = f" {slot:02} "

            if column == cursor[1] and row == cursor[0]:
                data_win.addstr(column,row*SLOT_WIDTH,render_slot, curses.A_REVERSE | curses.A_BOLD)
            else:
                data_win.addstr(column,row*SLOT_WIDTH,render_slot, curses.A_BOLD)

    scr.refresh()
    data_win.refresh()


# NOTE: Playback code happens here

def play_song(song):
    global song_step
    global chain_step
    global phrase_step
    global song_data
    for song_channel in range(MAX_CHANNELS):
        
        song_step = 0

        if song_step < 16:
            active_chain_no = song_data[song][song_channel][song_step]
            if active_chain_no !=  None:
                play_chain(active_chain_no,song_channel)
            else:
                pass

    time.sleep(60/bpm/16)
    phrase_step += 1 

    if phrase_step >= 16:
        phrase_step = 0
        chain_step += 1

    if chain_step >= 16:
        chain_step = 0
        song_step +=1
    
    if song_step >= 16:
        song_step = 0


def play_chain(chain_no,channel):
    global chain_step 
    if chain_step < 16:
        phrase = chain_data[chain_no][0][chain_step]        
        if phrase !=  None:
            play_phrase(phrase, channel)
        else:
            pass
        chain_step += 1


def play_phrase(phrase_no,channel):
    global phrase_step
    if phrase_step < 16:
        note = phrase_data[phrase_no][0][phrase_step]
        if note !=  None:
            play_note(note, channel)
        else:
            play_rest()


def play_note(note, channel):
    outport.send(Message('note_on', channel=channel, note=note, velocity=120))
    time.sleep(1/1000)
    outport.send(Message('note_off', channel=channel, note=note, velocity=120))

def play_rest():
    pass


# NOTE: Playback code ends here

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

            if column == cursor[1] and row == cursor[0]:
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
    global time_step
    global RED
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    RED = curses.color_pair(1)
    global GREEN
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    GREEN = curses.color_pair(2)

    # CURSES SETUP
    stdscr.keypad(True)
    stdscr.nodelay(True)
    #stdscr.timeout(150)
    # HIDE CURSES CURSOR
    curses.curs_set(0)
    stdscr.addstr("aMidiTracker v.01 ")

    global outport
    outport = None

    while 1:

        if outport == None:
            available_ports = mido.get_input_names()

            outport = mido.open_output()

        stdscr.addstr(0,13,f"{available_ports[0]}")

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
                drawData(stdscr,song_data,channels,steps,render_style='int')
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
                drawData(stdscr,chain_data,channels,steps,render_style='int')
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
                drawData(stdscr,phrase_data,channels,steps,render_style='tet')
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
                channels = 2
                steps = 4
                updateInput(stdscr,config_data,channels,steps)
                drawData(stdscr,config_data,channels,steps,render_style='hex')
                pass

            case _:
            
                pass
        
        if is_song_playing:
            play_song(0)
        
        

        stdscr.refresh()

wrapper(main)

