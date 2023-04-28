# utilities
import sys
import time

# midi libs
import mido
from mido import Message

# UI libs
import curses
from curses import wrapper


MAX_CHANNEL_AMOUNT = 6
MAX_SCREEN_LENGTH = 16
current_chain = 0

is_song_playing = True



bpm = 120

# configure midiport
# Set up port selection / device selection for the user 
outport = mido.open_output()

#############################################
# RENDERING:                STORAGE:        #
# Amount --->               Length --->     #
# Lenght                    Amount          #
#   |                         |             #
#   V                         V             #
#############################################

# Generates empty CHAIN slots for Song 
song_data = [[None for _ in range(16)] for _ in range(6)]

# for testing purposes
# add chains to chains to song for testing    
song_data[0][0] = 0x00
song_data[0][1] = 0x00
song_data[0][2] = 0x01
song_data[0][3] = 0x04

song_data[2][0] = 0x01
song_data[2][1] = 0x02
song_data[2][2] = 0x01
song_data[2][3] = 0x01

song_data[3][0] = 0x02
song_data[3][1] = 0x02
song_data[3][2] = 0x04
song_data[4][3] = 0x02
song_data[4][6] = 0x02

song_data[1][0] = 0x04
song_data[1][1] = 0x04
song_data[1][2] = 0x00
song_data[1][3] = 0x04
song_data[1][4] = 0x04
song_data[1][5] = 0x04


song_data[1][7] = 0x04




# Generates chain data, there can be a variing amount of chains in a project
chain_data = []

# Example chain data
chain0 =  [0x00,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]     # PHRASES
      #       [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]    # TRANSPOSE ( TODO, ignore all transposes that do not have a phrase assigneds )

chain1 =  [0x01,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]      # PHRASES
chain2 =  [0x02,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]      # PHRASES
chain3 =  [0x02,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]      # PHRASES
chain4 =  [0x04,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]      # PHRASES



# Append chains to chain data
chain_data.append(chain0)
chain_data.append(chain1)
chain_data.append(chain2)
chain_data.append(chain3)
chain_data.append(chain4)



phrase_data = []

phrase0 =  [0x3c,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None] 
phrase1 =  [None,None,None,None,0x5a,None,None,None,None,None,None,None,0x3c,None,0x3c,None] 
phrase2 =  [None,None,None,0x40,0x5a,None,None,0x5a,None,None,None,None,0x5a,None,0x5a,0x5a] 
phrase3 =  [None,None,0x30,None,None,None,0x30,None,None,None,0x30,None,None,None,0x30,None] 
phrase4 =  [0x3c,None,None,0x43,0x45,None,0x49,None,0x49,None,0x45,0x45,0x40,None,None,0x43] 

phrase_data.append(phrase0)
phrase_data.append(phrase1)
phrase_data.append(phrase2)
phrase_data.append(phrase3)
phrase_data.append(phrase4)




#################################
# get the longest chain length  #
#################################

# add empty chain lenghts, the loop will ad the max length of each channel to this list

# THIS WORKS ON THE SONG DATA
# do the next operation for every channel
def get_max_chains_length():
    chainlenghts = []
    for channel in range(MAX_CHANNEL_AMOUNT):

        #go backwards through the chains elements
        for chains in range(len(song_data[channel])-1, -1, -1):
            
            # look for the first occurence of None, we're going backwards!
            if song_data[channel][chains] != None:
                
                # append the index of that orrcurence to the chainlengths list
                chainlenghts.append(chains)
                # break this jumps out of the current loop and to the next channel if one is available
                break
        else:
            # if there is only  None inside the whole array return -1
            max_chains_length = -1
    # get the longest chain length
    max_chains_length = max(chainlenghts)
    # print('max_chains_length:')
    #print(max_chains_length)
    return max_chains_length

######################################
# get the longest chain_data length  #
######################################

# this will evalueded for current playing chain, but is implemented for all here

# THIS WORKS ON chain_data
# go backwards through the Phrase elements in all chains return max

phraseslenghts = []
for chains in range(len(chain_data)):
    for phrases in range(len(chain_data[chains])-1, -1, -1):
        
        # look for the first occurence of None, we're going backwards!
        if chain_data[chains][phrases] != None:
            
            # append the index of that orrcurence to the phraseslengths list
            phraseslenghts.append(phrases) 
            # break this jumps out of the current loop and to the next channel if one is available
            break
    else:
        # if there is only  None inside the whole array return -1
        max_phrases_length = -1

max_phrases_length = max(phraseslenghts)
print('max_phrases_length:')
print(max_phrases_length)

print('Amount of chains in data:')
print(len(chain_data))

""" def main(stdscr):

    stdscr.keypad(True)
    stdscr.nodelay(True)
    for column in range(MAX_SCREEN_LENGTH):
        for row in range(MAX_CHANNEL_AMOUNT):
            stdscr.addstr(f"{song_data[row][column]}")

    stdscr.refresh()
    stdscr.getch()
    
wrapper(main)
 """



def playSong():
    global current_step
    current_step = 0

    global current_bar
    current_bar = 0


    while(is_song_playing):
            
        global last_notes


        last_notes = [None,None,None,None,None,None]


        if max_phrases_length == -1:
            break

        
        for channel in range(MAX_CHANNEL_AMOUNT):

            # debug_draw_current_chain(channel)

            
            if song_data[channel][current_bar] != None:
                
                note = phrase_data[ int(song_data[channel][current_bar]) ][ current_step ]
                
                last_notes[channel] = note

                if note != None:
                    note = int(note)
                    outport.send(Message('note_on', channel=channel, note=note, velocity=120))

                    # sys.stdout.write(f'{note} ')
                    # sys.stdout.flush()
                else:
                    # sys.stdout.write(f'-- ')
                    pass
            else:
                # sys.stdout.write(f'-- ')
                pass

        time.sleep(60/bpm/8) 

        for channel in range(MAX_CHANNEL_AMOUNT):
            if song_data[channel][current_bar] != None:

                note = last_notes[channel]
                if note != None:
                    

                    outport.send(Message('note_off', channel=channel, note=note, velocity=120))
                    #sys.stdout.flush()

            
        
        current_step +=1
        if(current_step >= 16):
            current_step = 0
            current_bar += 1

            if current_bar >= get_max_chains_length(): # MAX_SCREEN_LENGTH
                current_bar = 0

def debug_draw_current_chain(channel):
    if current_step == 0:
        sys.stdout.write(f'{song_data[channel][current_bar]} ')
        sys.stdout.flush()
        pass


playSong()