import sys
import time

import mido
from mido import Message

max_channels_amount = 6
current_chain = 0
global current_bar
current_bar = 0
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
all_chain_data = []

# Example chain data
chain_data0 =  [0x00,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]     # PHRASES
      #       [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]    # TRANSPOSE ( TODO, ignore all transposes that do not have a phrase assigneds )

chain_data1 =  [0x01,0x01,None,None,None,None,None,None,None,None,None,None,None,None,None,None]      # PHRASES
chain_data2 =  [0x02,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]      # PHRASES
chain_data3 =  [0x02,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]      # PHRASES
chain_data4 =  [0x04,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]      # PHRASES



# Append chains to chain data
all_chain_data.append(chain_data0)
all_chain_data.append(chain_data1)
all_chain_data.append(chain_data2)
all_chain_data.append(chain_data3)
all_chain_data.append(chain_data4)




phrase_data0 =  [0x3c,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None] 
phrase_data1 =  [None,None,None,None,0x5a,None,None,None,None,None,None,None,0x3c,None,0x3c,None] 
phrase_data2 =  [None,None,None,0x40,0x5a,None,None,0x5a,None,None,None,None,0x5a,None,0x5a,0x5a] 
phrase_data3 =  [None,None,0x30,None,None,None,0x30,None,None,None,0x30,None,None,None,0x30,None] 
phrase_data4 =  [0x3c,None,None,0x43,0x45,None,0x49,None,0x49,None,0x45,0x45,0x40,None,None,0x43] 



all_phrase_data = []
all_phrase_data.append(phrase_data0)
all_phrase_data.append(phrase_data1)
all_phrase_data.append(phrase_data2)
all_phrase_data.append(phrase_data3)
all_phrase_data.append(phrase_data4)




#################################
# get the longest chain length  #
#################################

# add empty chain lenghts, the loop will ad the max length of each channel to this list

# THIS WORKS ON THE SONG DATA
# do the next operation for every channel
def get_max_chains_length():
    chainlenghts = []
    for channel in range(max_channels_amount):

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

# THIS WORKS ON ALL_CHAIN_DATA
# go backwards through the Phrase elements in all chains return max

phraseslenghts = []
for chains in range(len(all_chain_data)):
    for phrases in range(len(all_chain_data[chains])-1, -1, -1):
        
        # look for the first occurence of None, we're going backwards!
        if all_chain_data[chains][phrases] != None:
            
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
print(len(all_chain_data))

# debug printing without the use of curses
for channel in range(max_channels_amount):
    #print(f'Channel{channel}')
    for chain_ in range(16):
        #sys.stdout.write(f'{song_data[channel][chain_]}')
        #sys.stdout.write(' ')
        pass
    #print('\n')
    pass

max_song_length = 16

global step
step = 0
print(f'Ch1Ch2Ch3Ch4Ch5Ch6')
while(is_song_playing):
    if max_phrases_length == -1:
        break

    
    for channel in range(max_channels_amount):
        if step == 0:
            #sys.stdout.write(f'{song_data[channel][current_bar]} ')
            #sys.stdout.flush()
            pass

        if song_data[channel][current_bar] != None:
            
            note = all_phrase_data[ int(song_data[channel][current_bar]) ][ step ]
            
            if note != None:
                note = int(note)
                outport.send(Message('note_on', channel=channel, note=note, velocity=120))

                sys.stdout.write(f'{note} ')

                time.sleep(0.001)

                outport.send(Message('note_off', channel=channel, note=note, velocity=120))
                sys.stdout.flush()
            else:
                sys.stdout.write(f'-- ')
        else:
            sys.stdout.write(f'   ')

    sys.stdout.write('\n')
    sys.stdout.flush()

    time.sleep(60/bpm/8) 
        
    for channel in range(max_channels_amount):
        if song_data[channel][current_bar] != None:

            note = all_phrase_data[ int(song_data[channel][current_bar]) ][ step ]
            if note != None:
                note = int(note)


                outport.send(Message('note_off', channel=channel, note=note, velocity=120))
                #sys.stdout.flush()
    step +=1
    if(step >= 16):
        step = 0
        current_bar += 1

        if current_bar >= get_max_chains_length(): # max_song_length
            current_bar = 0
