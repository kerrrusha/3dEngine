import pygame
from lib import *

class FontImproved:
    def __init__(self, fontName, size, color=colors["black"]):
        self.fontName = fontName
        self.size = size
        self.font = pygame.font.SysFont(fontName, size)
        self.color = color
    
    def render(self, text, bool, color=None):
        textColor = self.color if color is None else color
        return self.font.render(text, bool, textColor)