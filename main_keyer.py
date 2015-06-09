#!/usr/bin/env python3

import os, sys, time, random, threading, queue, json
from housepy import osc, config, log, animation

osc.verbose = False

sender = osc.Sender(config['oscpin'], 23232)

time.sleep(1)

ctx = animation.Context(100, 100)
def on_mouse_press(data):
    print("ON")
    sender.send("/noteon", 3)
def on_mouse_release(data):
    print("OFF")
    sender.send("/noteoff", 3)
ctx.add_callback("mouse_press", on_mouse_press)
ctx.add_callback("mouse_release", on_mouse_release)
ctx.start(lambda: True)

