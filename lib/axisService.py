from machine import Pin
import utime
import math

import sys
sys.path.append('/lib')

import lib.motorService as motorService

class Gantry:
    def __init__(self, motors):
        self.motors = motors

        self.stepsPerRevolution = 200
        self.resolution = 1/16
        self.beltStepPerRevolution = 36
        self.beltStepLength = 2
        self.mmPerStep = (self.beltStepPerRevolution * self.beltStepLength) / (self.stepsPerRevolution / self.resolution)
        self.stepDelay = 0

        self.Kp = 1
        self.Kd = 0

        self.x = 0
        self.y = 0

    def EnableGantry(self):
        self.motors[0].Enable()
        self.motors[1].Enable()

    def DisableGantry(self):
        self.motors[0].Disable()
        self.motors[1].Disable()

    def MoveX(self, toX, delay):
        if toX - self.x >= 0: 
            direction = 1
            self.motors[0].pinDIR.value(direction)
            self.motors[1].pinDIR.value(direction)
        else:
            direction = 0
            self.motors[0].pinDIR.value(direction)
            self.motors[1].pinDIR.value(direction)
        
        initialDiff = abs(toX - self.x)

        while abs(toX - self.x) >= self.mmPerStep:
            self.motors[0].Step(1, self.stepDelay)
            self.motors[1].Step(1, self.stepDelay)

            if direction == 1: self.x += self.mmPerStep
            elif direction == 0: self.x -= self.mmPerStep

            #actualDelay = math.floor( abs((1000 * (1 - abs(toX - self.x)/initialDiff)) - 500) )
            utime.sleep_us(delay)

    def MoveY(self, toY, delay):
        if toY - self.y >= 0: 
            direction = 1
            self.motors[0].pinDIR.value(1)
            self.motors[1].pinDIR.value(0)
        else:
            direction = 0
            self.motors[0].pinDIR.value(0)
            self.motors[1].pinDIR.value(1)
        
        initialDiff = abs(toY - self.y)

        while abs(toY - self.y) >= self.mmPerStep:
            self.motors[0].Step(1, self.stepDelay)
            self.motors[1].Step(1, self.stepDelay)
            
            if direction == 1: self.y += self.mmPerStep
            elif direction == 0: self.y -= self.mmPerStep

            #actualDelay = math.floor( abs((1000 * (1 - abs(toY - self.y)/initialDiff)) - 500) )
            utime.sleep_us(delay)

