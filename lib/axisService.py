from machine import Pin
import utime

import sys
sys.path.append('/lib')

import lib.motorService as motorService

class Gantry:
    def __init__(self, motors):
        self.motors = motors

        self.x = 0
        self.y = 0

    def EnableGantry(self):
        self.motors[0].Enable()
        self.motors[1].Enable()

    def DisableGantry(self):
        self.motors[0].Disable()
        self.motors[1].Disable()

    def MoveX(self, toX, speed, delay):
        if toX - self.x >= 0: 
            direction = 1
            self.motors[0].pinDIR.value(direction)
            self.motors[1].pinDIR.value(direction)
        else:
            direction = 0
            self.motors[0].pinDIR.value(direction)
            self.motors[1].pinDIR.value(direction)
        
        while abs(toX - self.x) > 0:
            self.motors[0].Step(1, speed)
            self.motors[1].Step(1, speed)
            if direction == 1: self.x += 1
            elif direction == 0: self.x -= 1
            utime.sleep_us(delay)
            
        print(f"Yeni X pozisyonu: {self.x}")