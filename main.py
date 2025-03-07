from machine import Pin
import utime

import sys
sys.path.append('/lib')

import lib.motorService as motorService
import lib.axisService as axisService

baseResolution = 1/16

gantry = axisService.Gantry([motorService.Motor([2, 3, 4], baseResolution),
                             motorService.Motor([6, 7, 8], baseResolution)])

gantry.motors[1].stepsPerRevolution = 230

gantry.EnableGantry()

utime.sleep(1)

gantry.MoveX(200 / baseResolution, 0, 0)

utime.sleep(1)

#gantry.MoveX(0 / baseResolution, 0, 0)

gantry.DisableGantry()