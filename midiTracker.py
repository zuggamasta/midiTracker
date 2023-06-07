# PYTHON UTILITY MODULES
import sys
import time
import json
from datetime import datetime
from copy import copy
import random

# MIDI OBJECT MODULE (Requires python-rtmidi)
import mido
from mido import Message

# CURSES MODULE, Interface rendering
import curses
from curses import wrapper

################################
#          CONSTANTS           #
################################

SCREENS = ["SONG","CHAIN","PHRASE","CONFIG"]

MODIFIERS_LOOKUP = [" Bck"," Hld"," Jmp"," Rnd"," Stc"," Rtg","PC1"]
MODIFIERS_LEN = len(MODIFIERS_LOOKUP)
NOTES_LOOKUP = ['C ','C#','D ','Eb','E ','F ','F#','G ','G#','A ','Bb','B ' ]
SLOT_WIDTH = 4
RENDER_STYLE = ['int','hex','tet','chr']
MAX_MIDI = 128
HEIGHT, WIDTH = 0,0 # Will be set by the program to the height and with of the available screen in Chracters.
MAX_CONFIG_STEPS = 4    # DO NOT CHANGE
MAX_CHAIN_PARAMETERS = 2
MAX_PHRASE_PARAMETERS = 7



# USER EDITABLE CONSTANTS
MAX_CHANNELS = 8        # DEFAULT = 8
MAX_SONG_STEPS = 8      # DEFAULT = 8
MAX_CHAIN_STEPS = 4     # DEFAULT = 4
MAX_PHRASE_STEPS = 16   # DEFAULT = 16
MIDI_PORT = 0           # DEFAULT = 0, Initial Midiport, only edit if you know what you're doing.
SUB_STEPS = 8           # DEFAULT = 8, Reducing sub steps can make the app more performant, but the interface less responsive.

# TEXT ELEMENTS
INTRO_TEXT = ("\n                                        oo          dP    oo\n                                                    88      \n                          88d8b.d8b.    dP    .d888b88    dP\n                          88'`88'`88    88    88'  `88    88\n                          88  88  88    88    88.  .88    88\n                          dP  dP  dP    dP    `88888P8    dP\n                                                            \n  dP                              dP                        \n  88                              88                        \nd8888P 88d888b. .d8888b. .d8888b. 88  .dP  .d8888b. 88d888b.\n  88   88'  `88 88\'  `88 88\'  `\"\" 88888\"   88ooood8 88'  `88\n  88   88       88.  .88 88.  ... 88  `8b. 88.  ... 88      \n  dP   dP       `8888'P8 `88888P' dP   `YP `88888P' dP      \n ")
HELP_TEXT_SONG="Use the modifiers switch between cursor movement and editing values. Change with the numbers 1-4 between screens. "
HELP_TEXT_CHAIN="Use chains to connect multiple phrases together. Each new chain is filled with phrases. "
HELP_TEXT_PHRASE="Use phrases to arrange notes on a sixteenth grid. "
HELP_TEXT_CONFIG="Use the configuration page to set Midi device, tempo and other settings. "
HEADER_STRING = "Chn1Chn2Chn3Chn4RmplChn6Chn7Chn8Chn9Ch10Ch11Ch12Ch13Ch14Ch15Ch16"[0:MAX_CHANNELS*SLOT_WIDTH]

# INPUT
KEYMAP = {
    "up" :      "KEY_UP",
    "down":     "KEY_DOWN",
    "left":     "KEY_LEFT",
    "right":    "KEY_RIGHT",
    "moda":     "a",
    "modb":     "s",
    "delete":   "x",
    "quit":     "Q",
    "save":     "S",
    "panic":    "w",
    "restart":  " ",
    "help":     "h",
    "song":     "1",
    "chain":    "2",
    "phrase":   "3",
    "config":   "4",
    "help":     "h",
    "copy":     "c",
    "paste":    "v",
    "flood":    "V"
    }

# LAYOUT
STEP_INFO_Y, STEP_INFO_X = 5, 2 + MAX_CHANNELS*SLOT_WIDTH + 2
TABLE_HEADER_Y, TABLE_HEADER_X = 2, 2

