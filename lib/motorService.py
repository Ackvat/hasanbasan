from machine import Pin
import utime

class Motor:
    def __init__(self, controlPins, stepResolution):
        self.pinEN = Pin(controlPins[0],Pin.OUT)
        self.pinSTEP = Pin(controlPins[1],Pin.OUT)
        self.pinDIR = Pin(controlPins[2],Pin.OUT)

        self.stepResolution = stepResolution

        self.stepsPerRevolution = 200

        self.Enable() 

    def Enable(self):
        self.pinEN.value(0)
    
    def Disable(self):
        self.pinEN.value(1)

    def Step(self, steps=0, delay=1000):
        for i in range(steps):
            self.pinSTEP.value(1)
            utime.sleep_us(int(delay))
            self.pinSTEP.value(0)
            utime.sleep_us(int(delay))