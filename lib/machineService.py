from machine import Pin, UART, PWM
import select
import sys
import utime
import re

sys.path.append('/lib')
import lib.functionService as functionService

class Machine:
    def __init__(self, motors):
        self.gantry = Gantry(motors)
        self.serial = Serial()

        self.systemFrequency = 60

        self.commandTable = {
            'G': {
                'id': 0,
                '0': self.gantry.Move,
                '1': self.gantry.Move,
                '4': self.Dwell,

                '28': self.gantry.Home,

                '90': self.gantry.SetPositionType,
                '91': self.gantry.SetPositionType,
            },

            'M': {
                'id': 0,
                '30': self.gantry.Disable,
                '31': self.gantry.Enable,

                '114': self.gantry.GetCurrentPosition,
            },

            'F': self.gantry.SetFeedRate,
            'T': self.gantry.SetTravelFeedRate,
        }

    def InterpretCommand(self, command):
        if 'F' in command:
            self.commandTable['F'](command)

        if 'T' in command:
            self.commandTable['T'](command)

        if 'G' in command:
            code_str = str(command['G']).strip()
            if not code_str.isdigit():
                self.serial.Write("bruh")
                return

            commandType = self.commandTable['G']
            if code_str in commandType:
                commandType[code_str](command)
                self.serial.Write("ok")
                return
            else:
                self.serial.Write("bruh")
                return

        elif 'M' in command:
            code_str = str(command['M']).strip()
            if not code_str.isdigit():
                self.serial.Write("bruh")
                return

            commandType = self.commandTable['M']
            if code_str in commandType:
                commandType[code_str](command)
                self.serial.Write("ok")
                return
            else:
                self.serial.Write("bruh")
                return
        else:
            self.serial.Write("bruh")
    
    def Dwell(self, command):
        if 'S' in command:
            utime.sleep(int(command['S']))
        elif 'P' in command:
            utime.sleep_ms(int(command['P']))
        else:
            utime.sleep(1)
        
    

class Serial:
    def __init__(self):
        self.led = Pin("LED", Pin.OUT)

    def Read(self):
        if select.select([sys.stdin], [], [], 0)[0]:
            line = sys.stdin.readline().strip().upper()

            if line.startswith("TX>"):
                line = line[3:].strip()
            
            tokens = functionService.findall(r'([A-Za-z])(-?\d+(?:\.\d+)?)', line)
            
            parsed = {}
            for letter, number in tokens:
                if '.' in number:
                    parsed[letter] = float(number)
                else:
                    parsed[letter] = int(number)

            return parsed
        else:
            return None
    
    def Write(self, data):
        print(data)



