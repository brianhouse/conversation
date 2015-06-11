#!/usr/bin/env python3

import os, sys, time, random, threading, queue, json
from housepy import osc, config, log, util
from housepy.keys import Keys

osc.verbose = False

PIN = 3

last_note = float('inf')
paused = False
pause_threshold = 2.0
phrase_length = 0
max_wait = 12.0

def on_message(location, address, data):
    global last_note, phrase_length
    note_on = address == "/noteon"
    pin = int(data[0])
    t = float(data[1])
    if pin != PIN:
        last_note = time.time() # use local
        if not note_on:
            phrase_length += 1
    
receiver = osc.Receiver(23233, on_message)

sender = osc.Sender(config['oscpin'], 23232)

tap_pause = 0.3
note_pause = 0.6

def play_phrase():
    global tap_pause, note_pause, phrase_length
    log.info("Playing a phrase...")
    if phrase_length:
        notes = random.choice([phrase_length, random.randint(1, 5)])
    else:
        notes = random.randint(1, 5)
    log.info("length is %s (%s)" % (notes, phrase_length))
    for i in range(notes):
        sender.send("/noteon", PIN)
        tap_pause = (random.random() * 0.08) + 0.13 if random.random() > 0.5 else (tap_pause + (random.random() * 0.03))
        print("tap_pause", tap_pause)
        time.sleep(tap_pause)
        sender.send("/noteoff", PIN)
        note_pause = (random.random() * 0.35) + 0.13 if random.random() > 0.5 else (note_pause + (random.random() * 0.05))
        time.sleep(note_pause)
    log.info("--> done")

while True:
    if time.time() - last_note > pause_threshold:   # 2 second threshold
        if not paused:
            print("pause")
            paused = True
            play_phrase()
            phrase_length = 0
        if time.time() - last_note > max_wait:
            last_note = time.time()
    elif paused:
        print("unpause")
        paused = False
        pause_threshold = random.random() * 2
    time.sleep(0.02)