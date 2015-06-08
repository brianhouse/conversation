import sys, time, random, threading, queue
from housepy import osc, config, log

osc.verbose = False

sender = osc.Sender(config['oscpin'], 23232)

pins = [2, 3, 4, 17, 27, 22, 10, 9, 11]

for pin in pins:
    sender.send("/noteoff", pin)

