from machine import Pin
from time import sleep

import motorService as motorService

usleep = lambda x: sleep(x/1000000.0)

delaySpeed = 2000
steps = 200

motor1 = motorService.Motor([2, 3, 4])

motor1.Step(steps, delaySpeed)