################################
#          VARIABLES           #
################################

# TIME AND ANIMATION
sub_step = 0
help_scroll = 0
bpm = 90

# INTERFACE AND UI
cursor = [0,0]
current_screen = 0
active_data = 0 

# BOOLS
is_song_playing = True
is_show_help = False
is_dirty = False
shift_mod_a = False
shift_mod_b = False
shift_mod_color = 0

# BUFFERS
copy_buffer = 0
midi_messages_buffer = [None for _ in range(MAX_CHANNELS)]
current_notes_buffer = [None for _ in range(MAX_CHANNELS)]
current_modifier_buffer = [[None for _ in range(2)] for _ in range(MAX_CHANNELS)]
current_cc_buffer = [[None for _ in range(2)] for _ in range(MAX_CHANNELS)]


last_notes_buffer =    [None for _ in range(MAX_CHANNELS)]
active_chain_buffer = []
active_phrase_buffer = []

# TRANSPORT
song_step = 0
chain_step = 0
phrase_step = 0

# SONG DATA
current_song = 0
song_data = [[[None for _ in range(MAX_SONG_STEPS)] for _ in range(MAX_CHANNELS)]]

# CHAINS DATA
current_chain = 0
chain_data = [[[i for _ in range(MAX_CHAIN_STEPS)] for _ in range(MAX_CHAIN_PARAMETERS)] for i in range(MAX_MIDI)] # phrase | transpose

# PHRASES DATA
current_phrase = 0
phrase_data = [[[None for _ in range(MAX_PHRASE_STEPS)] for _ in range(MAX_PHRASE_PARAMETERS)] for _ in range(MAX_MIDI)] # note | CMD

# CONFIG DATA
current_config = 0
config_data = []
config=  [[0x01,120,0xff,0xab],["Midi Device","BPM",0xff,0xab] ]  
config_data.append(config)

def draw_debug(scr,value):
    scr.addstr(19,0,value)

def load_state(autoload):
    
    global song_data
    global chain_data
    global phrase_data
    global config_data

    save_file_name = None
    has_load_argument = False

    if autoload:
        try:
            with open(f"savestate.json", "r") as fp:
                loaded_data = json.load(fp)

                song_data = loaded_data[0]
                chain_data = loaded_data[1]
                phrase_data = loaded_data[2]
                config_data = loaded_data [3]
        except:
            save_state_data = []

            save_state_data.append(song_data)
            save_state_data.append(chain_data)
            save_state_data.append(phrase_data)
            save_state_data.append(config_data)
            with open(f"savestate.json", "w") as fp:
                json.dump(save_state_data, fp )  # Use indent=4 for a pretty-formatted JSON file

    try:
        arguments = sys.argv
        if arguments[1] == "-load":
            has_load_argument = True
            save_file_name = arguments[2]
        # print("  LOADING...       ")
        
        # Load the JSON file back as a dictionary
        with open(f"{save_file_name}", "r") as fp:
            loaded_data = json.load(fp)

            song_data = loaded_data[0]
            chain_data = loaded_data[1]
            phrase_data = loaded_data[2]
            config_data = loaded_data[3]
    except:
        if has_load_argument:
            print("  File not found")
            pass
        else:
            # print("  not loading   ")
            pass

def save_state():

    save_state_data = []

    save_state_data.append(song_data)
    save_state_data.append(chain_data)
    save_state_data.append(phrase_data)
    save_state_data.append(config_data)

    now = datetime.now()
    formatted_date = f"{now:%y%m%d-%H-%M}"
    print(formatted_date)

    with open(f"{formatted_date}.json", "w") as fp:
        json.dump(save_state_data, fp)  # Use indent=4 for a pretty-formatted JSON file

