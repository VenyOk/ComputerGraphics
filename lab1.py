import pygame
from pygame.locals import *
from OpenGL.GL import *
from math import sin, cos, radians

pygame.init()

display = (600, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Поворот правильного шестиугольника на 30 градусов при нажатии на пробел
def main():
    angle = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    angle += 30

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glRotatef(angle, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)
        init_figure()
        pygame.display.flip()


def init_figure():
    glBegin(GL_POLYGON)
    for i in range(6):
        angle = i * 60
        x = 0.2 * cos(radians(angle))
        y = 0.2 * sin(radians(angle))
        glVertex2f(x, y)
    glEnd()


if __name__ == "__main__":
    main()
