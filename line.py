import numpy as np
from dot import Dot
import math

class Line:
    def __init__(self) -> None:
        self.startDot = Dot()
        self.endDot = Dot()

    def __init__(self, startDot : Dot, endDot : Dot) -> None:
        self.startDot = startDot
        self.endDot = endDot

    def length(self):
        return math.sqrt( 
            (self.endDot.x - self.startDot.x) ** 2 + 
            (self.endDot.y - self.startDot.y) ** 2 + 
            (self.endDot.z - self.startDot.z) ** 2
        )

    def distanceToDot(self, dot : Dot) -> float:
        if self.length() == 0:
            return self.startDot.distanceTo(dot)
        return np.linalg.norm(np.cross(self.endDot.subtract(self.startDot).toList(), self.startDot.subtract(dot).toList())) / np.linalg.norm(self.endDot.subtract(self.startDot).toList())