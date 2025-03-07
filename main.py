from machine import Pin
import utime

import sys
sys.path.append('/lib')

import lib.motorService as motorService
import lib.axisService as axisService

testMode = 1

gantry = axisService.Gantry([motorService.Motor([2, 3, 4]),
                             motorService.Motor([6, 7, 8])])

gantry.EnableGantry()

if testMode == 0:
    for i in range(1):

        gantry.MoveY(25, 0)
        utime.sleep(0.5)

        gantry.MoveX(100, 0)
        utime.sleep(0.5)

        gantry.MoveY(50, 0)
        utime.sleep(0.5)

        gantry.MoveX(0, 0)
        utime.sleep(0.5)

        gantry.MoveY(75, 0)
        utime.sleep(0.5)

        gantry.MoveX(100, 0)
        utime.sleep(0.5)

        gantry.MoveY(100, 0)
        utime.sleep(0.5)
elif testMode == 1:
    currentPos = [0, 0]
    for b in range(10):
        gantry.MoveX(currentPos[0]+1, 0)
        currentPos[0] = currentPos[0] + 1
        gantry.MoveY(currentPos[1]+1, 0)
        currentPos[1] = currentPos[1] + 1


utime.sleep(1)

gantry.DisableGantry()