from machine import Pin
from time import sleep
import math

usleep = lambda x: sleep(x/1000000.0)

class Motor:
    def __init__(self, controlPins):
        self.EN = Pin(controlPins[0],Pin.OUT)
        self.STEP = Pin(controlPins[1],Pin.OUT)
        self.DIR = Pin(controlPins[2],Pin.OUT)

        self.stepResolution = 1

        self.degreeToStep = (200/360)
        self.minimumDelay = 1000

        self.Enable() 

    def GetSteps(self, degree):
        return degree*self.degreeToStep/self.stepResolution

    def Enable(self):
        self.EN.value(0)
    
    def Disable(self):
        self.EN.value(1)

    def Step(self, steps=0, delay=1000):
        if steps >= 0: self.DIR.value(1) 
        else: self.DIR.value(0)

        absSteps = abs(steps)
        
        for i in range(absSteps):
            self.STEP.value(1)
            usleep(delay)
            self.STEP.value(0)
            usleep(delay)
    
    def Rotate(self, degree=0, speed=1):
        if degree >= 0: self.DIR.value(1) 
        else: self.DIR.value(0)

        self.Step(math.floor(self.GetSteps(degree)), self.minimumDelay/speed)