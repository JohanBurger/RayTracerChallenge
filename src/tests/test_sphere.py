import unittest

from src.ray_tracer_challenge.matrix import Matrix
from src.ray_tracer_challenge.ray import Ray
from src.ray_tracer_challenge.sphere import Sphere
from src.ray_tracer_challenge.tuple import Point, Vector


class TestSphere(unittest.TestCase):
    def test_default_transformation(self):
        s = Sphere()
        self.assertTrue(s.transform == Matrix.identity())

    def test_change_transformation(self):
        s = Sphere()
        t = Matrix.translation(2, 3, 4)
        s.transform = t
        self.assertTrue(s.transform is t)

    def test_intersect_scaled_sphere_with_ray(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        s.transform = Matrix.scaling(2, 2, 2)
        xs = s.intersect(r)
        self.assertEqual(2, xs.count)
        self.assertEqual(3, xs[0].t)
        self.assertEqual(7, xs[1].t)

    def test_intersect_translated_sphere_with_ray(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        s.transform = Matrix.translation(5, 0, 0)
        xs = s.intersect(r)
        self.assertEqual(0, xs.count)
