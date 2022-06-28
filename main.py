import math
import pygame
from axis import Axis

from lib import *
from dot import Dot
from line import Line
from scene import Scene
from shape import Circle

WIDTH = 1000
HEIGHT = 600
FPS = 30            # Frame Per Second - кадров в секунду

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3d Engine")
clock = pygame.time.Clock()

# objects = [Dot(99, -99, -99), Dot(99, 99, 99), Dot(50, 0, 0)]
# objects = []

# center = Dot(20, 0, 0)
# radius = 10
# dots = 36
# for i in range(dots):
#     rads = math.radians(i * 360 / dots)
#     x = center.x
#     y = center.y + radius * math.cos(rads)
#     z = center.z + radius * math.sin(rads)
#     objects.append(Dot(x, y, z))

# центры кругов
shapesCenter = Dot(13, 0, 12.5)
radius = 7.5
N = 25
centers = []
for i in range(N):
    rads = math.radians(i * 360 / N)
    x = shapesCenter.x
    y = shapesCenter.y + radius * math.cos(rads)
    z = shapesCenter.z + radius * math.sin(rads)
    centers.append(Dot(x, y, z))

# круги
axis = Axis.y
radius = 7
N = 25
shapes = []
for center in centers:
    shapes.append(Circle.createCircle(center, radius, axis, N),)

# line = Line(Dot(50, -100, 10), Dot(50, 100, -10))
# axisX = Line(Dot(-200, 0, 0), Dot(200, 0, 0))
# axisY = Line(Dot(0, -200, 0), Dot(0, 200, 0))
# axisZ = Line(Dot(0, 0, -200), Dot(0, 0, 200))
# objects = [axisX, axisY, axisZ]
scene = Scene(screen)
scene.addShapes(shapes)

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