def update_input(scr,data,max_column,max_row,max_value = MAX_MIDI,large_step = 12):
    global song_step
    global chain_step
    global phrase_step
    global sub_step 

    global cursor
    global current_screen
    global current_song
    global current_chain
    global current_phrase
    global current_config
    global active_data

    global is_dirty
    global shift_mod_a
    global shift_mod_b
    global shift_mod_color
    global is_song_playing
    global is_show_help
    global copy_buffer

    is_dirty = True

    try:
        key = scr.getkey()
    except:
        key = None
        is_dirty = False

    if key == KEYMAP["moda"]:
        if shift_mod_b:
            shift_mod_b = False
        shift_mod_a = not shift_mod_a

    if key == KEYMAP["modb"]:
        if shift_mod_a:
            shift_mod_a = False
        shift_mod_b = not shift_mod_b

    if shift_mod_a:
        shift_mod_color = PRIMARY
    elif shift_mod_b:
        shift_mod_color = SECONDARY
    
    if not shift_mod_a and not shift_mod_b:
        shift_mod_color = 0

    if key == KEYMAP["copy"]:
        if current_screen == 3:
            return
        copy_buffer = copy(data[active_data][cursor[0]][cursor[1]] )

    if key == KEYMAP["paste"]:
        if current_screen == 3:
            return
        data[active_data][cursor[0]][cursor[1]] = copy(copy_buffer)
    
    if key == KEYMAP["flood"]:
        flood_length = 0
        if current_screen == 0:
            flood_length = MAX_SONG_STEPS
        elif current_screen == 1:
            flood_length = MAX_CHAIN_STEPS
        elif current_screen == 2:
            flood_length = MAX_PHRASE_STEPS
        elif current_screen == 3:
            flood_length = 0
        
        for i in range(flood_length):
            data[active_data][cursor[0]][i] = copy(copy_buffer)

        shift_mod_a = False
        shift_mod_b = False


    if current_screen == 0:
        active_data = current_song
    elif current_screen == 1:
        active_data = current_chain
    elif current_screen == 2:
        active_data = current_phrase
    elif current_screen == 3:
        active_data == current_config

    if key == "1":
        current_screen = 0
        shift_mod_a, shift_mod_b = False, False
    elif key == "2":
        current_screen = 1
        shift_mod_a, shift_mod_b = False, False
    elif key == "3":
        current_screen = 2
        shift_mod_a, shift_mod_b = False, False
    elif key == "4":
        current_screen = 3
        shift_mod_a, shift_mod_b = False, False
    elif key == "5":
        # current_screen = 4
        pass

     # SWITCH CHAIN / SONG / PHRASE  kUP5 kDN5
    elif key == KEYMAP["down"] and shift_mod_b:
        # CHAIN SCREEN
        if current_screen == 1:
            if current_chain+2 > len(chain_data) :
                chain_data.append([[None for _ in range(MAX_CHAIN_STEPS)] for _ in range(2)])
            current_chain += 1
        # PHRASE SCREEN
        if current_screen == 2:
            if current_phrase+2 > len(phrase_data) :
                phrase_data.append([[None for _ in range(MAX_PHRASE_STEPS)] for _ in range(2)])
            current_phrase += 1
        
    elif key == KEYMAP["up"] and shift_mod_b:
        # CHAIN SCREEN
        if current_screen == 1:
            current_chain -= 1
            if current_chain < 0:
                current_chain = 0

        # PHRASE SCREEN
        if current_screen == 2:
            current_phrase -= 1
            if current_phrase < 0:
                current_phrase = 0
 
    elif key == KEYMAP["help"]:
        is_show_help = not is_show_help

    elif key == KEYMAP["panic"]:
        panic()

    elif key == KEYMAP["restart"]:
        panic()
        is_song_playing = not is_song_playing
        song_step = 0
        chain_step = 0
        phrase_step = 0
        sub_step = 0
        global current_notes_buffer
        global last_notes_buffer
        current_notes_buffer = [None for _ in range(MAX_CHANNELS)]
        last_notes_buffer = [None for _ in range(MAX_CHANNELS)]
    
    elif key == KEYMAP["save"]:
        save_state()

    # MODIFY DATA
    elif key == KEYMAP["up"] and shift_mod_a:
        if data[active_data][cursor[0]][cursor[1]] == None:
            data[active_data][cursor[0]][cursor[1]] = 0x0
        else:
            data[active_data][cursor[0]][cursor[1]] += 0x1
    elif key == KEYMAP["down"] and shift_mod_a:
        if data[active_data][cursor[0]][cursor[1]] == None:
            data[active_data][cursor[0]][cursor[1]] = 0x0
        else:
            data[active_data][cursor[0]][cursor[1]] -= 0x1
    elif key == KEYMAP["right"] and shift_mod_a:
        if data[active_data][cursor[0]][cursor[1]] == None:
            data[active_data][cursor[0]][cursor[1]] = 0x0
        else:
            data[active_data][cursor[0]][cursor[1]] += large_step
    elif key == KEYMAP["left"] and shift_mod_a:
        if data[active_data][cursor[0]][cursor[1]] == None:
            data[active_data][cursor[0]][cursor[1]] = 0x0
        else:
            data[active_data][cursor[0]][cursor[1]] -= large_step
    elif key == KEYMAP["delete"]:
        if data[active_data][cursor[0]][cursor[1]] == None:
            pass
        else:
            data[active_data][cursor[0]][cursor[1]] = None

    # MOVE CURSOR

    if not shift_mod_a and not shift_mod_b:
        if key == KEYMAP["up"] :
            cursor[1] -= 1
        elif key == KEYMAP["down"]:
            cursor[1] += 1
        elif key == KEYMAP["right"]:
            cursor[0] += 1
        elif key == KEYMAP["left"]:
            cursor[0] -= 1



    # QUIT APPLICATION

    if key == KEYMAP["quit"]:
            panic()

            save_state_data = []

            save_state_data.append(song_data)
            save_state_data.append(chain_data)
            save_state_data.append(phrase_data)
            save_state_data.append(config_data)

            with open(f"savestate.json", "w") as fp:
                json.dump(save_state_data, fp)  # Use indent=4 for a pretty-formatted JSON file
            
            sys.exit()
    else:
        pass
    
    # WRAP CURSOR AROUND
    if cursor[0] < 0:
        cursor[0] = max_column-1
    if cursor[1] < 0:
        cursor[1] = max_row-1
    if cursor[0] >= max_column:
        cursor[0] = 0
    if cursor[1] >= max_row:
        cursor[1] = 0

    if current_screen == 3:
        active_data = 0
        current_config = 0

    if data[active_data][cursor[0]][cursor[1]] != None:
        if data[active_data][cursor[0]][cursor[1]] < 0:
            data[active_data][cursor[0]][cursor[1]] = max_value-1
        if data[active_data][cursor[0]][cursor[1]] > max_value-1:
            data[active_data][cursor[0]][cursor[1]] = 0
    
    scr.refresh()

    return cursor

