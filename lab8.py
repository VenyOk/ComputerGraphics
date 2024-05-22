import glfw
import numpy as np
from OpenGL.GL import *
import math
from PIL import Image
import time


size = 0.5
angle = 0.0
angle2 = 0
n = 50
flag = True
texture = 0
speed = 0
direction = [0, 1, 0, 5]
delta_x = 0
delta_y = 0.5
delta_z = 0

im = Image.open('texture.jpg')
width = im.width
height = im.height

l_frame = 0.0
f_count = 0
fps = 0.0

display_list = 0
vbo = 0

vertices = []
normals = []
indices = []

fps_list = [('Number', 'FPS')]
fps_count = 0


def create_shader(type, code):
    shader = glCreateShader(type)
    glShaderSource(shader, code)
    glCompileShader(shader)
    return shader


def getnorm(a, b, c):
    mult = 0
    n = [0] * 3
    n[0] = (b[1] - a[1]) * (c[2] - a[2]) - (b[2] - a[2]) * (c[1] - a[1])
    n[1] = (c[0] - a[0]) * (b[2] - a[2]) - (b[0] - a[0]) * (c[2] - a[2])
    n[2] = (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])
    for i in range(3):
        mult += a[i] * n[i]
    if mult < 0:
        for j in range(3):
            n[j] = -n[j]
    a = [b[0] - a[0], b[1] - a[1], b[2] - a[2]]
    b = [c[0] - a[0], c[1] - a[1], c[2] - a[2]]
    return np.cross(a, b)


def drawsq():
    global size, delta_x, delta_y, delta_z
    global vertices, normals, indices, display_list

    display_list = glGenLists(1)
    glNewList(display_list, GL_COMPILE)

    for j in range(1, n):
        i = 0
        glBegin(GL_QUAD_STRIP)
        while i <= 2 * math.pi:
            m = size - j / n * size
            m_pred = size - (j - 1) / n * size
            x = m * math.cos(i) * math.cos(j / n) + delta_x
            x_pred = m_pred * math.cos(i) * math.cos((j - 1) / n) + delta_x
            y = m * math.sin(i) * math.cos(j / n) + delta_y
            y_pred = m_pred * math.sin(i) * math.cos((j - 1) / n) + delta_y
            z = j / n + delta_z
            z_pred = (j - 1) / n + delta_z
            glColor3f(1, 1, 1)
            norm = getnorm([x_pred, y_pred, (j - 1 / n)], [x, y, j / n],
                           [m * math.cos(i + math.pi / 2) * math.cos(j / n),
                            m * math.sin(i + math.pi / 2) * math.cos(j / n), j / n])
            glNormal3d(norm[0], norm[1], norm[2])
            glTexCoord2f(i / (2 * math.pi), 1)

            glVertex3f(x, y, z)
            glTexCoord2f(0, i / (2 * math.pi))
            glVertex3f(x_pred, y_pred, z_pred)

            i += math.pi / 2
        glEnd()
    glEndList()

vertices = []


def create_vbo():
    global vbo

    for j in range(1, n):
        i = 0
        while i <= 2 * math.pi:
            m = size - j / n * size
            m_pred = size - (j - 1) / n * size
            x = m * math.cos(i) * math.cos(j / n) + delta_x
            x_pred = m_pred * math.cos(i) * math.cos((j - 1) / n) + delta_x
            y = m * math.sin(i) * math.cos(j / n) + delta_y
            y_pred = m_pred * math.sin(i) * math.cos((j - 1) / n) + delta_y
            z = j / n + delta_z
            z_pred = (j - 1) / n + delta_z
            norm = getnorm([x_pred, y_pred, (j - 1 / n)], [x, y, j / n],
                           [m * math.cos(i + math.pi / 2) * math.cos(j / n),
                            m * math.sin(i + math.pi / 2) * math.cos(j / n), j / n])
            glNormal3d(norm[0], norm[1], norm[2])
            vertices.extend([x, y, z])
            vertices.extend([x_pred, y_pred, z_pred])
            i += math.pi / 2
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, np.array(vertices, dtype=np.float32), GL_STATIC_DRAW)


def draw_with_vbo():
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, None)
    glDrawArrays(GL_QUAD_STRIP, 0, int(len(vertices) / 2))
    glDisableClientState(GL_VERTEX_ARRAY)

