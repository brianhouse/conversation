#!/usr/bin/env python3

import os, sys, time, random, threading, queue, json
from housepy import osc, config, log, util
from housepy.keys import Keys

osc.verbose = False
# SIGDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "conversations"))


last_note = 0.0
paused = False
pause_threshold = 2.0


def on_message(location, address, data):
    global last_note
    note_on = address == "/noteon"
    t = float(data[1])
    last_note = time.time() # use local
    
receiver = osc.Receiver(23233, on_message)

while True:
    if time.time() - last_note > pause_threshold:   # 2 second threshold
        if not paused:
            print("pause")
            paused = True
    elif paused:
        print("unpause")
        paused = False
        pause_threshold = random.random() * 3
    time.sleep(0.02)