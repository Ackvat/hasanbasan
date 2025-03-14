from machine import Pin
import utime
import sys

sys.path.append('/lib')
import lib.machineService as machineService

machine = machineService.Machine(motors=[machineService.Motor([2, 3, 4]), machineService.Motor([5, 6, 7])])

finished = False

machine.gantry.Enable()

while finished == False:
    try:
        machine.serial.Write(machine.serial.serial0)

        if machine.gantry.zeroX.value() == 1:
            print("Zero X")
        if machine.gantry.zeroY.value() == 1:
            print("Zero Y")
        utime.sleep(1)
    except KeyboardInterrupt:
        machine.gantry.Disable()
        finished = True