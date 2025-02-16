from machine import Pin
from time import sleep

IN1 = Pin(10,Pin.OUT)
IN2 = Pin(11,Pin.OUT)
IN3 = Pin(12,Pin.OUT)
IN4 = Pin(13,Pin.OUT)

BIN1 = Pin(2,Pin.OUT)
BIN2 = Pin(3,Pin.OUT)
BIN3 = Pin(4,Pin.OUT)
BIN4 = Pin(5,Pin.OUT)

APins = [IN1, IN2, IN3, IN4]
BPins = [BIN1, BIN2, BIN3, BIN4]

sequence = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]

stepT = 0.002
stepH = 100

def Kill(motor):
    for i in range(len(APins)):
        if motor == 0:
            APins[i].value(0)
        elif motor == 1:
            BPins[i].value(0)

def SmallStep(motor, count):
    if count < 0: 
        direction = -1 
    else: 
        direction = 1

    for i in range(abs(count)):
        try:
            for step in sequence:
                for i in range(len(APins)):
                    if direction == 1:
                        if motor == 0:
                            APins[i].value(step[i])
                        elif motor == 1:
                            BPins[i].value(step[i])
                    elif direction == -1:
                        if motor == 0:
                            APins[i].value(step[len(sequence)-1 - i])
                        elif motor == 1:
                            BPins[i].value(step[len(sequence)-1 - i])
                sleep(stepT)
        except KeyboardInterrupt:
            break

def NiggerStep(axis, count):
    if count < 0: 
        direction = -1 
    else: 
        direction = 1

    for i in range(abs(count)):
        try:
            for step in sequence:
                for i in range(len(APins)):
                    if direction == 1:
                        if axis == 0:
                            APins[i].value(step[i])
                            BPins[i].value(step[i])
                        elif axis == 1:
                            APins[i].value(step[i])
                            BPins[i].value(step[len(sequence)-1 - i])
                    elif direction == -1:
                        if axis == 0:
                            APins[i].value(step[len(sequence)-1 - i])
                            BPins[i].value(step[len(sequence)-1 - i])
                        elif axis == 1:
                            APins[i].value(step[len(sequence)-1 - i])
                            BPins[i].value(step[i])
                sleep(stepT)
        except KeyboardInterrupt:
            break


print("Step testi baslatiliyor...")

for i in range(1):
    SmallStep(0, stepH)
    SmallStep(0, -stepH)
    SmallStep(1, stepH)
    SmallStep(1, -stepH)

    SmallStep(0, -stepH)
    SmallStep(0, stepH)
    SmallStep(1, -stepH)
    SmallStep(1, stepH)

for i in range(1):
    NiggerStep(0, stepH)
    NiggerStep(0, -stepH)
    NiggerStep(1, stepH)
    NiggerStep(1, -stepH)

Kill(0)
Kill(1)

print("Step testi durduruldu!")
