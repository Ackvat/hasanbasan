import sys
sys.path.append('/lib')

from machine import Pin
from time import sleep

import lib.motorService as motorService

usleep = lambda x: sleep(x/1000000.0)

motor1 = motorService.Motor([2, 3, 4])
motor1.stepResolution = 1/8
motor1.Enable()

motor1.Step(200/motor1.stepResolution, 1000)
#motor1.Rotate(360, 1.05)
sleep(0.5)
#motor1.Rotate(-360, 1)
motor1.Step(-200/motor1.stepResolution, 900)

motor1.Disable()

