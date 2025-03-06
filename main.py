import sys
sys.path.append('/lib')

from machine import Pin
from time import sleep

import lib.motorService as motorService



baseDelay = 0
baseRange = 100

baseResolution = 1/16

motor1 = motorService.Motor([2, 3, 4], baseResolution)
motor1.Enable()

motor2 = motorService.Motor([6, 7, 8], baseResolution)
motor2.Enable()

motor1.Rotate(180, 5)

motor1.Disable()
motor2.Disable()

