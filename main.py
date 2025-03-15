from machine import Pin
import utime
import sys

sys.path.append('/lib')
import lib.machineService as machineService

machine = machineService.Machine(motors=[machineService.StepMotor([2, 3, 4]), machineService.StepMotor([6, 7, 8]), machineService.ServoMotor(pin=10)])
machine.gantry.Disable()

finished = False

while finished == False:
    try:
        command = machine.serial.Read()

        if command is not None:
            machine.InterpretCommand(command)
            
    except KeyboardInterrupt as error:
        machine.gantry.Disable()
        finished = True
        print("Exiting...")