import os
from machine import Pin, UART
import utime
import sys

class Machine:
    def __init__(self, motors):
        self.gantry = Gantry([motors[0], motors[1]])
        self.serial = Serial()

        self.systemFrequency = 60
    


class Serial:
    def __init__(self):
        self.serial0 = UART(1, baudrate=115200, tx=Pin(0), rx=Pin(1))

        self.led = Pin("LED", Pin.OUT)

    def Read(self, serialPort):
        if serialPort.any():
            data = serialPort.read().decode('utf-8').strip()
            self.led.toggle()
            utime.sleep(1)
            self.led.toggle()
            return data
    
    def Write(self, serialPort):
        serialPort.write("Hello World".encode('utf-8'))



class Gantry:
    def __init__(self, motors):
        self.motors = motors

        self.stepsPerRevolution = 200
        self.resolution = 1/16
        self.beltStepPerRevolution = 36
        self.beltStepLength = 2
        self.mmPerStep = (self.beltStepPerRevolution * self.beltStepLength) / (self.stepsPerRevolution / self.resolution)
        self.stepDelay = 0

        self.errorRate = 0.5

        self.Kp = 1
        self.Kd = 0

        self.zeroX = Pin(16, Pin.IN, Pin.PULL_DOWN)
        self.zeroY = Pin(17, Pin.IN, Pin.PULL_DOWN)

        self.x = 0
        self.y = 0

    def Enable(self):
        self.motors[0].Enable()
        self.motors[1].Enable()

    def Disable(self):
        self.motors[0].Disable()
        self.motors[1].Disable()

    def MoveX(self, toX):
        if toX - self.x >= 0: 
            direction = 1
            self.motors[0].pinDIR.value(direction)
            self.motors[1].pinDIR.value(direction)
        else:
            direction = 0
            self.motors[0].pinDIR.value(direction)
            self.motors[1].pinDIR.value(direction)

        while abs(toX - self.x) >= self.mmPerStep*self.errorRate:
            self.motors[0].Step()
            self.motors[1].Step()

            if direction == 1: self.x += self.mmPerStep
            elif direction == 0: self.x -= self.mmPerStep

    def MoveY(self, toY):
        if toY - self.y >= 0: 
            direction = 1
            self.motors[0].pinDIR.value(1)
            self.motors[1].pinDIR.value(0)
        else:
            direction = 0
            self.motors[0].pinDIR.value(0)
            self.motors[1].pinDIR.value(1)

        while abs(toY - self.y) >= self.mmPerStep*self.errorRate:
            self.motors[0].Step()
            self.motors[1].Step()
            
            if direction == 1: self.y += self.mmPerStep
            elif direction == 0: self.y -= self.mmPerStep

    def Move(self, position, delay):
        while abs(position[0] - self.x) >= self.mmPerStep or abs(position[1] - self.y) >= self.mmPerStep:
            if abs(position[0] - self.x) >= self.mmPerStep:
                if position[0] - self.x >= 0: 
                    self.MoveX(self.x + self.mmPerStep)
                else:
                    self.MoveX(self.x - self.mmPerStep)
            
            if abs(position[1] - self.y) >= self.mmPerStep:
                if position[1] - self.y >= 0: 
                    self.MoveY(self.y + self.mmPerStep)
                else:
                    self.MoveY(self.y - self.mmPerStep)
            utime.sleep_us(delay)



class Motor:
    def __init__(self, controlPins):
        self.pinEN = Pin(controlPins[0],Pin.OUT)
        self.pinSTEP = Pin(controlPins[1],Pin.OUT)
        self.pinDIR = Pin(controlPins[2],Pin.OUT)

        self.stepsPerRevolution = 200
        self.resolution = 1/16

    def Enable(self):
        self.pinEN.value(0)
    
    def Disable(self):
        self.pinEN.value(1)

    def Step(self, steps=0, delay=0):
        self.pinSTEP.value(1)
        self.pinSTEP.value(0)