import math

from src.ray_tracer_challenge.canvas import Canvas
from src.ray_tracer_challenge.matrix import Matrix
from src.ray_tracer_challenge.ray import Ray
from src.ray_tracer_challenge.tuple import Point


class Camera:
    """
    Represents a camera in a 3D scene.
    """

    def __init__(self, hsize, vsize, field_of_view):
        self._hsize = hsize
        self._vsize = vsize
        self._field_of_view = field_of_view
        self._transform = Matrix.identity()

        half_view = math.tan(self._field_of_view / 2)
        aspect = hsize / vsize
        if aspect >= 1:
            self._half_width = half_view
            self._half_height = half_view / aspect
        else:
            self._half_width = half_view * aspect
            self._half_height = half_view

        self._pixel_size = (self._half_width * 2) / self._hsize

    @property
    def hsize(self):
        return self._hsize

    @property
    def vsize(self):
        return self._vsize

    @property
    def field_of_view(self):
        return self._field_of_view

    @property
    def transform(self):
        return self._transform

    @transform.setter
    def transform(self, value):
        self._transform = value

    @property
    def pixel_size(self):
        return self._pixel_size

    def ray_for_pixel(self, x, y):
        # Offset from the edge of the canvas to the pixel's center
        x_offset = (x + 0.5) * self._pixel_size
        y_offset = (y + 0.5) * self._pixel_size

        # The untransformed coordinates of the pixel in world space
        # (remember that the camera looks toward -z, so +x is to the *left*)
        world_x = self._half_width - x_offset
        world_y = self._half_height - y_offset

        # Using the camera matrix, transform the canvas point and the origin,
        # and then compute the ray's direction vector.
        # The canvas is at z = -1, so the camera matrix transforms points
        # from z = 0 to z = -1.
        pixel = self._transform.inverse() * Point(world_x, world_y, -1)
        origin = self._transform.inverse() * Point(0, 0, 0)
        direction = (pixel - origin).normalize()

        return Ray(origin, direction)

    def render(self, world):
        canvas = Canvas(self._hsize, self._vsize)
        for y in range(self._vsize):
            for x in range(self._hsize):
                ray = self.ray_for_pixel(x, y)
                color = world.color_at(ray)
                canvas.set_pixel(x, y, color)
        return canvas