def draw_data(scr,data,max_column,max_row,render_style=['int' for _ in range(MAX_CHANNELS)]):
    data_win = curses.newwin(max_row,max_column*4+2,3,2)

    for row in range(max_row):
        for column in range(max_column):
            slot = data[active_data][column][row]
            note = 0x0
            render_slot = ""
            if slot == None:
                render_slot = " -- "
            else:
                if render_style[column] == 'tet':
                    note = NOTES_LOOKUP[int(slot)%12]
                    render_slot = f" {note}{round(int(slot/12)%12)+1}"
                elif render_style[column] == 'hex':
                    render_slot = f" {slot:02x} "
                elif render_style[column] == 'int':
                    render_slot = f" {slot:02} "
                elif render_style[column] == 'str':
                    render_slot = f" {slot} "
                elif render_style[column] == 'mod':
                    modifier = MODIFIERS_LOOKUP[int(slot)%MODIFIERS_LEN]
                    render_slot = f"{modifier}" # warp around every modifier lookup character

            if row == cursor[1] and column == cursor[0]:
                data_win.addstr(row,column*SLOT_WIDTH,render_slot, curses.A_REVERSE | curses.A_BOLD)
            else:
                data_win.addstr(row,column*SLOT_WIDTH,render_slot, curses.A_BOLD)

    scr.refresh()
    data_win.refresh()

