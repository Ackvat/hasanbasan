from machine import Pin, UART, PWM, freq
import select
import sys
import utime

sys.path.append('/lib')
from lib.mathService import Vector3, Clamp
import lib.functionService as functionService

class Machine:
    def __init__(self, motors):
        self.debug = False
        self.verbose = False
        self.echo = False
        self.exit = False

        self.coreFreq = 250*(10**6)
        freq(self.coreFreq)

        self.gantry = Gantry(self, motors)
        self.serial = Serial()

        self.parallelThread = None

        self.commandTable = {
            'G': {
                '-1': self.gantry.LinearMove,
                '0': self.gantry.LinearMove,
                '1': self.gantry.LinearMove,

                '4': self.Dwell,

                '28': self.gantry.Home,

                '90': self.gantry.SetPositionType,
                '91': self.gantry.SetPositionType,
            },

            'M': {
                '0': self.Pause,
                '30': self.gantry.Disable,
                '31': self.gantry.Enable,

                '114': self.gantry.GetCurrentPosition,

                '1000': self.gantry.SetResolution,
                '1001': self.SetCoreFreq,
                '1002': self.gantry.SetZStep,
            },

            'T': {
                
            },

            'F': self.gantry.SetFeedRate,
        }
        return

    def ParseCommand(self, command):
        tokens = functionService.findall(r'([A-Za-z])(-?\d+(?:\.\d+)?)', command)
        
        responseCommand = command

        parsed = {}
        for letter, number in tokens:
            if '.' in number:
                parsed[letter] = float(number)
            else:
                parsed[letter] = int(number)

        command = parsed

        if 'F' in command: self.commandTable['F'](command) 

        if 'M' in command:
            code_str = str(command['M']).strip()
            if not code_str.isdigit():
                self.serial.Write("error: Invalid statement")
                return

            commandType = self.commandTable['M']
            if code_str in commandType:
                commandType[code_str](command)
            else:
                self.serial.Write("error: Invalid statement")
                return
        if 'T' in command:
            code_str = str(command['T']).strip()
            if not code_str.isdigit():
                self.serial.Write("error: Invalid statement")
                return

            commandType = self.commandTable['T']
            if code_str in commandType:
                commandType[code_str](command)
            else:
                self.serial.Write("error: Invalid statement")
                return
        if 'G' in command:
            code_str = str(command['G']).strip()
            if not code_str.isdigit():
                self.serial.Write("error: Invalid statement")
                return

            commandType = self.commandTable['G']
            if code_str in commandType:
                commandType[code_str](command)
            else:
                self.serial.Write("error: Invalid statement")
                return
        if 'X' in command or 'Y' in command or 'Z' in command:
            self.gantry.LinearMove(command)

        if self.echo: self.serial.Write(f'[echo: {responseCommand}]')
        self.serial.Write("ok") 
        return
    
    def Dwell(self, command):
        if 'S' in command:
            utime.sleep(int(command['S']))
        elif 'P' in command:
            utime.sleep_ms(int(command['P']))
        else:
            utime.sleep(1)
        return
    
    def Pause(self, command):
        self.serial.Write("[MSG: Tool change, press enter to continue]")
        while True:
            command = self.serial.Read()
            if command is not None:
                break
        return

    def SetCoreFreq(self, command):
        if 'C' in command:
            self.coreFreq = int(command['C'])
            freq(self.coreFreq)
        return

    def GetParserState(self, command):
        self.serial.Write(f"[G{self.gantry.moveType} G54 G17 G21 G{self.gantry.positionType} G93 M1 M3 M9 T1 F{self.gantry.feedRate} S0]")
        return
        


class Serial:
    def __init__(self):
        self.led = Pin("LED", Pin.OUT)
        return

    def Read(self):
        if select.select([sys.stdin], [], [], 0)[0]:
            line = sys.stdin.readline().strip().upper()

            if line.startswith("TX>"):
                line = line[3:].strip()
            
            return line
        else:
            return None
    
    def Write(self, data):
        print(data + '\r\n')
        return