class Gantry:
    def __init__(self, motors):
        self.motors = motors

        self.stepsPerRevolution = 200
        self.resolution = 1/16
        self.beltStepPerRevolution = 36
        self.beltStepLength = 2
        self.mmPerStep = (self.beltStepPerRevolution * self.beltStepLength) / (self.stepsPerRevolution / self.resolution)

        self.zStep = 0.01

        self.stepDelay = 10

        self.errorRate = 0.5

        self.zeroX = Pin(16, Pin.IN, Pin.PULL_DOWN)
        self.zeroY = Pin(17, Pin.IN, Pin.PULL_DOWN)
        
        self.enabled = False

        self.positionType = 0

        self.x = 0
        self.tox = 0
        self.y = 0
        self.toy = 0
        self.z = 0
        self.toz = 0

        self.f = 1000
        self.tf = 2000
        self.homef = 1000
        self.maxf = 5000

        self.a = 50
        self.ta = 100
        self.homea = 50
        self.maxa = 300

    def Enable(self, command=None):
        self.motors[0].Enable()
        self.motors[1].Enable()
        self.enabled = True

    def Disable(self, command=None):
        self.motors[0].Disable()
        self.motors[1].Disable()
        self.enabled = False

    def SetFeedRate(self, command):
        self.f = int(command['F'])
        if self.f > self.maxf: self.f = self.maxf
    
    def SetTravelFeedRate(self, command):
        self.tf = int(command['T'])
        if self.tf > self.maxf: self.tf = self.maxf

    def SetPositionType(self, command):
        if command['G'] == 90:
            self.positionType = 0
        elif command['G'] == 91:
            self.positionType = 1
    
    def SetMoveToPosition(self, command):
        for i, (k, v) in enumerate(command.items()):
            if k == 'X': self.tox = float(v)
            elif k == 'Y': self.toy = float(v)
            elif k == 'Z': self.toz = float(v)
        

    def GetCurrentPosition(self, command):
        print("X: " + str(self.x) + " Y: " + str(self.y) + " Z: " + str(self.z) + " F: " + str(self.f) + " TF: " + str(self.tf))

    def Move(self, command):
        if self.enabled == False: return

        if self.tox - self.x >= 0: directionX = 1
        else: directionX = 0

        if self.toy - self.y >= 0: directionY = 1
        else: directionY = 0

        if self.toz - self.z >= 0: directionZ = 1
        else: directionZ = 0

        while abs(self.tox - self.x) >= self.mmPerStep*self.errorRate or abs(self.toy - self.y) >= self.mmPerStep*self.errorRate or abs(self.toz - self.z) >= self.mmPerStep*self.errorRate:
            if abs(self.tox - self.x) >= self.mmPerStep*self.errorRate:
                if directionX == 1: 
                    self.motors[0].pinDIR.value(1)
                    self.motors[1].pinDIR.value(1)
                    self.x += self.mmPerStep
                elif directionX == 0:
                    self.motors[0].pinDIR.value(0)
                    self.motors[1].pinDIR.value(0)
                    self.x -= self.mmPerStep
                self.motors[0].Step(1)
                self.motors[1].Step(1)
                utime.sleep_us(self.stepDelay)
                self.motors[0].Step(0)
                self.motors[1].Step(0)
            
            if abs(self.toy - self.y) >= self.mmPerStep*self.errorRate:
                if directionY == 1:
                    self.motors[0].pinDIR.value(1)
                    self.motors[1].pinDIR.value(0)
                    self.y += self.mmPerStep
                elif directionY == 0:
                    self.motors[0].pinDIR.value(0)
                    self.motors[1].pinDIR.value(1)
                    self.y -= self.mmPerStep
                self.motors[0].Step(1)
                self.motors[1].Step(1)
                utime.sleep_us(self.stepDelay)
                self.motors[0].Step(0)
                self.motors[1].Step(0)

            if abs(self.toz - self.z) >= self.mmPerStep*self.errorRate:
                if directionZ == 1:
                    self.z += self.zStep
                elif directionZ == 0:
                    self.z -= self.zStep
                    
                self.motors[2].Move(self.z)

            # 1000000 mikrosaniye beklerse, saniye de 1 mm hareket eder.
            if command['G'] == 0:
                utime.sleep_us(int(self.maxf / self.tf))
            elif command['G'] == 1:
                utime.sleep_us(int(self.maxf / self.f))
    
    def Home(self, command):
        self.Enable()

        savedFeedRate = self.f

        self.f = 1000
        self.Move({'G': 1, 'Z': 2})

        while self.zeroX.value() == 0:
            self.Move({'G': 1, 'X': self.x - self.mmPerStep})
        utime.sleep(1)
        self.Move({'G': 1, 'X': self.x + 10})
        self.x = 0

        utime.sleep(1)

        while self.zeroY.value() == 0:
            self.Move({'G': 1, 'Y': self.y - self.mmPerStep})
        utime.sleep(1)
        self.Move({'G': 1, 'Y': self.y + 10})
        self.y = 0

        self.f = savedFeedRate



class StepMotor:
    def __init__(self, controlPins):
        self.pinEN = Pin(controlPins[0],Pin.OUT)
        self.pinSTEP = Pin(controlPins[1],Pin.OUT)
        self.pinDIR = Pin(controlPins[2],Pin.OUT)

    def Enable(self, command=None):
        self.pinEN.value(0)
    
    def Disable(self, command=None):
        self.pinEN.value(1)

    def Step(self, value=0):
        self.pinSTEP.value(value)
    


class ServoMotor:
    def __init__(self, MIN_DUTY=300000, MAX_DUTY=2300000, pin=10, freq=50):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(freq)
        self.MIN_DUTY = MIN_DUTY
        self.MAX_DUTY = MAX_DUTY

        self.minAngle = 60
        self.maxAngle = 160
        self.offsetAngle = 0

        self.absRange = 4
        
    def Move(self, position):
        position = (self.maxAngle-self.offsetAngle) - (position/(self.absRange))*(100-self.offsetAngle)
        duty_ns = int(self.MAX_DUTY - position * (self.MAX_DUTY-self.MIN_DUTY)/180)
        self.pwm.duty_ns(duty_ns)