def draw_help(help_text):
    if not is_show_help:
        return
    global help_scroll
    help_pad = curses.newpad(1,512) # 512 is just a large number, this should be the max of helptext length * 2
    help_pad.addstr(help_text, shift_mod_color | curses.A_REVERSE)
    help_pad.addstr(help_text, shift_mod_color | curses.A_REVERSE)

    help_pad.refresh(0,int(help_scroll),HEIGHT-1,0,HEIGHT-1,WIDTH-1)
    help_scroll += 0.1
    if help_scroll > len(help_text):
        help_scroll = 0

def play_song(song, scr):
    global song_step
    global chain_step
    global phrase_step
    global song_data
    global current_notes_buffer
    global sub_step

    if(sub_step == 0):
        for song_channel in range(MAX_CHANNELS):
            
            if song_step < MAX_SONG_STEPS:
                active_chain_no = song_data[song][song_channel][song_step]
                if active_chain_no !=  None:
                    play_chain(active_chain_no,song_channel)
                else:
                    pass
        play_notes(current_notes_buffer,current_modifier_buffer,current_cc_buffer)

    time.sleep(60/bpm/4/SUB_STEPS)

    sub_step += 1

    if(sub_step >= SUB_STEPS):
        stop_notes(current_notes_buffer)
        phrase_step += 1 
        current_notes_buffer = [None for _ in range(MAX_CHANNELS)]
        sub_step = 0

    if phrase_step >= MAX_PHRASE_STEPS:
        phrase_step = 0
        chain_step += 1

    if chain_step >= MAX_CHAIN_STEPS:
        chain_step = 0
        song_step +=1
    
    if song_step >= MAX_SONG_STEPS:
        song_step = 0


def play_chain(chain_no,channel):
    global chain_step 
    phrase = chain_data[chain_no][0][chain_step]        
    if phrase !=  None:
        play_phrase(phrase, channel)
    else:
        pass

def play_phrase(phrase_no,channel):
    global phrase_step
    if phrase_step < MAX_PHRASE_STEPS:
        note = phrase_data[phrase_no][0][phrase_step]
        modifier = phrase_data[phrase_no][1][phrase_step],phrase_data[phrase_no][2][phrase_step]
        cc = phrase_data[phrase_no][5][phrase_step],phrase_data[phrase_no][6][phrase_step]
        save_note(note, modifier, cc, channel)

def save_note(note, modifier, cc, channel):
    
    current_notes_buffer[channel] = note
    current_modifier_buffer[channel] = modifier
    current_cc_buffer[channel] = cc


    last_notes_buffer[channel] = note

def play_notes(notes, modifiers, cc):
    for channel in range(MAX_CHANNELS):
        if cc[channel][0] != None and cc[channel][1] != None:
            outport.send(Message('control_change', channel=channel, control=cc[channel][0], value=cc[channel][1]))

        if notes[channel] != None:
            if modifiers[channel][0] == None:
                outport.send(Message('note_on', channel=channel, note=notes[channel], velocity=120))
            
            elif  modifiers[channel][0] == 3: # RND
                if modifiers[channel][1] == None:
                    outport.send(Message('note_on', channel=channel, note=notes[channel], velocity=120))
                else:
                    modifier_value =  modifiers[channel][1]
                    if modifier_value == None:
                        modifier_value == 0
                    modifier_value =  random.randint(0,modifier_value)
                    notes[channel] = (notes[channel]+modifier_value)%127
                    outport.send(Message('note_on', channel=channel, note=notes[channel], velocity=120))
            
            elif  modifiers[channel][0] == 2: # RND
                if modifiers[channel][1] == None:
                    outport.send(Message('note_on', channel=channel, note=notes[channel], velocity=120))
                else:
                    jump = random.randint(0, modifiers[channel][1]) #compare to 0?
                    if jump == 0:
                        outport.send(Message('note_on', channel=channel, note=notes[channel], velocity=120))
                    else:
                        pass

            
def stop_notes(notes):
    for channel in range(MAX_CHANNELS):
        if notes[channel] != None:
            outport.send(Message('note_off', channel=channel, note=notes[channel], velocity=120))

def play_rest():
    pass
    
