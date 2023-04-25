import sys
max_channels_amount = 6
current_chain = 0

#############################################
# RENDERING:                STORAGE:        #
# Amount --->               Length --->     #
# Lenght                    Amount          #
#   |                         |             #
#   V                         V             #
#############################################

# Generates empty CHAIN slots for Song 
song_data = [['' for _ in range(16)] for _ in range(6)]

# for testing purposes
# add chains to chains to song for testing    
song_data[5][9] = "00"
song_data[1][3] = "01"

# Generates chain data, there can be a variing amount of chains in a project
all_chain_data = []

# Example chain data
chain_data =  ['','01a','','','','01a','','','','','','', '','','','']     # PHRASE
      #          ['00a','','','','','','','03a','','','','', '','','','',]]    # TRANSPOSE ( TODO, ignore all transposes that do not have a phrase assigneds )

chain_data_b =  ['01b','','','','','','','02b','','','','', '','','','']     # PHRASE

# Append chains to chain data
all_chain_data.append(chain_data)
all_chain_data.append(chain_data_b)

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
        
        # look for the first occurence of '', we're going backwards!
        if song_data[channel][chains] != '':
            
            # append the index of that orrcurence to the chainlengths list
            chainlenghts.append(chains)
            # break this jumps out of the current loop and to the next channel if one is available
            break
    else:
        # if there is only  '' inside the whole array return -1
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
        
        # look for the first occurence of '', we're going backwards!
        if all_chain_data[chains][phrases] != '':
            
            # append the index of that orrcurence to the phraseslengths list
            phraseslenghts.append(phrases) 
            # break this jumps out of the current loop and to the next channel if one is available
            break
    else:
        # if there is only  '' inside the whole array return -1
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


