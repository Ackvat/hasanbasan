from machine import Pin
from time import sleep

IN1 = Pin(10,Pin.OUT)
IN2 = Pin(11,Pin.OUT)
IN3 = Pin(12,Pin.OUT)
IN4 = Pin(13,Pin.OUT)

pins = [IN1, IN2, IN3, IN4]

sequence = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]

print("Step testi baslatiliyor...")

while True:
    try:
        for step in sequence:
            for i in range(len(pins)):
                pins[i].value(step[i])
            sleep(0.002)
    except KeyboardInterrupt:
        break

for i in range(len(pins)):
    pins[i].value(0)

print("Step testi durduruldu!")