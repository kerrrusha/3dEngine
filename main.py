import math
import pygame
from axis import Axis

from lib import *
from dot import Dot
from scene import Scene

WIDTH = 1000
HEIGHT = 600
FPS = 30            # Frame Per Second - кадров в секунду

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3d Visualiser")
clock = pygame.time.Clock()

# objects = [Dot(99, -99, -99), Dot(99, 99, 99), Dot(50, 0, 0)]
objects = []

axis = Axis.x
center = Dot(100, 0, 0)
radius = 20
angle = 0
for i in range(30):
    angle += i * 3.6
    x = center.x
    y = center.y + radius * math.sin(angle)
    z = center.z + radius * math.cos(angle)
    objects.append(Dot(x, y, z))
for i in range(20):
    angle += i * 3.6
    x = center.x - 20
    y = center.y + radius * math.sin(angle)
    z = center.z + radius * math.cos(angle)
    objects.append(Dot(x, y, z))
for i in range(30):
    angle += i * 3.6
    x = center.x - 40
    y = center.y + radius * math.sin(angle)
    z = center.z + radius * math.cos(angle)
    objects.append(Dot(x, y, z))
scene = Scene(screen, objects)

running = True
while running:          #основной игровой цикл
    clock.tick(FPS)     #поддержание одинакового фпс
    
    for event in pygame.event.get():    # проверка событий
        if event.type == pygame.QUIT:   # обработка закрытия окна
            running = False

    # логика
    scene.update()
    
    # предварительная отрисовка
    screen.fill(colors["black"])
    scene.draw(debug=False, fps=int(clock.get_fps()))
    
    # показываем кадр
    pygame.display.flip()   

pygame.quit()