#!/usr/bin/env python3

import sys, time, random, threading, queue
import signal_processing as sp
from housepy import osc, config, log
from housepy.keys import Keys

osc.verbose = False

A, B = [], []

def on_message(location, address, data):
    log.debug(data)
    if address == "/noteon":
        pin = int(data[0])
        t = float(data[1])
        if pin == 14:
            A.append(t)
        elif pin == 15:
            B.append(t)
    
receiver = osc.Receiver(23232, on_message)

def pack():
    global A, B
    if not len(A) or not len(B):
        log.warning("One or both voices is empty")
        return
    minimum = min(min(A), min(B))
    maximum = max(max(A), max(B))
    A = sp.normalize(A, minimum, maximum)
    B = sp.normalize(B, minimum, maximum)
    result = A, B
    log.info(result)
    A, B = [], []

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
        


