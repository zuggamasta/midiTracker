```


                                        oo          dP    oo 
                                                    88       
                          88d8b.d8b.    dP    .d888b88    dP 
                          88'`88'`88    88    88'  `88    88 
                          88  88  88    88    88.  .88    88 
                          dP  dP  dP    dP    `88888P8    dP  
                                                                       
  dP                              dP                         
  88                              88                         
d8888P 88d888b. .d8888b. .d8888b. 88  .dP  .d8888b. 88d888b. 
  88   88'  `88 88'  `88 88'  `"" 88888"   88ooood8 88'  `88 
  88   88       88.  .88 88.  ... 88  `8b. 88.  ... 88       
  dP   dP       `8888'P8 `88888P' dP   `YP `88888P' dP       
                                                             
                                                                  
```                                 


aMidiTracker is a small tracker that sequences notes in a nested vertical layout. The UI is heavily inspired by LSDJ and other trackers from the past, present and future. To make it portable and useful on all kinds of plattforms I've choosen python for it with minimalist curses / ASCI user interface.

I am developing this tool for myself, but I'll try to make it accessible to other artists and everyone curious along the way.

## Screenshots

![screenshot](/Documentation/Screenshot_2023-05-02.png)


## Prerequisites

I'm building this whole thing with python 3.9.10. And I have close to no experience with python. You'll need a python environment with mido, rtmidi and curses modules installed.

## Documentation / Issues




### Keyboard Controls:
*← → ↑ ↓* : Navigation on Data Grid

Shift + *←* : -12 units / 1 Octave

Shift + *→* : +12 units / 1 Octave

Shift + *↓* : -1 unit / Semitone

Shift + *↑* : Up Arrow: +1 / Semitone



Ctrl + *→* :  Next Scene

Ctrl + *←* :  Next Scene


Space : Panic / Restart

s : Save

q : Quit


### Saving / Loading
You can save the current state of your file with the 's' button. Files will have this format ```230509-21-55.json```and will be saved next to your midipython.py file. If you want to load a state use ```miditracker.py -load yoursavefile.json```to do so.

### PANIC / STOP ALL NOTES / RESTART
Use the space key to stop all playing midi channels and notes. This also restarts playback.

### Quitting
process can only be closed by the 'q' key, if there is still a "note_off" message to be sent some channles might get stuck in a "note_on" and sustain forever

### Diagrams to keep my work organised
![data diagram](/Documentation/diagram_230501.png)

# This tool is in its prototype phase

### python modules used:
- MIDO for easy midi objects - https://github.com/mido/mido
- rtmidi for python - https://github.com/superquadratic/rtmidi-python
- curses for Terminal UI - https://docs.python.org/3/howto/curses.html
