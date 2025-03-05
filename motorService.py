from machine import Pin
from time import sleep

usleep = lambda x: sleep(x/1000000.0)

class Motor:
    def __init__(self, controlPins):
        self.EN = Pin(controlPins[0],Pin.OUT)
        self.STEP = Pin(controlPins[1],Pin.OUT)
        self.DIR = Pin(controlPins[2],Pin.OUT)   

    def Step(self, steps, delay):
        for i in range(steps):
            self.STEP.value(1)
            usleep(delay)
            self.STEP.value(0)
            usleep(delay)