class Gantry:
    def __init__(self, machine, motors):
        self.machine = machine
        self.motors = motors
        self.limitX = Pin(16, Pin.IN, Pin.PULL_DOWN)
        self.limitY = Pin(17, Pin.IN, Pin.PULL_DOWN)
        self.MS1 = Pin(14, Pin.OUT)
        self.MS2 = Pin(15, Pin.OUT)

        self.MS1.value(1)
        self.MS2.value(0)

        self.enabled = False



        self.errorRate = 0.9

        self.stepsPerRevolution = 200
        self.resolution = 1/32
        self.pulleyTeethCount = 46
        self.beltStepLength = 2
        self.mmPerStep = (self.pulleyTeethCount * self.beltStepLength) / (self.stepsPerRevolution / self.resolution)

        self.zStep = 0.005

        self.stepDelay = 10



        self.moveType = 0
        self.positionType = 90

        self.position = Vector3(0, 0, 0)
        self.goalPosition = Vector3(0, 0, 0)
        self.virtualPosition = Vector3(0, 0, 0)

        self.positionDifference = Vector3(0, 0, 0)

        self.direction = Vector3(0, 0, 0)

        self.limits = Vector3(270, 210, 4)
        self.outlie = Vector3(-10, -10, 0)

        self.velocity = Vector3(0, 0, 0)
        
        self.feedRate = 500
        self.engraveRate = 500
        self.travelRate = 1000
        self.homeRate = 100
        return

    def Enable(self, command=None):
        self.motors['STX'].Enable()
        self.motors['STY'].Enable()
        self.LinearMove({'G': 0, 'Z': 4})
        self.enabled = True
        return

    def Disable(self, command=None):
        self.motors['STX'].Disable()
        self.motors['STY'].Disable()
        self.enabled = False
        return

    def SetResolution(self, command):
        if 'R' in command:
            if int(command['R']) == 8:
                self.MS1.value(0)
                self.MS2.value(0)
                self.resolution = 1/8
            elif int(command['R']) == 16:
                self.MS1.value(1)
                self.MS2.value(1)
                self.resolution = 1/16
            elif int(command['R']) == 32:
                self.MS1.value(1)
                self.MS2.value(0)
                self.resolution = 1/32
            elif int(command['R']) == 64:
                self.MS1.value(0)
                self.MS2.value(1)
                self.resolution = 1/64
            self.mmPerStep = (self.pulleyTeethCount * self.beltStepLength) / (self.stepsPerRevolution / self.resolution)
            if self.machine.debug: print(self.resolution, self.mmPerStep, self.MS1.value(), self.MS2.value())

    def SetFeedRate(self, command):
        if 'F' in command: 
            self.engraveRate= int(command['F'])
            self.travelRate = self.engraveRate * 2
        return
    
    def SetZStep(self, command):
        if 'S' in command: self.zStep = float(command['S'])
        return

    def SetPositionType(self, command):
        if 'G' in command:
            if command['G'] == 90: self.positionType = 90
            elif command['G'] == 91: self.positionType = 91
        return
  
    def GetCurrentPosition(self, command=None):
        self.machine.serial.Write(f'X: {self.position.x} Y: {self.position.y} Z: {self.position.z}')
        return
    
    def LinearMove(self, command, force=False):
        if 'G' in command:
            if command['G'] == 0:
                self.moveType = 0
                self.feedRate = self.travelRate
            elif command['G'] == 1:
                self.moveType = 1
                self.feedRate = self.engraveRate
            elif command['G'] == -1:
                self.moveType = -1
                self.feedRate = self.homeRate

        self.goalPosition = self.position.Clone()
        self.virtualPosition = self.position.Clone()
        if self.positionType == 90:
            if 'X' in command: self.goalPosition.x = Clamp(float(command['X']), self.outlie.x, self.limits.x)
            if 'Y' in command: self.goalPosition.y = Clamp(float(command['Y']), self.outlie.y, self.limits.y)
            if 'Z' in command: self.goalPosition.z = Clamp(float(command['Z']), self.outlie.z, self.limits.z)
        elif self.positionType == 91:
            if 'X' in command: self.goalPosition.x += float(command['X'])
            if 'Y' in command: self.goalPosition.y += float(command['Y'])
            if 'Z' in command: self.goalPosition.z += float(command['Z'])

        self.positionDifference = (self.goalPosition - self.position)
        self.direction = self.positionDifference.Normalized()

        while self.positionDifference.Magnitude() > self.mmPerStep*self.errorRate:
            if (self.limitX.value() == 1 or self.limitY.value() == 1) and not force:
                break

            self.positionDifference = (self.goalPosition - self.position)
            self.direction = self.positionDifference.Normalized()

            self.virtualPosition += Vector3(self.direction.x*self.mmPerStep, self.direction.y*self.mmPerStep, self.direction.z*self.zStep)

            if abs(self.virtualPosition.x - self.position.x) > self.mmPerStep*self.errorRate:
                if self.virtualPosition.x - self.position.x > 0:
                    self.motors['STX'].pinDIR.value(0)
                    self.position.x += self.mmPerStep
                else:
                    self.motors['STX'].pinDIR.value(1)
                    self.position.x -= self.mmPerStep

                self.motors['STX'].StepSignal(1)

            if abs(self.virtualPosition.y - self.position.y) > self.mmPerStep*self.errorRate:
                if self.virtualPosition.y - self.position.y > 0:
                    self.motors['STY'].pinDIR.value(0)
                    self.position.y += self.mmPerStep
                else:
                    self.motors['STY'].pinDIR.value(1)
                    self.position.y -= self.mmPerStep

                self.motors['STY'].StepSignal(1)

            if abs(self.virtualPosition.z - self.position.z) > self.zStep*self.errorRate:
                if self.virtualPosition.z - self.position.z > 0:
                    self.position.z += self.zStep
                else:
                    self.position.z -= self.zStep

            utime.sleep_us(self.stepDelay)
            self.motors['STX'].StepSignal(0)
            self.motors['STY'].StepSignal(0)
            self.motors['SEZ'].Move(self.position.z)
            utime.sleep_us(self.stepDelay)

            if self.machine.debug:
                print(f'\n')
                print(f'Direction [mm]: {self.direction.x}, {self.direction.y}')
                print(f'Position [mm]: {self.position.x}, {self.position.y} -> {self.goalPosition.x}, {self.goalPosition.y}')
                print(f'Virtual Position [mm]: {self.virtualPosition.x}, {self.virtualPosition.y}')

            utime.sleep_us(int((10**6)/(self.feedRate/self.mmPerStep)))
        
        return
                    
    def Home(self, command=None):
        self.LinearMove({'G': -1, 'Z': 4})

        self.SetPositionType({'G': 91})

        self.LinearMove({'G': -1, 'X': -self.limits.x})
        self.position.x = 0
        self.LinearMove({'G': -1, 'X': 15}, True)
        self.position.x = 0
        if self.machine.debug: print("X-axis homed!")

        self.LinearMove({'G': -1, 'Y': -self.limits.y})
        self.position.y = 0
        self.LinearMove({'G': -1, 'Y': 15}, True)
        self.position.y = 0
        if self.machine.debug: print("Y-axis homed!")

        self.SetPositionType({'G': 90})

        return



class StepMotor:
    def __init__(self, controlPins):
        self.pinEN = Pin(controlPins[0],Pin.OUT)
        self.pinSTEP = Pin(controlPins[1],Pin.OUT)
        self.pinDIR = Pin(controlPins[2],Pin.OUT)
        return

    def Enable(self, command=None):
        self.pinEN.value(0)
        return
    
    def Disable(self, command=None):
        self.pinEN.value(1)
        return

    def StepSignal(self, value=0):
        self.pinSTEP.value(value)
        return
    


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
        return
        
    def Move(self, position):
        position = Clamp(position, 1, 4)
        position = (self.maxAngle-self.offsetAngle) - (position/(self.absRange))*(100-self.offsetAngle)
        duty_ns = int(self.MAX_DUTY - position * (self.MAX_DUTY-self.MIN_DUTY)/180)
        self.pwm.duty_ns(duty_ns)
        return