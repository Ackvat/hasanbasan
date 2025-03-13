from machine import Pin
import utime

import sys
sys.path.append('/lib')

import lib.machineService as machineService

gantry = machineService.Gantry([machineService.Motor([2, 3, 4]),
                             machineService.Motor([6, 7, 8])])

finished = False

while finished == False:
    try:
        gantry.EnableGantry()
        zeroX = Pin(16, Pin.IN, Pin.PULL_DOWN)
        zeroY = Pin(17, Pin.IN, Pin.PULL_DOWN)
        print(zeroX.value(), zeroY.value())
        utime.sleep(1)
    except KeyboardInterrupt:
        gantry.DisableGantry()
        finished = True