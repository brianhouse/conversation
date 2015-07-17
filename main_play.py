#!/usr/bin/env python3

import os, sys, time, random, threading, queue, json
from housepy import osc, config, log

osc.verbose = False
SIGDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "conversations"))

def retrieve_convo(filename):
    try:        
        if filename is None:
            signal_files = [f for f in os.listdir(SIGDIR) if f[-4:] == "json"]
            path = os.path.join(SIGDIR, random.choice(signal_files))
        else:
            path = os.path.join(SIGDIR, filename)
        print("Loading conversation data from %s..." % path)
        with open(path, 'r') as handle:
            content = handle.read()
            signal = json.loads(content)
    except Exception as e:
        log.error(log.exc(e))
        exit()
    return signal    


def main():

    filename = sys.argv[1] if len(sys.argv) > 1 else None
    notes = retrieve_convo(filename)

    # normalize
    min_t = notes[0][0]
    for note in notes:
        note[0] -= min_t

    sender = osc.Sender(config['oscpin'], 23232)

    for pin in (2, 3):
        sender.send("/noteoff", pin)

    time.sleep(1)

    start_t = time.time()
    i = 0
    while True:
        while time.time() - start_t < notes[i][0]:
            time.sleep(0.01)
        sender.send("/noteon" if notes[i][2] else "/noteoff", 2 if notes[i][1] == 'A' else 3)
        log.info("%s %s" % (notes[i][1], "ON " if notes[i][2] else "OFF"))
        i += 1
        if i == len(notes):
            break

    if filename is None:
        time.sleep(((random.random() * 5) + 5) * 60)    # pause between 5 and 10 minutes
        main()

main()