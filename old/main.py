from machine import Pin
import utime

import sys
sys.path.append('/lib')

import lib.machineService as machineService
import lib.axisService as axisService

finished = False
testMode = 4

gantry = axisService.Gantry([machineService.Motor([2, 3, 4]),
                             machineService.Motor([6, 7, 8])])

while finished == False:
    try:
        gantry.EnableGantry()

        if testMode == 0:
            generalDelay = 0
            gantry.Move([100, 0], generalDelay)
            gantry.Move([100, 100], generalDelay)
            gantry.Move([0, 100], generalDelay)
            gantry.Move([0, 0], generalDelay)


        elif testMode == 1:
            currentPos = [0, 0]
            for b in range(100):
                gantry.MoveX(currentPos[0]+gantry.mmPerStep)
                currentPos[0] = currentPos[0] + gantry.mmPerStep
                gantry.MoveY(currentPos[1]+gantry.mmPerStep)
                currentPos[1] = currentPos[1] + gantry.mmPerStep

            for b in range(100):
                gantry.MoveX(currentPos[0]-gantry.mmPerStep)
                currentPos[0] = currentPos[0] - gantry.mmPerStep
                gantry.MoveY(currentPos[1]-gantry.mmPerStep)
                currentPos[1] = currentPos[1] - gantry.mmPerStep

        elif testMode == 2:
            utime.sleep(3)

        elif testMode == 3:
            gantry.motors[0].pinDIR.value(1)
            gantry.motors[1].pinDIR.value(1)
            for i in range(1000):
                gantry.motors[0].Step(1)
                gantry.motors[1].Step(1)
                utime.sleep_us(1000)
        
        elif testMode == 4:
            zeroX = Pin(16, Pin.IN, Pin.PULL_DOWN)
            zeroY = Pin(17, Pin.IN, Pin.PULL_DOWN)
            print(zeroX.value(), zeroY.value())


        utime.sleep(1)

        gantry.DisableGantry()

        finished = True
    except KeyboardInterrupt as error:
        gantry.DisableGantry()  

        finished = True
        print('Program, kullanici tarafindan sonlandirildi!')