from machine import Pin
import utime

class Motor:
    def __init__(self, controlPins):
        self.pinEN = Pin(controlPins[0],Pin.OUT)
        self.pinSTEP = Pin(controlPins[1],Pin.OUT)
        self.pinDIR = Pin(controlPins[2],Pin.OUT)

        self.stepsPerRevolution = 200
        self.resolution = 1/16

        self.Enable() 

    def Enable(self):
        self.pinEN.value(0)
    
    def Disable(self):
        self.pinEN.value(1)

    def Step(self, steps=0, delay=0):
        for i in range(steps):
            self.pinSTEP.value(1)
            #utime.sleep_us(delay)
            self.pinSTEP.value(0)
            #utime.sleep_us(delay)