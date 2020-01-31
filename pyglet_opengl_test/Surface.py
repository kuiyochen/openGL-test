# http://www.poketcode.com/en/pyglet_demos/index.html
import os
import numpy as np
from colorsys import hsv_to_rgb

from PIL import Image
import pyglet
from pyglet import gl
from pyglet.gl import glu


class Surface:
    def __init__(self):
        self.vertices = []
        # translation and rotation values
        self.x = self.y = 0  # heightmap translation
        self.z = -100
        self.rx = self.ry = self.rz = 0  # heightmap rotation

    def load(self, mx, my, mz, dx, dy, dz):
        self.width, self.height = mz.shape

        # loads the vertices
        for j in range(self.height - 1):
            # a row of triangles
            row = []
            for i in range(self.width):
                row.extend((mx[i, j] * dx, - my[i, j] * dy, mz[i, j] * dz))
                row.extend((mx[i, j + 1] * dx, - my[i, j + 1] * dy, mz[i, j + 1] * dz))
            self.vertices.append(row)

        self.colormax = np.array(self.vertices).reshape(-1, 3)[:, 2]
        self.colormin = np.amin(self.colormax)
        self.colormax = np.amax(self.colormax)

    def draw(self, c):
        gl.glLoadIdentity()
        gl.glTranslatef(self.x, self.y, self.z)
        # rotation
        gl.glRotatef(self.rx - 40, 1, 0, 0)
        gl.glRotatef(self.ry, 0, 1, 0)
        gl.glRotatef(self.rz - 40, 0, 0, 1)
        # color
        gl.glColor3f(*gray)

        # draws the primitives (GL_TRIANGLE_STRIP)
        for row in self.vertices:
            row = np.array(row).reshape(-1, 3)
            color = (row[:, 2] - self.colormin) / (self.colormax - self.colormin)
            if c == 'b':
                color = np.column_stack([1 - color, 1 - color, np.ones_like(color), np.zeros_like(color) + 0.7]).reshape(-1)
            if c == 'g':
                color = np.column_stack([1 - color, np.ones_like(color), 1 - color, np.zeros_like(color) + 0.7]).reshape(-1)

            row = row.reshape(-1)
            pyglet.graphics.draw(self.width * 2, gl.GL_TRIANGLE_STRIP, ('v3f', row), ('c4f', color))

    # @window.event
    def surface_on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # scroll the MOUSE WHEEL to zoom
        with np.errstate(divide = 'ignore', over = 'ignore'):
            self.z += scroll_y * 5 * (1 + 1 / (1 + np.exp((self.z + 5) * 5)**(-1)))
    # @window.event
    def surface_MOD_CTRL_mouse_LEFT(self, x, y, dx, dy, button, modifiers):
        self.rz -= dx / 5.0
        self.rz += dy / 5.0
    # @window.event
    def surface_mouse_MIDDLE(self, x, y, dx, dy, button, modifiers):
        self.x += dx / 10.0
        self.y += dy / 10.0
    # @window.event
    def surface_mouse_LEFT(self, x, y, dx, dy, button, modifiers):
        self.ry += dx / 5.0
        self.rx -= dy / 5.0

class Point_dot:
    def __init__(self):
        # translation and rotation values
        self.x = self.y = 0  # heightmap translation
        self.z = -100
        self.rx = self.ry = self.rz = 0  # heightmap rotation

    def load(self, points, pointsize):
        self.points = np.array(points)
        self.pointsize = pointsize
        self.data_points_color = self.color_plot()

    def color_plot(self):
        h = self.points[:, 2]
        if np.max(h) == np.min(h):
            return np.column_stack([np.ones_like(h)] * 3)
        h = (h - np.min(h)) / (np.max(h) - np.min(h))
        h = h * 0.8 + 0.2
        return np.array(list(map(lambda x: hsv_to_rgb(x, 1., 1.), h)))

    def draw(self):
        gl.glLoadIdentity()
        gl.glTranslatef(self.x, self.y, self.z)
        # rotation
        gl.glRotatef(self.rx - 40, 1, 0, 0)
        gl.glRotatef(self.ry, 0, 1, 0)
        gl.glRotatef(self.rz - 40, 0, 0, 1)
        # color
        gl.glColor3f(*gray)

        gl.glPointSize(self.pointsize)
        pyglet.graphics.draw(len(self.points), gl.GL_POINTS, #v3f/stream c4B/static
            ('v3f', self.points.reshape(-1)),
            ('c3f', self.data_points_color.reshape(-1)))

    # @window.event
    def Point_dot_on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # scroll the MOUSE WHEEL to zoom
        with np.errstate(divide = 'ignore', over = 'ignore'):
            self.z += scroll_y * 5 * (1 + 1 / (1 + np.exp((self.z + 5) * 5)**(-1)))
    # @window.event
    def Point_dot_MOD_CTRL_mouse_LEFT(self, x, y, dx, dy, button, modifiers):
        self.rz -= dx / 5.0
        self.rz += dy / 5.0
    # @window.event
    def Point_dot_mouse_MIDDLE(self, x, y, dx, dy, button, modifiers):
        self.x += dx / 10.0
        self.y += dy / 10.0
    # @window.event
    def Point_dot_mouse_LEFT(self, x, y, dx, dy, button, modifiers):
        self.ry += dx / 5.0
        self.rx -= dy / 5.0