def panic():
    for channel in range(MAX_CHANNELS):
        for note in range(MAX_MIDI):
            outport.send(Message('note_off', channel=channel, note=note, velocity=120))

def draw_column_no(scr,columns,step):
    header_win = curses.newwin(columns+1,2,3,0)

    for frame in range(columns):
        if frame == step:
            header_win.addstr(frame, 0, f"{frame:02}", shift_mod_color)
        else:
            header_win.addstr(frame, 0, f"{frame:02}", curses.A_REVERSE | shift_mod_color)

    scr.refresh()
    header_win.refresh()

def draw_intro(scr):
    global HEIGHT
    global WIDTH
    HEIGHT,WIDTH = scr.getmaxyx()

    pad = curses.newpad(16,68)
    ANIMATION_START = 16

    pad.addstr(INTRO_TEXT, curses.A_BOLD | PRIMARY )
    for i in range(ANIMATION_START):
        pad.refresh(0,0,0,ANIMATION_START-1-i,HEIGHT-1,WIDTH-1)
        scr.addstr(0,0,"v0.1", curses.A_BOLD | PRIMARY )
        scr.refresh()
        time.sleep(0.033)
    time.sleep(1.033)
    scr.clear()

def draw_step_info(scr,y_pos,x_pos):
        scr.attron(shift_mod_color | curses.A_STANDOUT)
        
        scr.addstr(y_pos+0,x_pos,f"song_step:   {song_step:02}")
        scr.addstr(y_pos+1,x_pos,f"chain_step:  {chain_step:02}")
        scr.addstr(y_pos+2,x_pos,f"phrase_step: {phrase_step:02}")
        
        scr.attroff(shift_mod_color | curses.A_STANDOUT)

def setup_colors():


    global PRIMARY
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    PRIMARY = curses.color_pair(1)

    global SECONDARY
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    SECONDARY = curses.color_pair(2)
    
    global TERTIARY
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    TERTIARY = curses.color_pair(3)

