import math

class Vector3:
    def __init__(self, x, y, z):
        self.x: float = x
        self.y: float = y
        self.z: float = z

        self.n = 3
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other):
        return Vector3(self.x * other, self.y * other, self.z * other)
    
    def __div__(self, other):
        return Vector3(self.x / other, self.y / other, self.z / other)
    
    def __truediv__(self, other):
        return Vector3(self.x / other, self.y / other, self.z / other)
    
    def Magnitude(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
    
    def Median(self):
        return (self.x + self.y + self.z) / self.n
    
    def AbsoluteMedian(self):
        return abs(self.Median())
    
    def Normalized(self):
        if self.Magnitude() == 0:
            return Vector3(0, 0, 0)
        
        normalizedVector = Vector3(self.x, self.y, self.z)
        normalizedVector.x /= self.Magnitude()
        normalizedVector.y /= self.Magnitude()
        normalizedVector.z /= self.Magnitude()
        return normalizedVector
    
    def Unit(self):
        normalizedVector = self.Normalized()

        if normalizedVector.x > 0: normalizedVector.x = 1 
        elif normalizedVector.x < 0: normalizedVector.x = -1 
        else: normalizedVector.x = 0

        if normalizedVector.y > 0: normalizedVector.y = 1 
        elif normalizedVector.y < 0: normalizedVector.y = -1 
        else: normalizedVector.y = 0

        if normalizedVector.z > 0: normalizedVector.z = 1 
        elif normalizedVector.z < 0: normalizedVector.z = -1 
        else: normalizedVector.z = 0

        return normalizedVector

    def RotateZ(self, angle):
        degreeToRadians = math.radians(angle)
        return Vector3(self.x*math.cos(degreeToRadians) - self.y*math.sin(degreeToRadians), self.x*math.sin(degreeToRadians) + self.y*math.cos(degreeToRadians), self.z)

    def Clone(self):
        return Vector3(self.x, self.y, self.z)
    


def Clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n 