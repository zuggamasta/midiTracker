# utilities
import time
import random

# UI libs
import curses
from curses import wrapper

# midi IO libs
import rtmidi
import mido
from mido import Message

# configure midiport
# TODO: Set up port selection / device selection for the user 
outport = mido.open_output()

# basic on of messages for sending midi on and midi off
msg = Message.from_bytes([0x90, 0x40, 0x60])
msg_off = Message.from_bytes([0x80, 0x40, 0x60])

is_song_playing = True
current_song_no = 0x00
current_song_name = "Very first LmidiJ Song"
current_chain_no = 0x00
current_pattern_no = 0x00
bpm = random.randint(90, 160)	

# magic numbers these need to be removed
char_offset_channel = 3
char_offset_y = 3

# first idea for the data grid
current_song_data = [
    [0x24,"ff","99", "A3", "00", "00"],
    [0x20,"ff","99", "A3", "00", "00"],    
    [0x34,"ff","99", "A3", "00", "00"],
    [0x32,"ff","--", "A3", "00", "00"],
    [0x42,"--","--", "A3", "00", "00"],
    [0x40,"--","--", "A3", "00", "00"],
    [0x42,"--","--", "A3", "00", "00"],
    [0x40,"--","99", "A3", "00", "00"],
    [0x26,"--","99", "A3", "00", "00"]
    ]

current_chain_data = [
    [0x24,"ff"],
    [0x20,"ff"],    
    [0x34,"ff"],
    [0x32,"ff"],
    [0x42,"--"],
    [0x40,"--"],
    [0x42,"--"],
    [0x40,"--"],
    [0x26,"--"]
    ]

current_pattern_data = [
    [0x24,"ff"],
    [0x20,"ff"],    
    [0x34,"ff"],
    [0x32,"ff"],
    [0x42,"--"],
    [0x40,"--"],
    [0x42,"--"],
    [0x40,"--"],
    [0x26,"--"]
    ]
    
current_song_data.extend(current_song_data)

def main(stdscr):

    while(is_song_playing):

        for current_frame in range(0,256):
            stdscr.erase()

            frame_win = curses.newwin(17,2,3,0)

            for frame in range(16):
                frame_win.addstr(frame, 0, f"{frame:02}",curses.A_BOLD | curses.A_REVERSE)

            stdscr.addstr(f"BPM: {bpm}  |  Frame:{current_frame}")
            stdscr.addstr(2,2," Ch0 Ch1 Ch2 Ch3 Ch4 Ch5 ",curses.A_BOLD | curses.A_REVERSE)

            for channel in range(0,6):
                for row in range(0,16):
                    stdscr.addstr(row+char_offset_y, channel*4+char_offset_channel, f"{current_song_data[row][channel]:02}")
                    
                    if(current_frame%16 == row):  
                        if(0 == channel):
                            note = current_song_data[row][0]
                        
                            stdscr.addstr(row+char_offset_y, channel*3+char_offset_channel, f"{current_song_data[row][channel]:02}", curses.A_REVERSE)
                            msg = Message.from_bytes([0x94, note, 0x60])
                            msg_off = Message.from_bytes([0x84, note, 0x60])
                            outport.send(msg)

            stdscr.refresh()
            frame_win.refresh()

            time.sleep(60/bpm/4)
            outport.send(msg_off)

    stdscr.getch()

wrapper(main)

