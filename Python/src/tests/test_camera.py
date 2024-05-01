import math
import unittest

from src.ray_tracer_challenge.camera import Camera
from src.ray_tracer_challenge.color import Color
from src.ray_tracer_challenge.matrix import Matrix
from src.ray_tracer_challenge.tuple import Point, Vector
from src.tests.test_world import TestWorld


class TeastCamera(unittest.TestCase):
    def test_constructing_a_camera(self):
        hsize = 160
        vsize = 120
        field_of_view = math.pi / 2
        c = Camera(hsize, vsize, field_of_view)
        self.assertEqual(hsize, c.hsize)
        self.assertEqual(vsize, c.vsize)
        self.assertEqual(field_of_view, c.field_of_view)
        self.assertEqual(Matrix.identity(), c.transform)

    def test_the_pixel_size_for_a_horizontal_canvas(self):
        c = Camera(200, 125, math.pi / 2)
        self.assertAlmostEqual(0.01, c.pixel_size)

    def test_the_pixel_size_for_a_vertical_canvas(self):
        c = Camera(125, 200, math.pi / 2)
        self.assertAlmostEqual(0.01, c.pixel_size)

    def test_constructing_a_ray_through_the_center_of_the_canvas(self):
        c = Camera(201, 101, math.pi / 2)
        r = c.ray_for_pixel(100, 50)
        self.assertEqual(Point(0, 0, 0), r.origin)
        self.assertEqual(Vector(0, 0, -1), r.direction)

    def test_constructing_a_ray_through_a_corner_of_the_canvas(self):
        c = Camera(201, 101, math.pi / 2)
        r = c.ray_for_pixel(0, 0)
        self.assertEqual(Point(0, 0, 0), r.origin)
        self.assertEqual(Vector(0.66519, 0.33259, -0.66851), r.direction)

    def test_constructing_a_ray_when_the_camera_is_transformed(self):
        c = Camera(201, 101, math.pi / 2)
        c.transform = Matrix.rotation_y(math.pi / 4) * Matrix.translation(0, -2, 5)
        r = c.ray_for_pixel(100, 50)
        self.assertEqual(Point(0, 2, -5), r.origin)
        self.assertEqual(Vector(math.sqrt(2) / 2, 0, -math.sqrt(2) / 2), r.direction)

    def test_render_world_with_camera(self):
        test_world = TestWorld()
        w = test_world.setup_world()
        c = Camera(11, 11, math.pi / 2)
        origin = Point(0, 0, -5)
        to = Point(0, 0, 0)
        up = Vector(0, 1, 0)
        c.transform = Matrix.view_transform(origin, to, up)
        image = c.render(w)
        self.assertEqual(Color(0.38066, 0.47583, 0.2855), image[5][5])
