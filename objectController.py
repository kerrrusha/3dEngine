from enum import Enum
import math
from random import randint
from axis import Axis
from dot import Dot
from geometry import Geometry
from line import Line
from shape import Circle

class Direction(Enum):
    forward = 1
    backward = -1

class ObjectController:
    def __init__(self, objects=[], shapes=[]) -> None:
        self.objects = objects
        self.shapes = shapes

    def update(self, objects=None, shapes=None):
        if objects is not None:
            self.objects = objects
        if shapes is not None:
            self.shapes = shapes

    def rotateCircles(self, angleStep=randint(1,2)/10, 
                        direction=Direction.forward):
        # угловая скорость вращения (радиан за кадр)
        radPerFrame = math.radians(angleStep)
        for shape in self.shapes:
            if type(shape) is Circle:
                circle = shape
                center = circle.center
                axis = circle.axis
                for dot in circle.dots:
                    radius = dot.distanceTo(center)
                    dotAngle = Geometry.calculateDotAngle(dot, center, axis)
                    newAngle = dotAngle + direction.value*radPerFrame
                    newHorizontalValue = math.cos(newAngle) * radius
                    newVerticalValue = math.sin(newAngle) * radius
                    if axis == Axis.x:
                        dot.y = newHorizontalValue
                        dot.z = newVerticalValue
                    if axis == Axis.y:
                        dot.x = center.x + newHorizontalValue
                        dot.z = center.z + newVerticalValue

    def moveDotsForward(self, speed=0.5):
         for obj in self.objects:
            if type(obj) is Dot:
                obj.moveByAxis(-speed, Axis.x)
                obj.moveByAxis(speed, Axis.y)
                obj.moveByAxis(-speed, Axis.z)