def main(stdscr):

    global shift_mod_a
    global shift_mod_b

    global bpm
    global outport
    outport = None

    # CURSES SETUP
    setup_colors()
    stdscr.keypad(True)     # Get better input names
    stdscr.nodelay(True)    # Don't wait for input, don't delay it
    curses.curs_set(0)      # Hide CLI cursor, this project uses a custom cursor

    draw_intro(stdscr)      # Play animated Intro

    load_state(autoload=True)   # Load 'savestate.json'

    # This keeps the app running 
    while True:                 
        
        # is_dirty get set everytime an input changes the screen
        if is_dirty:           
            stdscr.erase()
        
        # make sure that the songs bpm equals the bpm from the config data
        if bpm != config_data[0][0][1]:    
            bpm = config_data[0][0][1]

        # Make sure to setup a Midiport
        if outport == None or MIDI_PORT != config_data[0][0][0]:
            MIDI_PORT = config_data[0][0][0]
            try:
                available_ports = mido.get_input_names()
                if MIDI_PORT >= len(available_ports):
                    MIDI_PORT = 0
                    config_data[0][0][0] = 0
                outport = mido.open_output(available_ports[MIDI_PORT])
            
            except:
                outport = None
            
            stdscr.clear()

        # draw global infos, these are always on screen.
        stdscr.addstr(0,2,f"BPM:{bpm} | Device: {available_ports[MIDI_PORT][0:24]}")   # BPM and Midi port

        # blinking dot to show that the program is working
        if is_song_playing:
            if phrase_step % 2 == 0:
                stdscr.addstr(2,0, "  ", curses.A_REVERSE | shift_mod_color)
            else:
                stdscr.addstr(2,0, "  ", )
        else:
            stdscr.addstr(2,0, "  ", )

        # draw Playback info of song, chain and phrase step
        draw_step_info(stdscr,STEP_INFO_Y,STEP_INFO_X)                          


        # different screens are selected and only the current screen is drawn
        if current_screen == 0:
            # SONG VIEW
            # Header
            
            stdscr.addstr(1,2,f"{SCREENS[current_screen]} {current_song:02}      ")
            stdscr.addstr(TABLE_HEADER_Y,TABLE_HEADER_X,f"{HEADER_STRING}",curses.A_REVERSE | shift_mod_color)
            
            # DATA
            channels = MAX_CHANNELS
            steps = MAX_SONG_STEPS
            update_input(stdscr,song_data,channels,steps,large_step=10)
            draw_column_no(stdscr,steps,song_step)
            draw_data(stdscr,song_data,channels,steps)
            draw_help(HELP_TEXT_SONG)
        elif current_screen == 1:
            # CHAIN VIEW
            # Header
            stdscr.addstr(1,2,f"{SCREENS[current_screen]} {current_chain:02}      ")
            stdscr.addstr(TABLE_HEADER_Y,TABLE_HEADER_X,f"PhrsTrsp",curses.A_REVERSE | shift_mod_color)
            stdscr.addstr("                          ")

            # DATA
            channels = MAX_CHAIN_PARAMETERS
            steps = MAX_CHAIN_STEPS
            update_input(stdscr,chain_data,channels,steps,large_step=10)
            draw_column_no(stdscr,steps,chain_step)
            draw_data(stdscr,chain_data,channels,steps,render_style=['int','int'])
            draw_help(HELP_TEXT_CHAIN)
        elif current_screen == 2:
            # PHRASE VIEW
            # Header
            stdscr.addstr(1,2,f"{SCREENS[current_screen]} {current_phrase:02}      ")
            stdscr.addstr(TABLE_HEADER_Y,TABLE_HEADER_X,f"Note MOD▒▒▒▒ PC ▒▒▒▒ CC ▒▒▒▒",curses.A_REVERSE | shift_mod_color)
            

            # DATA
            channels = MAX_PHRASE_PARAMETERS
            steps = MAX_PHRASE_STEPS
            update_input(stdscr,phrase_data,channels,steps)
            draw_column_no(stdscr,steps,phrase_step)
            draw_data(stdscr,phrase_data,channels,steps,render_style=['tet','mod','int','int','int','int','int'])
            draw_help(HELP_TEXT_PHRASE)

        elif current_screen == 3:
            # CONFIG VIEW
            # Header            
            stdscr.addstr(1,2,f"{SCREENS[current_screen]}    ")
            stdscr.addstr(TABLE_HEADER_Y,TABLE_HEADER_X,f"Value:     Settings      ",curses.A_REVERSE | shift_mod_color)

            # DATA
            channels = 1
            steps = MAX_CONFIG_STEPS
            update_input(stdscr,config_data,channels,steps,max_value=512,large_step=10)
            draw_column_no(stdscr,steps,99)

            draw_data(stdscr,config_data,channels,steps,render_style=['int'])
            draw_help(HELP_TEXT_CONFIG)

            stdscr.addstr(TABLE_HEADER_Y+1,TABLE_HEADER_X+6,"Midi Device")
            stdscr.addstr(TABLE_HEADER_Y+2,TABLE_HEADER_X+6,"Beats per Minute")
            stdscr.addstr(TABLE_HEADER_Y+3,TABLE_HEADER_X+6,"Groove/Swing")
            stdscr.addstr(TABLE_HEADER_Y+4,TABLE_HEADER_X+6,"Disable Autosaving")

            stdscr.refresh()

        else:
            # fallback in case a non available screen number gets selected error happens
            pass
        
        if is_song_playing:
            play_song(0,stdscr)


        if shift_mod_a:
            stdscr.addstr(STEP_INFO_Y+4,STEP_INFO_X,f"-> Mod1 ", PRIMARY | curses.A_REVERSE)
        else:
            stdscr.addstr(STEP_INFO_Y+4,STEP_INFO_X,f"  Mod1  ")
        
        if shift_mod_b:
            stdscr.addstr(STEP_INFO_Y+5,STEP_INFO_X,f"-> Mod2 ", SECONDARY | curses.A_REVERSE)
        else:
            stdscr.addstr(STEP_INFO_Y+5,STEP_INFO_X,f"  Mod2  ")

        stdscr.refresh()

# Make sure that the app is only executed as script
if __name__ == "__main__":
    wrapper(main)

