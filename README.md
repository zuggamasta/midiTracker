```
v0.2                                    oo          dP    oo 
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
- MIDO for easy midi objects - [github.com/mido/mido](https://github.com/mido/mido)
- rtmidi for python - [github.com/superquadratic/rtmidi-python](https://github.com/superquadratic/rtmidi-python)
- curses for Terminal UI - [docs.python.org/3/howto/curses](https://docs.python.org/3/howto/curses.html)
- cx_freeze for builds - [pypi.org/project/cx-Freeze](https://pypi.org/project/cx-Freeze/)

### Installation for beginners:
I learned how to use git and the CLI from well documented projects. Prerequisite is that you have python 3.9.10 or above, ```pip``` and ```git``` intalled. Installing the terminal git command can be achieved by installing the desktop variant.
#### Get the files
- First change directories to the parent folder where you want to store this repository, for example: ```cd /Users/YOUUSERNAME/Desktop/```. In the next step we will automatically create the folder with the name of this repository.
- We will now clone the respository to our machine ```git clone https://github.com/zuggamasta/midiTracker.git```, via the terminal. You could also download it from the github page as *.zip, but we'll do the rest in the terminal anyway.
- To verify that everything went well, you can look at your desktop and find the folder ```midiTracker```. With the terminal still open change directory to it with ```cd midiTracker``` and check if everyting went well. The terminal will echo that you don't have changes to commit.
#### setup dependencies / venv
- Change Directory to the midiTracker folder. If you haven't closed the Terminal since the last step there is nothing to do.
- We will now setup a virtual enviroment by python3 -m venv env/




![Song editor](/Documentation/screen_1.png)

## Keyboard Controls:

This is the keymap which midiTracker has preconfigured, you can change the assingment of keys in the top of the main miditracker.py file.

### Change Screens

```1``` : Song Screen

```2``` : Chain Screen

```3``` : Phrase Screen

```4``` : Config Screen

```5``` : Visualizer Screen (Press any key to leave)



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

```Space``` : Stop / Restart Song

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

