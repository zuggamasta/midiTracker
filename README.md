```

        ___ ___ __    __ __ _______                 __               
 .---.-|   V   |__.--|  |__|       .----.---.-.----|  |--.-----.----.
 |  _  |.      |  |  _  |  |.|   | |   _|  _  |  __|    <|  -__|   _|
 |___._|. \_/  |__|_____|__`-|.  |-|__| |___._|____|__|__|_____|__|  
       |:  |   |             |:  |                                   
       |::.|:. |             |::.|                                   
       `--- ---'             `---'                                   
                                                                     
```                                 


aMidiTracker is a small tracker that sequences notes in a nested vertical layout. The UI is heavily inspired by LSDJ and other trackers from the past, present and future. To make it portable and useful on all kinds of plattforms I've choosen python for it with minimalist curses / ASCI user interface.

I am developing this tool for myself, but I'll try to make it accessible to other artists and everyone curious along the way.

## Screenshots

![screenshot](/Documentation/Screenshot_2023-05-02.png)
![screenshot](/Documentation/Screenshot_2023-05-02b.png)


## Prerequisites

I'm building this whole thing with python 3.9.10. And I have close to no experience with python. You'll need a python environment with mido, rtmidi and curses modules available.

## Documentation / Issues

- [ ] https://github.com/zuggamasta/midiTracker/issues/2 aMidiTracker currently uses the first available MidiPort, this will change at one point.

- [ ] https://github.com/zuggamasta/midiTracker/issues/3 Arrange your composition in song view, filling the channels with phrase chains. Each chain can have a variable amount of phrases. (As of now only 1 phrase long chains work correct)

- [ ] https://github.com/zuggamasta/midiTracker/issues/6 Phrases always consist of 16 steps, to each of these steps a musical note can be assigned. At this point in time notes are entered as numbers, with note 60 representing the middle C3.

### Keyboard Controls:
*← → ↑ ↓* : Navigation on Data Grid

Shift + *←* : -12 units / 1 Octave

Shift + *→* : +12 units / 1 Octave

Shift + *↓* : -1 unit / Semitone

Shift + *↑* : Up Arrow: +1 / Semitone



Ctrl + *→* :  Next Scene

Ctrl + *←* :  Next Scene

q : Quit


process can only be closed by the 'q' key, if there is still a "note_off" message to be sent some channles might get stuck in a "note_on" and sustain forever

### Diagrams to keep my work organised
![data diagram](/Documentation/diagram_230501.png)

# This tool is in its prototype phase

### python modules used:
- MIDO for easy midi objects - https://github.com/mido/mido
- rtmidi for python - https://github.com/superquadratic/rtmidi-python
- curses for Terminal UI - 
