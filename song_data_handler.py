import sys
import time

import mido
from mido import Message

max_channels_amount = 6
current_chain = 0
global current_bar
current_bar = 0
is_song_playing = True

bpm = 156

# configure midiport
# Set up port selection / device selection for the user 
outport = mido.open_output()

# basic on of messages for sending midi on and midi off
# for channel in range(max_channels_amount):
#     note_on = channel + 90
#     note_off = channel + 80

#     msg = Message.from_hex([str(note_on), 40, 60])
#     msg_off = Message.from_hex([str(note_off), 40, 60])
#     messages_on.append(msg)
#     messages_off.append(msg_off)

#############################################
# RENDERING:                STORAGE:        #
# Amount --->               Length --->     #
# Lenght                    Amount          #
#   |                         |             #
#   V                         V             #
#############################################

# Generates empty CHAIN slots for Song 
song_data = [['--' for _ in range(16)] for _ in range(6)]

# for testing purposes
# add chains to chains to song for testing    
song_data[0][0] = "00"
song_data[0][1] = "00"
song_data[0][2] = "00"
song_data[0][3] = "00"

song_data[2][0] = "01"
song_data[2][1] = "02"
song_data[2][2] = "01"
song_data[2][3] = "01"

song_data[3][0] = "03"
song_data[3][1] = "03"
song_data[3][2] = "03"
song_data[4][3] = "03"




# Generates chain data, there can be a variing amount of chains in a project
all_chain_data = []

# Example chain data
chain_data0 =  ['00','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--']     # PHRASES
      #       ['--','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--']]    # TRANSPOSE ( TODO, ignore all transposes that do not have a phrase assigneds )

chain_data1 =  ['01','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--']      # PHRASES
chain_data2 =  ['02','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--']      # PHRASES
chain_data3 =  ['03','--','--','--','--','--','--','--','--','--','--','--','--','--','--','--']      # PHRASES



# Append chains to chain data
all_chain_data.append(chain_data0)
all_chain_data.append(chain_data1)
all_chain_data.append(chain_data2)
all_chain_data.append(chain_data3)



phrase_data0 =  ['60','--','--','--','--','--','--','--','60','--','--','--','--','--','--','--'] 
phrase_data1 =  ['--','--','--','--','90','--','--','--','--','--','--','--','90','--','--','--'] 
phrase_data2 =  ['--','--','--','99','90','--','--','90','--','--','--','--','90','--','91','92'] 
phrase_data3 =  ['--','--','28','--','--','--','28','--','--','--','28','--','--','--','28','00'] 


all_phrase_data = []
all_phrase_data.append(phrase_data0)
all_phrase_data.append(phrase_data1)
all_phrase_data.append(phrase_data2)
all_phrase_data.append(phrase_data3)



#################################
# get the longest chain length  #
#################################

# add empty chain lenghts, the loop will ad the max length of each channel to this list
chainlenghts = []

# THIS WORKS ON THE SONG DATA
# do the next operation for every channel
for channel in range(max_channels_amount):

    #go backwards through the chains elements
    for chains in range(len(song_data[channel])-1, -1, -1):
        
        # look for the first occurence of '--', we're going backwards!
        if song_data[channel][chains] != '--':
            
            # append the index of that orrcurence to the chainlengths list
            chainlenghts.append(chains)
            # break this jumps out of the current loop and to the next channel if one is available
            break
    else:
        # if there is only  '--' inside the whole array return -1
        max_chains_length = -1
# get the longest chain length
max_chains_length = max(chainlenghts)
print("max_chains_length:")
print(max_chains_length)

######################################
# get the longest chain_data length  #
######################################

# this will evalueded for current playing chain, but is implemented for all here

# THIS WORKS ON ALL_CHAIN_DATA
# go backwards through the Phrase elements in all chains return max

phraseslenghts = []
for chains in range(len(all_chain_data)):
    for phrases in range(len(all_chain_data[chains])-1, -1, -1):
        
        # look for the first occurence of '--', we're going backwards!
        if all_chain_data[chains][phrases] != '--':
            
            # append the index of that orrcurence to the phraseslengths list
            phraseslenghts.append(phrases) 
            # break this jumps out of the current loop and to the next channel if one is available
            break
    else:
        # if there is only  '--' inside the whole array return -1
        max_phrases_length = -1

max_phrases_length = max(phraseslenghts)
print("max_phrases_length:")
print(max_phrases_length)


print("Amount of chains in data:")
print(len(all_chain_data))

# debug printing without the use of curses
for channel in range(max_channels_amount):
    print(f"Channel{channel}")
    for chain_ in range(16):
        sys.stdout.write(song_data[channel][chain_])
        sys.stdout.write(" ")

    print("\n")

max_song_length = 16

global step
step = 0
print(f"Ch1Ch2Ch3Ch4Ch5Ch6")
while(is_song_playing):
    if max_phrases_length == -1:
        break

    
    for channel in range(max_channels_amount):
        if step == 0:
            sys.stdout.write(f"{song_data[channel][current_bar]} ")
            sys.stdout.flush()

        if song_data[channel][current_bar] != "--":

            note = all_phrase_data[ int(song_data[channel][current_bar]) ][ step ]
            if note != '--':
                note = int(note)
                outport.send(Message('note_on', channel=channel, note=note, velocity=120))
                time.sleep(0.01)

                outport.send(Message('note_off', channel=channel, note=note, velocity=120))
                sys.stdout.flush()

    time.sleep(60/bpm/4/2) 
        
    for channel in range(max_channels_amount):
        if song_data[channel][current_bar] != "--":

            note = all_phrase_data[ int(song_data[channel][current_bar]) ][ step ]
            if note != '--':
                note = int(note)


                outport.send(Message('note_off', channel=channel, note=note, velocity=120))
                sys.stdout.flush()
    step +=1
    if(step >= 16):
        step = 0
        current_bar += 1

        sys.stdout.write("\n")
        sys.stdout.flush()
        if current_bar >= 4: # max_song_length
            current_bar = 0
