from decimal import DivisionByZero
import math
from axis import Axis

id = 0
class Dot:
    def __init__(self, x=0.0, y=0.0, z=0.0, name="") -> None:
        self.x = x
        self.y = y
        self.z = z

        self.name = name

        global id
        id += 1
        self.id = id

    def setValue(self, x=None, y=None, z=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if z is not None:
            self.z = z

    def copy(self, other):
        self.x = other.x
        self.y = other.y
        self.z = other.z

    def distanceTo(self, other):
        return math.sqrt( 
            (self.x - other.x) ** 2 + 
            (self.y - other.y) ** 2 + 
            (self.z - other.z) ** 2
        )

    def moveByAxis(self, delta, axis : Axis):
        if axis == Axis.z:
            self.z += delta
        elif axis == Axis.y:
            self.y += delta
        else:
            self.x += delta

    def turnAround(self, dotCenter, axis : Axis, angle):
        if angle == 0 or axis not in [Axis.x, Axis.y, Axis.z]:
            return

        radius = self.distanceTo(dotCenter)

        deltaW, deltaH = None, None
        if axis == Axis.z:
            deltaW = (self.x - dotCenter.x)
            deltaH = (self.y - dotCenter.y)
        elif axis == Axis.y:
            deltaW = (self.x - dotCenter.x)
            deltaH = (self.z - dotCenter.z)
        else:
            deltaW = (self.y - dotCenter.y)
            deltaH = (self.z - dotCenter.z)

        dotAngle = math.acos(math.fabs(deltaW) / radius)
        if deltaW < 0 and deltaH > 0:
            dotAngle = math.pi - dotAngle
        elif deltaW < 0 and deltaH < 0:
            dotAngle = math.pi + dotAngle
        elif deltaW > 0 and deltaH < 0:
            dotAngle = 2*math.pi - dotAngle
        newDotAngle = dotAngle + angle

        if axis == Axis.z:
            self.x = dotCenter.x + math.cos(newDotAngle) * radius
            self.y = dotCenter.y + math.sin(newDotAngle) * radius
        elif axis == Axis.y:
            self.x = dotCenter.x + math.cos(newDotAngle) * radius
            self.z = dotCenter.z + math.sin(newDotAngle) * radius
        else:
            self.y = dotCenter.y + math.cos(newDotAngle) * radius
            self.z = dotCenter.z + math.sin(newDotAngle) * radius

    def add(self, other):
        return Dot(self.x + other.x, self.y + other.y, self.z + other.z)

    def subtract(self, other):
        return Dot(self.x - other.x, self.y - other.y, self.z - other.z)

    def multiply(self, num : float):
        return Dot(self.x * num, self.y * num, self.z * num)

    def divide(self, num : float):
        if num == 0:
            raise DivisionByZero("Trying to divide dot by 0!")
        return Dot(self.x / num, self.y / num, self.z / num)

    def equal(self, dot) -> bool:
        return self.x == dot.x and self.y == dot.y and self.z == dot.z

    def toList(self):
        return [self.x, self.y, self.z]

    def __str__(self):
        return "({:.3f}, {:.3f}, {:.3f})".format(self.x,self.y,self.z)