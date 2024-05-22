import glfw
from OpenGL.GL import *
import time
import collections
size = 300
pixels = [255] * (size * size * 3)
points = []

def sign(a, b):
    if a > b:
        return -1
    return 1

def bresenhamfloat(x1, y1, x2, y2, color):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    sx = sign(x1, x2)
    sy = sign(y1, y2)
    if dx > dy:
        err = dx / 2.0
        while x != x2:
            if 0 <= x < size and 0 <= y < size:
                position = (x + y * size) * 3
                pixels[position] = color[0]
                pixels[position + 1] = color[1]
                pixels[position + 2] = color[2]
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y2:
            if 0 <= x < size and 0 <= y < size:
                position = (x + y * size) * 3
                pixels[position] = color[0]
                pixels[position + 1] = color[1]
                pixels[position + 2] = color[2]
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    if 0 <= x < size and 0 <= y < size:
        position = (x + y * size) * 3
        pixels[position] = color[0]
        pixels[position + 1] = color[1]
        pixels[position + 2] = color[2]


### Сазерленд-Ходжман
def is_inside(p1, p2, q):
    R = (p2[0] - p1[0]) * (q[1] - p1[1]) - (p2[1] - p1[1]) * (q[0] - p1[0])
    return R <= 0

def compute_intersection(p1, p2, p3, p4):
    if p2[0] - p1[0] == 0:
        x = p1[0]

        m2 = (p4[1] - p3[1]) / (p4[0] - p3[0])
        b2 = p3[1] - m2 * p3[0]

        y = m2 * x + b2

    elif p4[0] - p3[0] == 0:
        x = p3[0]

        m1 = (p2[1] - p1[1]) / (p2[0] - p1[0])
        b1 = p1[1] - m1 * p1[0]

        y = m1 * x + b1

    else:
        m1 = (p2[1] - p1[1]) / (p2[0] - p1[0])
        b1 = p1[1] - m1 * p1[0]

        m2 = (p4[1] - p3[1]) / (p4[0] - p3[0])
        b2 = p3[1] - m2 * p3[0]

        x = (b2 - b1) / (m1 - m2)

        y = m1 * x + b1

    intersection = (x, y)

    return intersection


def clip(subject_polygon, clipping_polygon):
    final_polygon = subject_polygon.copy()

    for i in range(len(clipping_polygon)):

        next_polygon = final_polygon.copy()

        final_polygon = []

        c_edge_start = clipping_polygon[i - 1]
        c_edge_end = clipping_polygon[i]

        for j in range(len(next_polygon)):

            s_edge_start = next_polygon[j - 1]
            s_edge_end = next_polygon[j]

            if is_inside(c_edge_start, c_edge_end, s_edge_end):
                if not is_inside(c_edge_start, c_edge_end, s_edge_start):
                    intersection = compute_intersection(s_edge_start, s_edge_end, c_edge_start, c_edge_end)
                    final_polygon.append(intersection)
                final_polygon.append(tuple(s_edge_end))
            elif is_inside(c_edge_start, c_edge_end, s_edge_start):
                intersection = compute_intersection(s_edge_start, s_edge_end, c_edge_start, c_edge_end)
                final_polygon.append(intersection)
    return final_polygon


def draw_window():
    bresenhamfloat(100, 100, 100, 200, [255, 0, 0])
    bresenhamfloat(100, 200, 200, 200, [255, 0, 0])
    bresenhamfloat(200, 200, 200, 100, [255, 0, 0])
    bresenhamfloat(200, 100, 100, 100, [255, 0, 0])

def mouse_button_callback(window, button, action, mods):
    global points, edges, size
    if action == glfw.PRESS and button == glfw.MOUSE_BUTTON_LEFT:
        x, y = glfw.get_cursor_pos(window)
        y = size - y
        points.append((int(x), int(y)))
        redraw_polygon(points,  [0, 0, 0])

def redraw_polygon(array, color):
    global pixels, points, edges, size
    pixels = [255] * (size * size * 3)
    for i in range(1, len(array)):
        bresenhamfloat(int(array[i - 1][0]), int(array[i - 1][1]), int(array[i][0]), int(array[i][1]), color)

    if len(array) > 2:
        bresenhamfloat(int(array[-1][0]), int(array[-1][1]), int(array[0][0]), int(array[0][1]), color)

def fill(x, y):
    q = collections.deque([(x, y)])
    while q:
        x, y = q.popleft()
        current_pos = (x + y * size) * 3
        if x < 0 or x >= size or y < 0 or y >= size:
            continue
        if pixels[current_pos] == pixels[current_pos + 1] == pixels[current_pos + 2] == 255:
            if 0 <= x < size and 0 <= y < size:
                position = (x + y * size) * 3
                pixels[position] = 0
                pixels[position + 1] = 0
                pixels[position + 2] = 0
            q.append((x + 1, y))
            q.append((x - 1, y))
            q.append((x, y + 1))
            q.append((x, y - 1))


def apply_post_filter(N):
    global pixels, size
    filtered_pixels = pixels.copy()

    radius = N // 2
    weights = [[1, 2, 1],
               [2, 4, 2],
               [1, 2, 1]]

    for y in range(size):
        for x in range(size):
            sum_r = sum_g = sum_b = 0
            weight_sum = 0

            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < size and 0 <= ny < size:
                        index = (ny * size + nx) * 3
                        weight = weights[dy + radius][dx + radius]
                        sum_r += pixels[index] * weight
                        sum_g += pixels[index + 1] * weight
                        sum_b += pixels[index + 2] * weight
                        weight_sum += weight

            avg_r = int(sum_r / weight_sum)
            avg_g = int(sum_g / weight_sum)
            avg_b = int(sum_b / weight_sum)

            index = (y * size + x) * 3
            filtered_pixels[index] = avg_r
            filtered_pixels[index + 1] = avg_g
            filtered_pixels[index + 2] = avg_b

    pixels = filtered_pixels

def key_callback(window, key, scancode, action, mods):
    global pixels, points, edges, size
    if action == glfw.PRESS:
        if key == glfw.KEY_SPACE:
            if len(points) > 2:
                clipped_polygon = clip(points, [(100, 100), (100, 200), (200, 200), (200, 100)])
                print("Отсеченный многоугольник: ", *clipped_polygon)
                print("Точки: ", *points)
                redraw_polygon(clipped_polygon, [0, 0, 0])
                min_x = min(points, key=lambda x: x[0])[0]
                max_x = max(points, key=lambda x: x[0])[0]
                min_y = min(points, key=lambda x: x[1])[1]
                max_y = max(points, key=lambda x: x[1])[1]
                x = (min_x + max_x) // 2
                y = (min_y + max_y) // 2
                if x and y:
                   fill(x, y)
                apply_post_filter(N=3)
        elif key == glfw.KEY_BACKSPACE:
            points = []
            pixels = [255] * (size * size * 3)



def display(window):
    glClear(GL_COLOR_BUFFER_BIT)
    draw_window()
    glDrawPixels(size, size, GL_RGB, GL_UNSIGNED_BYTE, pixels)

    glfw.swap_buffers(window)
    glfw.poll_events()
def main():
    if not glfw.init():
        return
    window = glfw.create_window(size, size, "Lab5", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)

    glClearColor(1.0, 1.0, 1.0, 1.0)

    while not glfw.window_should_close(window):
        display(window)

    glfw.terminate()


if __name__ == "__main__":
    main()