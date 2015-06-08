#!/usr/bin/env python3

import sys, time, os
from housepy import osc, config, log, process
log.info("Starting up...")
try:
    import RPi.GPIO as GPIO
except ImportError:
    log.warning("--> using fake GPIO")
    class GPIO(object):
        BCM = 303
        OUT = "out"
        HIGH, LOW = 1, 0
        PUD_UP = None
        def setmode(n):
            pass
        def setup(n, m):
            pass
        def output(n, m):
            pass

process.secure_pid(os.path.abspath(os.path.join(os.path.dirname(__file__), "run")))  

# https://www.raspberrypi.org/documentation/usage/gpio/
log.info("Setting up pins...")
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
outputs = [2, 3, 4, 17, 27, 22, 10, 9, 11]
inputs = [14]#, 15, 18, 23, 24, 25, 8, 7]
for pin in outputs:
    log.info("--> %s output" % pin)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
for pin in inputs:
    log.info("--> %s input" % pin)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
log.info("--> done")

def on_message(location, address, data):
    pin = int(data[0])
    if address == "/noteon":
        GPIO.output(pin, 0)
    if address == "/noteoff":
        GPIO.output(pin, 1)

osc.Receiver(23232, on_message)

sender = osc.Sender(config['recorder'], 23232)
state = {pin: False for pin in inputs}
while True:
    t = time.time()
    for pin in inputs:
        if state[pin] != GPIO.input(pin):
            state[pin] = !state[pin]
            if state[pin]:
                sender.send("/noteon", [pin, t])
            else:
                sender.send("/noteoff", [pin, t])
    time.sleep(0.01)     # as fast as possible
