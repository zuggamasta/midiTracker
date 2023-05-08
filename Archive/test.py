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

bpm = 60 

# scene infos
current_scene = 0

active_data = 0 
active_chain = []
active_phrase = []


# SONGS
current_song = 0
song_data = []
song0 = [[None for _ in range(16)] for _ in range(6)]
song0[0][0] = 0
song0[0][1] = 1

song0[1][0] = 1
song0[1][0] = 0

song0[5][0] = 1
song0[5][1] = 1
song0[5][2] = 1
song0[5][3] = 1




global sync_channels



song_data.append(song0)

# CHAINS
current_chain = 0
chain_data = []
chain0 = [[None for _ in range(16)] for _ in range(2)] # phrase | transpose
chain0[0][0] = 0
chain0[0][1] = 1
chain0[0][2] = 2
chain0[0][3] = 0

chain1 = [[None for _ in range(16)] for _ in range(2)] # phrase | transpose
chain1[0][0] = 2
chain1[0][1] = 1
chain1[0][2] = 2
chain1[0][3] = 2
chain1[0][4] = 2
chain1[0][5] = 1
chain1[0][6] = 2
chain1[0][7] = 2

chain_data.append(chain0)
chain_data.append(chain1)


current_phrase = 0
# PHRASES
phrase_data = []
phrase0 = [[None for _ in range(16)] for _ in range(2)] # note | CMD
phrase0[0][0] = 60

phrase1 =  [[None,None,None,None,0x5a,None,None,None,None,None,None,None,0x3c,None,0x3c,None],
            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
phrase2 =  [[None,None,None,0x40,0x5a,None,None,0x5a,None,None,None,None,0x5a,None,0x5a,0x5a],
            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
phrase3 =  [[0x3c,None,None,0x43,0x45,None,0x49,None,0x49,None,0x45,0x45,0x40,None,None,0x43],
            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]

phrase_data.append(phrase0)
phrase_data.append(phrase1)
phrase_data.append(phrase2)
phrase_data.append(phrase3)

current_config = 0
config_data = []
config=  [[0x00,None,0xff,0xab],[0x00,None,0xff,0xab] ]  
config_data.append(config)

def play_song(song):
    global song_step
    global song_data
    print(f"play_song()")
    for song_channel in range(MAX_CHANNELS):
        print(f"song_channel:{song_channel}")
        
        song_step = 0

        while song_step < 16:
            print(f"song_step:{song_step}")
            active_chain_no = song_data[song][song_channel][song_step]
            if active_chain_no !=  None:
                play_chain(active_chain_no,song_channel)
            else:
                print(f"no chain in song")
            song_step +=1


def play_chain(chain_no,channel):
    print(f"play_chain({chain_no})")
    chain_step = 0 
    while chain_step < 16:
        phrase = chain_data[chain_no][0][chain_step]        
        if phrase !=  None:
            play_phrase(phrase, channel)
        else:
            print(f"no phrase in chain")
        chain_step += 1


def play_phrase(phrase_no,channel):
    print(f"play_phrase({phrase_no}) channel({channel}) ♫ ♫ ♫ ♫")
    phrase_step = 0
    while phrase_step < 16:
        note = phrase_data[phrase_no][0][phrase_step]
        if note !=  None:
            play_note(note, channel)
        else:
            play_rest()
        phrase_step += 1 


def play_note(note, channel):
    print(f"note_on, channel:{channel}, note: {note}")
    #outport.send(Message('note_on', channel=channel, note=note, velocity=120))
    time.sleep(60/bpm/16)
    #outport.send(Message('note_off', channel=channel, note=note, velocity=120))

def play_rest():
    print(f"...rest...")
    time.sleep(60/bpm/16)


print(f"start")
play_song(song = 0)
