from machine import Pin
import utime

class Motor:
    def __init__(self, controlPins, stepResolution):
        self.pinEN = Pin(controlPins[0],Pin.OUT)
        self.pinSTEP = Pin(controlPins[1],Pin.OUT)
        self.pinDIR = Pin(controlPins[2],Pin.OUT)

        self.stepResolution = stepResolution

        self.degreeToStep = 200/360

        self.Enable() 

    def Enable(self):
        self.pinEN.value(0)
    
    def Disable(self):
        self.pinEN.value(1)

    def Step(self, steps=0, delay=1000):
        if steps >= 0: self.pinDIR.value(1)
        else: self.pinDIR.value(0)

        steps = abs(steps)

        for i in range(steps):
            self.pinSTEP.value(1)
            utime.sleep_us(int(delay))
            self.pinSTEP.value(0)
            utime.sleep_us(int(delay))

    def Rotate(self, degree, speed):
        for i in range((degree * self.degreeToStep) / self.stepResolution):
            if degree >= 0: self.Step(steps=1, delay=1000/speed)
            else: self.Step(steps=-1, delay=1000/speed)