def display(window):
    global size, delta_x, delta_y, delta_z, display_list
    glEnable(GL_TEXTURE_2D)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    material_diffuse = [0, 0, 0., 0.]
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, material_diffuse)
    glBindTexture(GL_TEXTURE_2D, texture)

    light3_diffuse = [0.4, 0.7, .1]
    light3_position = [0, 0.25, 1, 3]
    light3_attenuation = [1.0, 0.01, 0.032]

    glLightfv(GL_LIGHT2, GL_DIFFUSE, light3_diffuse)
    glLightfv(GL_LIGHT2, GL_POSITION, light3_position)
    glLightfv(GL_LIGHT2, GL_CONSTANT_ATTENUATION, light3_attenuation[0])
    glLightfv(GL_LIGHT2, GL_LINEAR_ATTENUATION, light3_attenuation[1])
    glLightfv(GL_LIGHT2, GL_QUADRATIC_ATTENUATION, light3_attenuation[2])
    glLightfv(GL_LIGHT2, GL_SPOT_DIRECTION, [0, 0, -1])

    glPointSize(5)
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)

    glTexCoord2f(0, 1)
    glNormal3f(0., 1.1, .0, )
    glVertex3f(-0.7, -0.6, 0.)

    glTexCoord2f(1, 1)
    glVertex3f(0.7, -0.6, 0.)

    glTexCoord2f(1, 0)
    glVertex3f(0.7, 1., .0)

    glTexCoord2f(0, 0)
    glVertex3f(-0.7, 1., .0)

    glEnd()
    glCallList(display_list)
    draw_with_vbo()
    glDisable(GL_TEXTURE_2D)
    if flag:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glPushMatrix()
    glRotatef(angle2, 1, 0, 0)
    glRotate(angle, 0, 0, 1)
    glPushMatrix()
    glPopMatrix()
    glPopMatrix()
    drawsq()

    glfw.swap_buffers(window)
    glfw.poll_events()


def key_callback(window, key, scancode, action, mods):
    global angle, angle2, flag
    if action == glfw.PRESS:
        if key == glfw.KEY_SPACE:
            flag = not flag


def scroll_callback(window, xoffset, yoffset):
    global size
    if xoffset > 0:
        size -= yoffset / 10
    else:
        size += yoffset / 10


def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, "Lab8", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1.2, 1.2, -1.2, 1.2, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    glGenTextures(1, texture)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, im.tobytes())
    glBindTexture(GL_TEXTURE_2D, 0)
    drawsq()
    create_vbo()
    v = create_shader(GL_VERTEX_SHADER, """
                attribute vec3 aVert;
                varying vec3 n;
                varying vec3 v;
                varying vec2 uv;
                //varying vec4 vertexColor;
                void main()
                {   
                    uv = gl_MultiTexCoord0.xy;
                    v = vec3(gl_ModelViewMatrix * gl_Vertex);
                    n = normalize(gl_NormalMatrix * gl_Normal);
                    gl_TexCoord[0] = gl_TextureMatrix[0]  * gl_MultiTexCoord0;
                    gl_Position = gl_ModelViewProjectionMatrix * vec4(gl_Vertex.x, gl_Vertex.y, gl_Vertex.z, 1);
                    //vec4 vertexColor = vec4(0.5f, 0.0f, 0.0f, 1.0f);
                }
                """)
    f = create_shader(GL_FRAGMENT_SHADER, """
            varying vec3 n;
            varying vec3 v; 
            //varying vec4 vertexColor; // Входная переменная из вершинного шейдера (то же название и тот же тип)

            uniform sampler2D tex;
            void main ()  
            {  
                vec3 L = normalize(gl_LightSource[0].position.xyz - v);   
                vec3 E = normalize(-v);
                vec3 R = normalize(-reflect(L,n));  

                //calculate Ambient Term:  
                vec4 Iamb = gl_FrontLightProduct[0].ambient;    

                //calculate Diffuse Term:  
                vec4 Idiff = gl_FrontLightProduct[0].diffuse * max(dot(n,L), 1.0);
                Idiff = clamp(Idiff, 2.0, 0.6);     

                // calculate Specular Term:
                vec4 Ispec = gl_LightSource[0].specular 
                                * pow(max(dot(R,E),0.0),0.7);
                Ispec = clamp(Ispec, 0.0, 1.0); 

                vec4 texColor = texture2D(tex, gl_TexCoord[0].st);
                gl_FragColor = (Idiff + Iamb + Ispec) * texColor;
            }
            """)
    prog = glCreateProgram()
    glAttachShader(prog, v)
    glAttachShader(prog, f)
    glLinkProgram(prog)
    glUseProgram(prog)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        display(window)
    glfw.terminate()

if __name__ == "__main__":
    main()