# colors
black = (0, 0, 0, 1)
gray = (0.5, 0.5, 0.5)
width = 800
height = 800

window = pyglet.window.Window(width=width, height=height, caption='Surface', resizable=True)

# background color
gl.glClearColor(*black)

pyglet.graphics.glEnable(pyglet.graphics.GL_DEPTH_TEST)
# gl.glEnable(gl.GL_LINE_SMOOTH)
# gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_DONT_CARE)
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
# gl.glEnable(gl.GL_CULL_FACE)

# Surface
surface = Surface()
# surface.load('surface_64-2.png', 1, 1, .1)
surface1 = Surface()
# surface1.load('surface_64-1.png', 1, 1, .1)

x = np.arange(-50, 50, 1)
y = np.arange(-100, 100, 1)
mx, my = np.meshgrid(x, y, indexing='ij')
mz = (mx**2 + my**2) / (5 * 10**2) + 10
surface.load(mx, my, mz, 1, 1, 1)
x = np.arange(-60, 60, 1)
y = np.arange(-60, 60, 1)
mx1, my1 = np.meshgrid(x, y, indexing='ij')
mz1 = ((mx1 + 30)**2 + my1**2) / (10**3) + 15
surface1.load(mx1, my1, mz1, 1, 1, 1)

# data_points = np.array([[10.0, 10.0, 20], 
#                         [13.0, 13.0, 10]])
# data_points_color = np.array([[255, 0, 0, 255//2], 
#                         [255, 255, 0, 255//2]])
data_points = Point_dot()
data_points.load(np.column_stack([np.arange(-10, 10, 1), 
                        np.arange(-10, 10, 1) + 10,
                        np.arange(-10, 10, 1) + 10]), 5)

@window.event
def on_resize(width, height):
    # sets the viewport
    gl.glViewport(0, 0, width, height)

    # sets the projection
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    glu.gluPerspective(60.0, width / float(height), 0.1, 1000.0)

    # sets the model view
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()

    return pyglet.event.EVENT_HANDLED

@window.event
def on_draw():

    # clears the background with the background color
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    # wire-frame mode
    gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)

    data_points.draw()

    # gl.glPointSize(10)
    # pyglet.graphics.draw(len(data_points), gl.GL_POINTS, #v3f/stream c4B/static
    #         ('v3f', data_points.reshape(-1)),
    #         ('c4B', data_points_color.reshape(-1)))
    # gl.glPointSize(1)

    # gl.glBegin(gl.GL_POINTS)
    gl.glBegin(gl.GL_LINES)
    gl.glColor4fv((gl.GLfloat * 4)(1, 0, 0, 1))
    gl.glVertex3f(10.0, 10.0, 20)
    gl.glVertex3f(0.0, 0.0, 20)
    gl.glEnd()

    surface.draw('b')
    surface1.draw('g')

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    # scroll the MOUSE WHEEL to zoom
    surface.surface_on_mouse_scroll(x, y, scroll_x, scroll_y)
    surface1.surface_on_mouse_scroll(x, y, scroll_x, scroll_y)
    data_points.Point_dot_on_mouse_scroll(x, y, scroll_x, scroll_y)

@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
    key = pyglet.window.key
    if button == pyglet.window.mouse.LEFT and (modifiers & key.MOD_CTRL):
        surface.surface_MOD_CTRL_mouse_LEFT(x, y, dx, dy, button, modifiers)
        surface1.surface_MOD_CTRL_mouse_LEFT(x, y, dx, dy, button, modifiers)
        data_points.Point_dot_MOD_CTRL_mouse_LEFT(x, y, dx, dy, button, modifiers)
        return
    #   print("YOO")
    # press the LEFT and RIGHT MOUSE BUTTON simultaneously to pan
    if button == pyglet.window.mouse.MIDDLE:
        surface.surface_mouse_MIDDLE(x, y, dx, dy, button, modifiers)
        surface1.surface_mouse_MIDDLE(x, y, dx, dy, button, modifiers)
        data_points.Point_dot_mouse_MIDDLE(x, y, dx, dy, button, modifiers)


        return
    # press the LEFT MOUSE BUTTON to rotate
    if button == pyglet.window.mouse.LEFT:
        surface.surface_mouse_LEFT(x, y, dx, dy, button, modifiers)
        surface1.surface_mouse_LEFT(x, y, dx, dy, button, modifiers)
        data_points.Point_dot_mouse_LEFT(x, y, dx, dy, button, modifiers)


pyglet.app.run()
