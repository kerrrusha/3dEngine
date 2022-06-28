import math
from axis import Axis
from dot import Dot

class Shape:
    def __init__(self, dots : list[Dot]) -> None:
        self.dots = dots

class Circle(Shape):
    def __init__(self, dots : list[Dot], center : Dot, axis : Axis) -> None:
        super().__init__(dots)
        self.center = center
        self.axis = axis

    def createCircle(center : Dot, radius : float, axis : Axis, dotsNumber : int):
        dots = []
        axis = Axis.y
        radius = 15
        for i in range(dotsNumber):
            rads = math.radians(i * 360 / dotsNumber)
            if axis == Axis.x:
                x = center.x
                y = center.y + radius * math.cos(rads)
                z = center.z + radius * math.sin(rads)
            elif axis == Axis.y:
                y = center.y
                x = center.x + radius * math.cos(rads)
                z = center.z + radius * math.sin(rads)
            elif axis == Axis.z:
                z = center.z
                x = center.x + radius * math.cos(rads)
                y = center.y + radius * math.sin(rads)
            dots.append(Dot(x, y, z))
        circle = Circle(dots, center, axis)
        return circle