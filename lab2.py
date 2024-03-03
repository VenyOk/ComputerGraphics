#!/usr/bin/env python3

import glfw
from OpenGL.GL import *

alpha = 0.0
beta = 0.0
gamma = 0.0
fill = True


def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, "Lab 2", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()


def display(window):
    global alpha, beta, gamma
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)

    def projection_x():
        glMultMatrixf([0, 0, -1, 0,
                       0, 1, 0, 0,
                       -1, 0, 0, 0,
                       0, 0, 0, 1])

    def projection_y():
        glMultMatrixf([1, 0, 0, 0,
                       0, 0, -1, 0,
                       0, -1, 0, 0,
                       0, 0, 0, 1])

    def projection_z():
        glMultMatrixf([1, 0, 0, 0,
                       0, 1, 0, 0,
                       0, 0, -1, 0,
                       0, 0, 0, 1])

    def cube(sz):
        glBegin(GL_QUADS)
        glColor3f(0.0, 0.0, 1.0);
        glVertex3f(-sz / 2, -sz / 2, -sz / 2)
        glVertex3f(-sz / 2, sz / 2, -sz / 2)
        glVertex3f(-sz / 2, sz / 2, sz / 2)
        glVertex3f(-sz / 2, -sz / 2, sz / 2)
        glColor3f(1.0, 0.0, 0.0);
        glVertex3f(sz / 2, -sz / 2, -sz / 2)
        glVertex3f(sz / 2, -sz / 2, sz / 2)
        glVertex3f(sz / 2, sz / 2, sz / 2)
        glVertex3f(sz / 2, sz / 2, -sz / 2)
        glColor3f(0.0, 1.0, 0.0);
        glVertex3f(-sz / 2, -sz / 2, -sz / 2)
        glVertex3f(-sz / 2, -sz / 2, sz / 2)
        glVertex3f(sz / 2, -sz / 2, sz / 2)
        glVertex3f(sz / 2, -sz / 2, -sz / 2)
        glColor3f(1.0, 1.0, 0.0);
        glVertex3f(-sz / 2, sz / 2, -sz / 2)
        glVertex3f(-sz / 2, sz / 2, sz / 2)
        glVertex3f(sz / 2, sz / 2, sz / 2)
        glVertex3f(sz / 2, sz / 2, -sz / 2)
        glColor3f(0.0, 1.0, 1.0);
        glVertex3f(-sz / 2, -sz / 2, -sz / 2)
        glVertex3f(sz / 2, -sz / 2, -sz / 2)
        glVertex3f(sz / 2, sz / 2, -sz / 2)
        glVertex3f(-sz / 2, sz / 2, -sz / 2)
        glColor3f(1.0, 0.0, 1.0);
        glVertex3f(-sz / 2, -sz / 2, sz / 2)
        glVertex3f(sz / 2, -sz / 2, sz / 2)
        glVertex3f(sz / 2, sz / 2, sz / 2)
        glVertex3f(-sz / 2, sz / 2, sz / 2)
        glEnd()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    projection_x()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(-0.5, 0.5, 0.5)
    glRotatef(alpha, 1, 0, 0)
    glRotatef(beta, 0, 1, 0)
    glRotatef(gamma, 0, 0, 1)
    cube(0.3)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    projection_y()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, 0)
    glRotatef(alpha, 1, 0, 0)
    glRotatef(beta, 0, 1, 0)
    glRotatef(gamma, 0, 0, 1)
    cube(0.3)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    projection_z()
    glTranslatef(0.5, -0.5, 0)
    glRotatef(alpha, 1, 0, 0)
    glRotatef(beta, 0, 1, 0)
    glRotatef(gamma, 0, 0, 1)
    cube(0.3)

    glLoadIdentity()
    glTranslatef(-0.6, -0.6, 0.0)

    alpha += 0.2
    beta += 0.2
    gamma += 0.2
    glRotatef(alpha, 1, 0, 0)
    glRotatef(beta, 0, 1, 0)
    glRotatef(gamma, 0, 0, 1)
    cube(0.4)

    glfw.swap_buffers(window)
    glfw.poll_events()


if __name__ == "__main__":
    main()
