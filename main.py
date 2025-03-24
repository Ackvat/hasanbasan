from machine import Pin
import utime
import sys
import _thread

sys.path.append('/lib')
import lib.machineService as machineService

machine = machineService.Machine(motors={
    'STX': machineService.StepMotor([2, 3, 4]), 
    'STY': machineService.StepMotor([6, 7, 8]), 
    'SEZ': machineService.ServoMotor(pin=10)})
machine.gantry.Disable()

machine.debug = False
machine.exit = False

machine.serial.Write("discoplotter 1.2a [\'$\' for help]")
machine.serial.Write("ok")

while machine.exit == False:
    try:
        command = machine.serial.Read()
    
        if command is not None:
            machine.ParseCommand(command)
            
    except KeyboardInterrupt as error:
        machine.gantry.Disable()
        machine.exit = True
        print("Exiting...")