import glfw
from OpenGL.GL import *
import numpy as np
from OpenGL.raw.GLU import gluPerspective

WIDTH, HEIGHT = 800, 600
rotate_x, rotate_y = 0, 0


def cone():
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(0, 0, -1)
    num_segments = 200
    for i in range(num_segments + 1):
        theta = 2.0 * np.pi * i / num_segments
        x = np.cos(theta)
        y = np.sin(theta)
        glVertex3f(x, y, -1)
    glEnd()

    glBegin(GL_TRIANGLE_FAN)
    glColor3f(0.7, 0.7, 0.7)
    glVertex3f(0, 0, 1)
    for i in range(num_segments + 1):
        theta = 2.0 * np.pi * i / num_segments
        x = np.cos(theta)
        y = np.sin(theta)
        glVertex3f(x, y, -1)
    glEnd()


def draw():
    global rotate_x, rotate_y
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5.0)
    glRotatef(rotate_x, 1, 0, 0)
    glRotatef(rotate_y, 0, 1, 0)
    cone()
    glfw.swap_buffers(window)


def key_callback(window, key, scancode, action, mods):
    global rotate_x, rotate_y
    if key == glfw.KEY_UP:
        rotate_x += 5
    elif key == glfw.KEY_DOWN:
        rotate_x -= 5
    elif key == glfw.KEY_LEFT:
        rotate_y -= 5
    elif key == glfw.KEY_RIGHT:
        rotate_y += 5


def main():
    global window
    if not glfw.init():
        return
    window = glfw.create_window(WIDTH, HEIGHT, "Cone with Rotation", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, WIDTH / HEIGHT, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        draw()
    glfw.terminate()


if __name__ == "__main__":
    main()
