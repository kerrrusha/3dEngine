import pygame
from axis import Axis

from lib import *
from dot import Dot
from line import Line
from camera import Camera
from fontImpoved import FontImproved
from objectController import Direction, ObjectController
from shape import Shape

class Scene:
    def __init__(self, screen : pygame.Surface, objects=[], cameraPos=Dot(), horizontalAngle=0, verticalAngle=0) -> None:
        self.screen = screen
        
        self.objects = objects
        self.objectController = ObjectController(self.objects)
        self.shapes = []

        self.camera = Camera(cameraPos, horizontalAngle, verticalAngle)

        self.frameRect = self.calculateFrameRect()

    def calculateFrameRect(self):
        scale = self.screen.get_height() / self.camera.frameHeight
        
        width = self.camera.frameWidth * scale
        height = self.camera.frameHeight * scale
        rect = pygame.Rect(0,0, width, height)
        rect.center = (self.screen.get_width() / 2, self.screen.get_height() / 2)
        
        return rect

    def toScreenXY(self, frameXY : tuple) -> tuple:
        x = self.frameRect.left + (frameXY[0] / self.camera.frameWidth) * self.frameRect.width
        y = self.frameRect.top + (frameXY[1] / self.camera.frameHeight) * self.frameRect.height
        return x, y

    def getObjectsInFrame(self) -> list:
        objectsInFrame = []
        for obj in self.objects:
            if type(obj) is Dot and self.camera.dotIsInFrame(obj):
                objectsInFrame.append(obj)
            if type(obj) is Line and self.camera.lineIsInFrame(obj):
                objectsInFrame.append(obj)
        return objectsInFrame

    def addShape(self, shape : Shape):
        self.shapes.append(shape)
        self.objects.extend(shape.dots)
        self.objectController.update(shapes=self.shapes)

    def addShapes(self, shapes : list[Shape]):
        for sh in shapes:
            self.addShape(sh)

    def update(self):
        self.objectController.rotateCircles(direction=Direction.backward, angleStep=0.5)
        # self.objectController.moveDotsForward()

    def draw(self, debug=False, fps=None):
        for obj in self.getObjectsInFrame():
            if type(obj) is Dot:
                dotFrameXY = self.camera.dotToFrameXY(obj)
                distance = self.camera.distanceToDot(obj)
                scale = self.camera.scaleToDot(obj)
                
                dotScreenXY = self.toScreenXY(dotFrameXY)

                MAX_RADIUS = 1
                radius = MAX_RADIUS*scale if MAX_RADIUS*scale >= 1 else 1
                pygame.draw.circle(self.screen, colors['white'], dotScreenXY, radius)
            if type(obj) is Line:
                lineframePartLine = self.camera.lineToInframePartLine(obj)
                if lineframePartLine is None:
                    continue

                lineFrameXY = self.camera.dotToFrameXY(lineframePartLine.startDot),  self.camera.dotToFrameXY(lineframePartLine.endDot)
                distance = self.camera.distanceToLine(obj)
                scale = self.camera.scaleToLine(obj)

                lineScreenXY = self.toScreenXY(lineFrameXY[0]), self.toScreenXY(lineFrameXY[1])
                
                MAX_WIDTH = 3
                width = MAX_WIDTH*scale if MAX_WIDTH*scale >= 1 else 1
                pygame.draw.line(self.screen, colors['white'], lineScreenXY[0], lineScreenXY[1], int(width))

        if debug:
            msgList = []
            if fps is not None:
                msgList.append(f"FPS: {fps}")
            for obj in self.getObjectsInFrame():
                if type(obj) is Dot:
                    dot = obj
                    msgList.append(f"dotID={dot.id} ({round(dot.x,3)}, {round(dot.y,3)}, {round(dot.z,3)})")
            self.debugDraw(msgList)

    def drawCameraFrameRect(self):
        pygame.draw.rect(self.screen, colors['blue'], self.frameRect, 2)

    def debugDraw(self, msgList):
        self.drawCameraFrameRect()

        font = FontImproved('consolas', 14)
        paddingY = 30
        pos = (self.screen.get_width() - 250, 20)

        for i in range(len(msgList)):
            self.screen.blit(font.render(str(msgList[i]), 1, colors['green']), (pos[0], pos[1] + i*paddingY))