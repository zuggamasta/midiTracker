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


### ⚠️ This tool is in its prototype phase ⚠️

## Running midiTracker

I'm building this whole thing with python 3.9.10. And I have close to no experience with python. You'll need a python environment with mido, rtmidi and curses modules installed.

### python modules used:
- MIDO for easy midi objects - https://github.com/mido/mido
- rtmidi for python - https://github.com/superquadratic/rtmidi-python
- curses for Terminal UI - https://docs.python.org/3/howto/curses.html


### Keyboard Controls:
*← → ↑ ↓* : Navigation on Data Grid

Shift + *←* : -12 units / 1 Octave

Shift + *→* : +12 units / 1 Octave

Shift + *↓* : -1 unit / Semitone

Shift + *↑* : Up Arrow: +1 / Semitone



1 : Song View

2 : Chain View

3 : Phrase View

4 : Config View

w : Panic (stops all Midi Messages)

Space : Panic / Restart Song

s : Save

q : Quit


### Saving / Loading

Miditracker automatically saves your file when you quit a session with the ```'q'``` button. This save is available in ```savestate.json``` and will always be overwritten you quit a session.

You can save the current state of your file with the ```'s'``` button. Files will have this format ```230509-21-55.json```and will be saved next to your midipython.py file. If you want to load a state use:

```miditracker.py -load yoursavefile.json```

### PANIC / STOP ALL NOTES / RESTART
Use the ```space``` key to stop all playing midi channels and notes. This also restarts playback.

### Quitting
process can be closed by the ```'q'``` key,

## Thank you
Thank you to everyone helping and making all of this possible. I'll take care and list you all when there is a little more time to do so.
