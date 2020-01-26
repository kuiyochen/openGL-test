# http://www.poketcode.com/en/pyglet_demos/index.html
import os
import numpy as np

from PIL import Image
import pyglet
from pyglet import gl
from pyglet.gl import glu


class Surface:
    def __init__(self):
        self.vertices = []

        # dimensions
        self.x_length = 0
        self.y_length = 0
        self.z_length = 0

        # image dimensions
        self.image_width = 0
        self.image_height = 0

        # translation and rotation values
        self.x = self.y = 0  # heightmap translation
        self.z = -100
        self.rx = self.ry = self.rz = 0  # heightmap rotation

    def load(self, path, dx, dy, dz):
        """ loads the vertices positions from an image """

        # opens the image
        image = Image.open(path)
        # image dimensions
        self.image_width, self.image_height = width, height = image.size
        # self.image_width, self.image_height = width, height = 64, 64

        # heightmap dimensions
        self.x_length = (self.image_width - 1) * dx
        self.y_length = (self.image_height - 1) * dy

        # used for centering the heightmap
        half_x_length = self.x_length / 2.0
        half_y_length = self.y_length / 2.0

        max_z = 0

        # loads the vertices
        for y in range(height - 1):
            # a row of triangles
            row = []
            for x in range(width):
                # gets the red component of the pixel
                # in a grayscale image; the red, green and blue components have the same value
                r = np.mean(image.getpixel((x, y)))
                # centers the heightmap and inverts the y axis
                row.extend((x * dx - half_x_length, half_y_length - y * dy, r * dz))
                # gets the maximum component value
                max_z = max(max_z, r)

                # gets the red component of the pixel
                # in a grayscale image; the red, green and blue components have the same value
                r = np.mean(image.getpixel((x, y + 1)))
                # centers the heightmap and inverts the y axis
                row.extend((x * dx - half_x_length, half_y_length - (y + 1) * dy, r * dz))
                # gets the maximum component value
                max_z = max(max_z, r)
            self.vertices.append(row)

        self.z_length = max_z * dz
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
            pyglet.graphics.draw(self.image_width * 2, gl.GL_TRIANGLE_STRIP, ('v3f', row), ('c4f', color))

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
        self.points = []
        self.tetrahedrons = []

        # translation and rotation values
        self.x = self.y = 0  # heightmap translation
        self.z = -100
        self.rx = self.ry = self.rz = 0  # heightmap rotation
        self.pointsize = 1

    def load(self, points):
        self.points = points
        for i in range(len(self.points)):
            # a row of triangles
            point = np.array(points[i])
            vertices = [point + self.pointsize * np.array([2 * 1.414 / 3, 0, -1 / 3])]\
                        + [point + self.pointsize * np.array([-1.414 / 3, 1.414 / 1.732, -1 / 3])]\
                        + [point + self.pointsize * np.array([-1.414 / 3, -1.414 / 1.732, -1 / 3])]\
                        + [point + self.pointsize * np.array([0, 0, 1])]
            self.tetrahedrons.append(vertices)

    def draw(self):
        gl.glLoadIdentity()
        gl.glTranslatef(self.x, self.y, self.z)
        # rotation
        gl.glRotatef(self.rx - 40, 1, 0, 0)
        gl.glRotatef(self.ry, 0, 1, 0)
        gl.glRotatef(self.rz - 40, 0, 0, 1)
        # color
        gl.glColor3f(*gray)

        # draws the primitives (GL_TRIANGLE_STRIP)
        for i in range(len(self.points)):
            tetrahedrons_verteices = self.tetrahedrons[i]
            faces = []
            faces.append([tetrahedrons_verteices[0], tetrahedrons_verteices[1], tetrahedrons_verteices[3]])
            faces.append([tetrahedrons_verteices[1], tetrahedrons_verteices[2], tetrahedrons_verteices[3]])
            faces.append([tetrahedrons_verteices[2], tetrahedrons_verteices[0], tetrahedrons_verteices[3]])
            faces.append([tetrahedrons_verteices[0], tetrahedrons_verteices[1], tetrahedrons_verteices[2]])
            color = [1, 0, 0, 0.5] * 4 * 3
            faces = np.array(faces).reshape(-1)
            pyglet.graphics.draw(4 * 3, gl.GL_TRIANGLE_STRIP, ('v3f', faces), ('c4f', color))

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
surface.load('surface_64-2.png', 1, 1, .1)
surface1 = Surface()
surface1.load('surface_64-1.png', 1, 1, .1)

# data_points = np.array([[10.0, 10.0, 20], 
#                         [13.0, 13.0, 10]])
# data_points_color = np.array([[255, 0, 0, 255//2], 
#                         [255, 255, 0, 255//2]])
data_points = Point_dot()
data_points.load(np.array([[10.0, 10.0, 20], 
                        [13.0, 13.0, 10],
                        [-32.0, -16.0, 11]]))

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

    # draws the heightmap
    surface.draw('b')
    surface1.draw('g')

    # gl.glBegin(gl.GL_POINTS)
    gl.glBegin(gl.GL_LINES)
    gl.glColor4fv((gl.GLfloat * 4)(1, 0, 0, 1))
    gl.glVertex3f(10.0, 10.0, 20)
    gl.glVertex3f(0.0, 0.0, 20)
    gl.glEnd()

    data_points.draw()

    # gl.glPointSize(10)
    # pyglet.graphics.draw(len(data_points), gl.GL_POINTS, #v3f/stream c4B/static
    #         ('v3f', data_points.reshape(-1)),
    #         ('c4B', data_points_color.reshape(-1)))
    # gl.glPointSize(1)

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    # scroll the MOUSE WHEEL to zoom
    surface.surface_on_mouse_scroll(x, y, scroll_x, scroll_y)
    surface1.surface_on_mouse_scroll(x, y, scroll_x, scroll_y)
    data_points.Point_dot_on_mouse_scroll(x, y, scroll_x, scroll_y)
    # with np.errstate(divide='ignore', over='ignore'):
    #     surface.z += scroll_y * 5 * (1 + 1 / (1 + np.exp((surface.z + 5) * 5)**(-1)))
        # surface1.z += scroll_y * 5 * (1 + 1 / (1 + np.exp((surface1.z + 5) * 5)**(-1)))

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
