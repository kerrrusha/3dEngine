import math
from axis import Axis
from dot import Dot
from geometry import Geometry
from line import Line

class ObjectController:
    def __init__(self, objects : list) -> None:
        self.objects = objects

    def rotateAll(self, center : Dot, axis=Axis.y, angleStep=10):
        # угловая скорость вращения (радиан за кадр)
        radPerFrame = math.pi * angleStep / 180 
        for obj in self.objects:
            if type(obj) is Dot:
                dot = obj
                radius = dot.distanceTo(center)
                dotAngle = Geometry.calculateDotAngle(dot, center, axis)
                newAngle = dotAngle + radPerFrame
                deltaW = math.cos(newAngle) * radius
                deltaH = math.sin(newAngle) * radius
                if axis == Axis.y:
                    dot.moveByAxis(deltaW, Axis.x)
                    dot.moveByAxis(deltaH, Axis.z)
                    print(deltaW, deltaH)

    def moveForwardAll(self, speed=0.5):
         for obj in self.objects:
            if type(obj) is Dot:
                obj.moveByAxis(-speed, Axis.x)
                obj.moveByAxis(speed, Axis.y)
                obj.moveByAxis(-speed, Axis.z)