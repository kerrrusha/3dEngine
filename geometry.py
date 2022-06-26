from dot import Dot
from line import Line
from parser import Parser
from axis import Axis
import math

class Geometry:
    def calculateRectangleVertexes(center : Dot, width, height, zAngle=0, yAngle=0, xAngle=0) -> list[Dot]:
        """
            Returns 4 rectangle vertexes
        """
        zAngle = Parser.parseAngle(zAngle, 0, 360)
        yAngle = Parser.parseAngle(yAngle, 0, 360)
        xAngle = Parser.parseAngle(xAngle, 0, 360)

        result = [Dot(), Dot(), Dot(), Dot()]
        for dot in result:
            dot.copy(center)
        result[0].moveByAxis(-width / 2, Axis.y)
        result[0].moveByAxis(-height / 2, Axis.z)
        result[1].moveByAxis(-width / 2, Axis.y)
        result[1].moveByAxis(height / 2, Axis.z)
        result[2].moveByAxis(width / 2, Axis.y)
        result[2].moveByAxis(height / 2, Axis.z)
        result[3].moveByAxis(width / 2, Axis.y)
        result[3].moveByAxis(-height / 2, Axis.z)

        if not (zAngle or yAngle or xAngle):
            for dot in result:
                dot.turnAround(center, Axis.z, zAngle)
                dot.turnAround(center, Axis.y, yAngle)
                dot.turnAround(center, Axis.x, xAngle)

        return result

    def calculateRectangleCenter(A : Dot, B : Dot, C : Dot, D : Dot) -> Dot:
        return A.add(C.subtract(A).divide(2))

    def calculateDotAngle(dot : Dot, center : Dot, axis=Axis.y) -> float:
        radius = dot.distanceTo(center)

        deltaW, deltaH = None, None
        if axis == Axis.y:
            deltaW = (dot.x - center.x)
            deltaH = (dot.z - center.z)
        elif axis == Axis.z:
            deltaW = (dot.x - center.x)
            deltaH = (dot.y - center.y)
        elif axis == Axis.x:
            deltaW = (dot.y - center.y)
            deltaH = (dot.z - center.z)
        dotAngle = math.acos(math.fabs(deltaW) / radius)
        if deltaW < 0 and deltaH > 0:
            dotAngle = math.pi - dotAngle
        elif deltaW < 0 and deltaH < 0:
            dotAngle = math.pi + dotAngle
        elif deltaW > 0 and deltaH < 0:
            dotAngle = 2*math.pi - dotAngle

        return dotAngle