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


aMidiTracker is a small tracker that sequences notes in a nested vertical layout. The UI is heavily inspired by LSDJ and other trackers from the past, present and future. To make it portable and useful on all kinds of plattforms I've choosen python for it with minimalist curses / ASCII user interface.


## Running midiTracker

I'm building this whole thing with python 3.9.10. And I have close to no experience with python. You'll need a python environment with mido, rtmidi and curses modules installed.

### python modules used:
- MIDO for easy midi objects - https://github.com/mido/mido
- rtmidi for python - https://github.com/superquadratic/rtmidi-python
- curses for Terminal UI - https://docs.python.org/3/howto/curses.html

![Song editor](/Documentation/screen_1.png)

## Keyboard Controls:

This is the keymap which midiTracker has preconfigured, you can change the assingment of keys in the top of the main miditracker.py file.

### Change Screens

```1``` : Song Screen

```2``` : Chain Screen

```3``` : Phrase Screen

```4``` : Config Screen


### Move the cursor:

```Arrow Keys ← → ↑ ↓``` : Navigation on Data Grid

### Edit notes:

```a``` : Modifier 1 (Screen highlights in green)

&emsp; ```Mod1 + ←``` : -12 units / 1 Octave

&emsp; ```Mod1 + →``` : +12 units / 1 Octave

&emsp; ```Mod1 + ↓``` : -1 unit / Semitone

&emsp; ```Mod1 + ↑``` : +1 / Semitone

&emsp; ```c``` : copy value

&emsp; ```v``` : paste value

&emsp; ```shift + v``` : flood value, writes copy buffer to all steps

### Change Chains and Phrases:

```s``` : Modifier 2 (Screen highlights in yellow/orange)

&emsp; ```Mod2 + ↓``` : View next Phrase or Chain

&emsp; ```Mod2 + ↑``` : View last Phrase or Chain

&emsp; *The arrows for switching between chains and phrases are fipped as it made more sense for me. Makes it feel like there is a wheel you scroll through to get to the element you're looking for.* 

### Other controls:

```w``` : Panic (stops all Midi Messages)

```Space``` : Panic / Restart Song

```Shift + s``` : Save

```Shift + q``` : Quit


## Saving / Loading

Miditracker automatically saves your file when you quit a session with ```shift ü q``` button. This save is available in ```savestate.json``` and will always be overwritten you quit a session.

You can save the current state of your file with the ```shift + s``` combination. Files will have this format ```230509-21-55.json```and will be saved next to your midipython.py file. If you want to load a state use:

```miditracker.py -load yoursavefile.json```

## PANIC / STOP ALL NOTES / RESTART
Use the ```space``` key to stop all playing midi channels and notes. This also restarts playback.

## Quitting
process can be closed with ```shift + q``` .

## More Screenshots

![A screenshot of miditracker in action, showing the phrase editor](/Documentation/screen_2.png)

![Chain editor](/Documentation/screen_3.png)


## Thank you
Thank you to everyone helping and making all of this possible. Thank you Mirjam, Thank you Fiona, thank you Sylt, thank you Markus.


## ⚠️ ⚠️ ⚠️ Use at your own risk ⚠️ ⚠️ ⚠️
I am developing this tool for myself, but I'll try to make it accessible to other artists and everyone curious along the way.

