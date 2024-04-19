```
v0.4                                    oo          dP    oo 
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

I'm building this whole thing with python **3.9.10.** And I have close to no experience with python. You'll need a python environment with mido, rtmidi and curses modules installed.

### python modules used:
- MIDO for easy midi objects - [github.com/mido/mido](https://github.com/mido/mido)
- rtmidi for python - [github.com/superquadratic/rtmidi-python](https://github.com/superquadratic/rtmidi-python)
- curses for Terminal UI - [docs.python.org/3/howto/curses](https://docs.python.org/3/howto/curses.html)
- cx_freeze for builds - [pypi.org/project/cx-Freeze](https://pypi.org/project/cx-Freeze/)

For artists, beginners or other curious folk you can [read the installation guide here if you want help getting started](https://github.com/zuggamasta/midiTracker/wiki/Installing-midiTracker-(Beginner-Friendly)). I also tried to explain some basic info on how to use command line git to clone a repository for a workflow where you do not need to leave your terminal.

```

    SONG 00                                   ┌───────────────┐
    Chn1Chn2Chn3Chn4RmplChn6Chn7Chn8          │       BPM: 120│
  00 --  --  --  --  --  --  --  --           │IAC-Treiber … 1│
  01 --  --  --  --  --  --  --  --           │               │
  02 --  --  --  --  --  --  --  --           │               │
  03 --  --  --  --  --  --  --  --           │Song Step:   00│
  04 --  --  --  --  --  --  --  --           │Chain Step:  01│
  05 --  --  --  --  --  --  --  --           │Phrase Step: 10│
  06 --  --  --  --  --  --  --  --           │               │
  07 --  --  --  --  --  --  --  --           │Loop Length: 08│
  08 --  --  --  --  --  --  --  --           │               │
  09 --  --  --  --  --  --  --  --           │               │
  10 --  --  --  --  --  --  --  --           │  Mod1         │
  11 --  --  --  --  --  --  --  --           │  Mod2         │
  12 --  --  --  --  --  --  --  --           │               │
  13 --  --  --  --  --  --  --  --           │               │
  14 --  --  --  --  --  --  --  --           │               │
  15 --  --  --  --  --  --  --  --           └───────────────┘

```
## Keyboard Controls:

This is the keymap which midiTracker has preconfigured, you can change the assingment of keys in the top of the main miditracker.py file.

### Change Screens

```Number Keys 1 - 5``` :  Brings you to the different screens. In the order Song, Chain, Phrase, Confing, Visualizer.

### Move the cursor:

```Arrow Keys ← → ↑ ↓``` : Navigation on Data Grid

### Edit notes:

```a``` : Modifier 1 (Screen highlights in green)

&emsp; ```Mod1 + ←``` : -12 units / 1 Octave

&emsp; ```Mod1 + →``` : +12 units / 1 Octave

&emsp; ```Mod1 + ↓``` : -1 unit / Semitone

&emsp; ```Mod1 + ↑``` : +1 / Semitone

&emsp; ```c``` : copy value

&emsp; ```shift + c``` : deep copy, copies the current phrase content 

&emsp; ```v``` : paste value

&emsp; ```shift + v``` : flood value, writes copy buffer to all steps or deep copy buffer if one is available

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


## More Screenshots

![A screenshot of miditracker in action, showing the phrase editor](/Documentation/screen_2.png)

![Chain editor](/Documentation/screen_3.png)


## Thank you
Thank you to everyone helping and making all of this possible. Thank you Mirjam, Thank you Fiona, thank you Sylt, thank you Markus.


## ⚠️ ⚠️ ⚠️ Use at your own risk ⚠️ ⚠️ ⚠️
I am developing this tool for myself, but I'll try to make it accessible to other artists and everyone curious along the way.

