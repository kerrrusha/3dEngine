import math
import numpy as np

from dot import Dot
from line import Line
from parser import Parser
from axis import Axis
from geometry import Geometry

class Camera:
    def __init__(self, position=Dot(), horizontalAngle=0, verticalAngle=0, 
                    frameWidth=10, frameHeight=10, focusDistance=5, maxDistance=101) -> None:
        self.position = position

        self.horizontalAngle = Parser.parseAngle(horizontalAngle, 0, 360)
        self.verticalAngle = Parser.parseAngle(verticalAngle, -90, 90)

        self.frameWidth = frameWidth
        self.frameHeight = frameHeight

        self.focusDistance = focusDistance
        self.maxDistance = maxDistance

        self.frameLines = self.getFrameLines()

    def moveTo(self, newPosition : Dot):
        self.position = newPosition

    # 4 линии, отображающие направление камеры 
    def getFrameLines(self) -> list[Line]:
        focusCenter = Dot(self.focusDistance, 0, 0)
        focusDots = Geometry.calculateRectangleVertexes(focusCenter, self.frameWidth, self.frameHeight)

        maxDistanceCenter = Dot(self.maxDistance, 0, 0)
        scale = self.maxDistance / self.focusDistance
        maxDistanceDots = Geometry.calculateRectangleVertexes(maxDistanceCenter, self.frameWidth * scale, self.frameHeight * scale)

        for dot in maxDistanceDots:
            dot.moveByAxis(self.position.x, Axis.x)
            dot.moveByAxis(self.position.y, Axis.y)
            dot.moveByAxis(self.position.z, Axis.z)
            dot.turnAround(self.position, Axis.z, self.horizontalAngle)
            dot.turnAround(self.position, Axis.y, self.verticalAngle)

        return [
            Line(self.position, maxDistanceDots[0]),
            Line(self.position, maxDistanceDots[1]),
            Line(self.position, maxDistanceDots[2]),
            Line(self.position, maxDistanceDots[3])
        ]

    def distanceToDot(self, dot : Dot) -> float:
        A, B, C, D = self.getFrameABCD()
        n = np.cross( A.subtract(C).toList() , 
                                B.subtract(D).toList() )
        n = n / np.linalg.norm(n)
        d = self.maxDistance - np.dot(dot.subtract(A).toList(), n)
        return float(d)
    
    def distanceToLine(self, line : Line):
        return min(self.distanceToDot(line.startDot), self.distanceToDot(line.endDot))

    def scaleToDot(self, dot : Dot) -> float:
        distance = self.distanceToDot(dot)
        scale = 1 - distance / self.maxDistance
        return scale

    def scaleToLine(self, line : Line) -> float:
        distance = self.distanceToLine(line)
        scale = 1 - distance / self.maxDistance
        return scale

    def dotIsInFrame(self, dot : Dot) -> bool:
        """
            Determine if dot is inside the camera frame
        """
        if dot is None:
            return False
        if self.position.equal(dot):
            return False
        if self.distanceToDot(dot) > self.maxDistance:
            return False
        if np.dot(self.getMaxDistanceDot().toList(), dot.toList()) < 0:
            return False

        O = self.position
        A, B, C, D = self.getFrameABCD()

        # нормали граней пирамиды
        noab, nobc, nocd, noad, nabc = self.getFramePyramidSurfaceNormales()

        directionVector = dot.subtract(O).toList()
        r = np.dot(directionVector, noab)
        insideOAB = True if np.sign(r) <= 0 else False

        r = np.dot(directionVector, nobc)
        insideOBC = True if np.sign(r) <= 0 else False
        
        r = np.dot(directionVector, nocd)
        insideOCD = True if np.sign(r) <= 0 else False
        
        r = np.dot(directionVector, noad)
        insideOAD = True if np.sign(r) <= 0 else False

        directionVector = dot.subtract(A).toList()
        r = np.dot(directionVector, nabc)
        insideABC = True if np.sign(r) <= 0 else False
        
        return insideOAB and insideOBC and insideOCD and insideOAD and insideABC

    def lineToInframePartLine(self, line : Line) -> Line:
        A, B = None, None
        
        if self.dotIsInFrame(line.startDot):
            A = line.startDot
        if self.dotIsInFrame(line.endDot):
            B = line.endDot
        if A is not None and B is not None:
            return Line(A, B)
        
        # плоскости пирамиды кадра формата (вектор нормали; точка плоскости)
        surfaces = self.getFramePyramidSurfaces()
        for surf in surfaces:
            planeNormalVector = surf[0]
            planePoint = surf[1]
            dotIntersects = Geometry.lineIntersectsPlane(line, planeNormalVector, planePoint)
            if dotIntersects is None:
                continue
            if self.dotIsInFrame(dotIntersects):
                if A is None:
                    A = dotIntersects
                elif not A.equal(dotIntersects):
                    B = dotIntersects
        if A is None and B is None:
            return None
        if A is None:
            return Line(B, B)
        if B is None:
            return Line(A, A)
        if A.equal(B):
            return Line(A, A)
        return Line(A, B)
    
    def lineIsInFrame(self, line : Line) -> bool:
        surfaces = self.getFramePyramidSurfaces()
        for surf in surfaces:
            planePoint = surf[0]
            planeNormalVector = surf[1]
            dotIntersects = Geometry.lineIntersectsPlane(line, planePoint, planeNormalVector)
            if self.dotIsInFrame(dotIntersects) is not None:
                return True
        return False

    def getMaxDistanceDot(self) -> Dot:
        A, B, C, D = self.getFrameABCD()
        return A.add(C.subtract(A).divide(2))

    def getFrameABCD(self) -> tuple:
        return self.frameLines[0].endDot, self.frameLines[1].endDot, self.frameLines[2].endDot, self.frameLines[3].endDot
    
    def getFramePyramidSurfaceNormales(self) -> tuple:
        A, B, C, D = self.getFrameABCD()
        O = self.position
        noab = np.cross(A.subtract(O).toList(), B.subtract(O).toList())
        nobc = np.cross(B.subtract(O).toList(), C.subtract(O).toList())
        nocd = np.cross(C.subtract(O).toList(), D.subtract(O).toList())
        noad = np.cross(D.subtract(O).toList(), A.subtract(O).toList())
        nabc = np.cross(C.subtract(B).toList(), B.subtract(B).toList())
        return noab, nobc, nocd, noad, nabc

    def getFramePyramidSurfaces(self) -> list:
        A, B, C, D = self.getFrameABCD()
        O = self.position

        # нормали граней пирамиды
        noab, nobc, nocd, noad, nabc = self.getFramePyramidSurfaceNormales()
        surfaces = [(noab, A), (nobc, B), (nocd, C), (noad, D), (nabc, A)]
        return surfaces

    def dotToFrameXY(self, dot : Dot) -> tuple:
        distance = self.distanceToDot(dot)
        scale = 1 - self.scaleToDot(dot)
        
        A, B, C, D = self.getFrameABCD()
        maxDistanceCenter = Geometry.calculateRectangleCenter(A, B, C, D)
        # прямоугольник содержащий точку (сечение пирамиды кадра)
        center = self.position.add(maxDistanceCenter.subtract(self.position).multiply(scale))
        width = self.frameWidth * (self.maxDistance / self.focusDistance) * scale
        height = self.frameHeight * (self.maxDistance / self.focusDistance) * scale
        if width == 0 or height == 0:
            return (-1, -1)
        rectangle1 = Geometry.calculateRectangleVertexes(center, width, height, self.horizontalAngle, self.verticalAngle)
        
        A1, B1, C1, D1 = rectangle1[0], rectangle1[1], rectangle1[2], rectangle1[3]
        # abs/rel расстояние от левой стороны пирамиды кадра
        w = Line(D1, C1).distanceToDot(dot)
        relativeX = w / width
        # abs/rel расстояние от верхней стороны пирамиды кадра
        h = Line(B1, C1).distanceToDot(dot)
        relativeY = h / height

        x, y = relativeX * self.frameWidth, relativeY * self.frameHeight

        return x, y