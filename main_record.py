#!/usr/bin/env python3

import os, sys, time, random, threading, queue, json
from housepy import osc, config, log, util
from housepy.keys import Keys

osc.verbose = False
SIGDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "conversations"))

notes = []

sender = osc.Sender(23233) # for robot

def on_message(location, address, data):
    note_on = address == "/noteon"
    pin = int(data[0])
    t = float(data[1])
    if note_on:
        log.info("%d ON  %f" % (pin, t))
    else:
        log.info("%d OFF %f" % (pin, t))
    notes.append((t, 'A' if pin == 2 else 'B', note_on))
    sender.send(address, data)
    
receiver = osc.Receiver(23232, on_message)

def pack():
    global notes
    if not len(notes):
        log.warning("Conversation is empty")
        return
    notes_ = list(zip(*notes))       
    min_t = min(notes_[0])
    ts = [t - min_t for t in notes_[0]]
    result = list(zip(ts, notes_[1], notes_[2]))
    # print(result)
    store_convo(result)
    notes = []

def store_convo(signal):
    t = util.timestamp()
    path = os.path.join(SIGDIR, "%s.json" % t)
    log.info("Storing conversation at %s" % path)
    with open(path, 'w') as handle:
        content = json.dumps(signal, indent=4)
        print(content)
        handle.write(content)

keys = Keys()

def on_a():
    log.info("A")
def on_s():
    pack()
keys.add_callback(ord('a'), on_a)
keys.add_callback(ord('s'), on_s)

log.info("--> ready")

while True:
    try:
        time.sleep(5)
    except KeyboardInterrupt:
        keys.restore()
        break
        


