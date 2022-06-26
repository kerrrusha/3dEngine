import pygame
from axis import Axis

from lib import *
from dot import Dot
from line import Line
from camera import Camera
from fontImpoved import FontImproved
from objectController import ObjectController

class Scene:
    def __init__(self, screen : pygame.Surface, objects=[]) -> None:
        self.screen = screen
        
        self.objects = objects
        self.objectController = ObjectController(self.objects)
        
        self.camera = Camera()

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
        return objectsInFrame

    def update(self):
        # self.objectController.rotateAll(Dot(10, 0, 25))
        self.objectController.moveForwardAll()

    def draw(self, debug=False, fps=None):
        for obj in self.getObjectsInFrame():
            if type(obj) is Dot:
                dotFrameXY = self.camera.dotToFrameXY(obj)
                distance = self.camera.distanceTo(obj)
                scale = self.camera.scaleTo(obj)
                
                dotScreenXY = self.toScreenXY(dotFrameXY)

                MAX_RADIUS = 3
                radius = MAX_RADIUS*scale if MAX_RADIUS*scale >= 1 else 1
                pygame.draw.circle(self.screen, colors['white'], dotScreenXY, radius)

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