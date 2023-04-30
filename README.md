```

        ___ ___ __    __ __ _______                 __               
 .---.-|   V   |__.--|  |__|       .----.---.-.----|  |--.-----.----.
 |  _  |.      |  |  _  |  |.|   | |   _|  _  |  __|    <|  -__|   _|
 |___._|. \_/  |__|_____|__`-|.  |-|__| |___._|____|__|__|_____|__|  
       |:  |   |             |:  |                                   
       |::.|:. |             |::.|                                   
       `--- ---'             `---'                                   
                                                                     
```                                 


Is a small tracker that sequences notes in a nested vertical layout. The UI is heavily inspired by LSDJ and other trackers from the past, present and future. To make it portable and useful on all kinds of plattforms I've choosen python for it with minimalist curses / ASCI user interface.

I am developing this tool for myself, but please let me know if it is useful for you, too. 

## Prerequisites

Tested with python 3.9.10. You'll need a python environment with mido, rtmidi and curses modules available.

## Documentation

aMidiTracker currently uses the first available MidiPort, this will change at one point.

Arrange your composition in song view, filling the channels with phrase chains.

Each chain can have a variable amount of phrases. (As of now only 1 phrase long chains work correct)

Phrases always consist of 16 steps, to each of these steps a musical note can be assigned. At this point in time notes are entered as numbers, with note 60 representing the middle C3.

### Keyboard Controls:
*← → ↑ ↓* : Navigation on Data Grid

Shift + *←* : -12 units / 1 Octave

Shift + *→* : +12 units / 1 Octave

Shift + *↓* : -1 unit / Semitone

Shift + *↑* : Up Arrow: +1 / Semitone



Strg + *→* :  Next Scene

Strg + *←* :  Next Scene

q : Quit


process can only be closed by the 'q' key, if there is still a "note_off" message to be sent some channles might get stuck in a "note_on" and sustain forever

# This tool is in its prototype phase: Constant updates, breaking changes, bad codebase.

### python modules used:
- MIDO for easy midi objects - https://github.com/mido/mido
- rtmidi for python - https://github.com/superquadratic/rtmidi-python
- curses for Terminal UI - 
