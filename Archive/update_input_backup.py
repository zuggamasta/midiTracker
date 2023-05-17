def update_input(scr,data,max_column,max_row):
    global song_step
    global chain_step
    global phrase_step
    global cursor
    global current_screen
    global current_song
    global current_chain
    global current_phrase
    global current_config
    global active_data
    global is_dirty

    is_dirty = True

    try:
        key = scr.getkey()
    except:
        key = None
        is_dirty = False

    if current_screen == 0:
        active_data = current_song
    elif current_screen == 1:
        active_data = current_chain
    elif current_screen == 2:
        active_data = current_phrase
    elif current_screen == 3:
        active_data == current_config

    if key == "1":
        current_screen = 0
    elif key == "2":
        current_screen = 1
    elif key == "3":
        current_screen = 2
    elif key == "4":
        current_screen = 3
    elif key == "5":
        current_screen = 4

     # SWITCH CHAIN / SONG / PHRASE  kUP5 kDN5
    elif key == "kUP5":
        # CHAIN SCENE
        if current_screen == 1:
            if current_chain+2 > len(chain_data) :
                chain_data.append([[None for _ in range(MAX_CHAIN_STEPS)] for _ in range(2)])
            current_chain += 1
        # PHRASE SCENE
        if current_screen == 2:
            if current_phrase+2 > len(phrase_data) :
                phrase_data.append([[None for _ in range(MAX_PHRASE_STEPS)] for _ in range(2)])
            current_phrase += 1
        
    elif key == "kDN5":
        # CHAIN SCENE
        if current_screen == 1:
            current_chain -= 1
            if current_chain < 0:
                current_chain = 0

        # PHRASE SCENE
        if current_screen == 2:
            current_phrase -= 1
            if current_phrase < 0:
                current_phrase = 0
 
    elif key == "w":
        panic()

    elif key == " ":
        panic()
        song_step = 0
        chain_step = 0
        phrase_step = 0
        global current_notes
        global last_notes
        current_notes = [None for _ in range(MAX_CHANNELS)]
        last_notes = [None for _ in range(MAX_CHANNELS)]
    
    elif key == "s":
        save_state()

    # MODIFY DATA
    elif key == "KEY_SR":
        if data[active_data][cursor[0]][cursor[1]] == None:
            data[active_data][cursor[0]][cursor[1]] = 0x0
        else:
            data[active_data][cursor[0]][cursor[1]] += 0x1
    elif key == "KEY_SF":
        if data[active_data][cursor[0]][cursor[1]] == None:
            data[active_data][cursor[0]][cursor[1]] = 0x0
        else:
            data[active_data][cursor[0]][cursor[1]] -= 0x1
    elif key == "KEY_SRIGHT":
        if data[active_data][cursor[0]][cursor[1]] == None:
            data[active_data][cursor[0]][cursor[1]] = 0x0
        else:
            data[active_data][cursor[0]][cursor[1]] += 12
    elif key == "KEY_SLEFT":
        if data[active_data][cursor[0]][cursor[1]] == None:
            data[active_data][cursor[0]][cursor[1]] = 0x0
        else:
            data[active_data][cursor[0]][cursor[1]] -= 12
    elif key == "x":
        if data[active_data][cursor[0]][cursor[1]] == None:
            pass
        else:
            data[active_data][cursor[0]][cursor[1]] = None

    # MOVE CURSOR
    elif key == "KEY_UP":
        cursor[1] -= 1
    elif key == "KEY_DOWN":
        cursor[1] += 1
    elif key == "KEY_RIGHT":
        cursor[0] += 1
    elif key == "KEY_LEFT":
        cursor[0] -= 1

    # QUIT APPLICATION

    elif key == "q":
            panic()

            save_state_data = []

            save_state_data.append(song_data)
            save_state_data.append(chain_data)
            save_state_data.append(phrase_data)
            with open(f"savestate.json", "w") as fp:
                json.dump(save_state_data, fp, indent=4)  # Use indent for a pretty-formatted JSON file
            
            sys.exit()
    else:
        pass
    
    
    # WRAP CURSOR AROUND
    if cursor[0] < 0:
        cursor[0] = max_column-1
    if cursor[1] < 0:
        cursor[1] = max_row-1
    if cursor[0] >= max_column:
        cursor[0] = 0
    if cursor[1] >= max_row:
        cursor[1] = 0

    if current_screen == 3:
        active_data = 0
        current_config = 0

    if data[active_data][cursor[0]][cursor[1]] != None:
        if data[active_data][cursor[0]][cursor[1]] < 0:
            data[active_data][cursor[0]][cursor[1]] = MAX_MIDI-1
        if data[active_data][cursor[0]][cursor[1]] > MAX_MIDI-1:
            data[active_data][cursor[0]][cursor[1]] = 0

    
    scr.refresh()

    return cursor