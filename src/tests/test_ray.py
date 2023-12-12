import unittest

from src.ray_tracer_challenge.matrix import Matrix
from src.ray_tracer_challenge.ray import Ray
from src.ray_tracer_challenge.sphere import Sphere
from src.ray_tracer_challenge.tuple import Point, Vector


class TestRay(unittest.TestCase):
    def test_ray_has_origin_and_direction(self):
        origin = Point(1, 2, 3)
        direction = Vector(4, 5, 6)
        r = Ray(origin, direction)
        self.assertEqual(r.origin, origin)
        self.assertEqual(r.direction, direction)

    def test_compute_point_from_distance(self):
        r = Ray(Point(2, 3, 4), Vector(1, 0, 0))
        self.assertEqual(r.position(0), Point(2, 3, 4))
        self.assertEqual(r.position(1), Point(3, 3, 4))
        self.assertEqual(r.position(-1), Point(1, 3, 4))
        self.assertEqual(r.position(2.5), Point(4.5, 3, 4))

    def test_ray_intersects_a_sphere_at_two_points(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(2, xs.count)
        self.assertEqual(4.0, xs[0].t)
        self.assertTrue(s is xs[0].object)
        self.assertEqual(6.0, xs[1].t)
        self.assertTrue(s is xs[1].object)

    def test_ray_intersects_sphere_at_tangent(self):
        r = Ray(Point(0, 1, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(2, xs.count)
        self.assertEqual(5.0, xs[0].t)
        self.assertTrue(s is xs[0].object)
        self.assertEqual(5.0, xs[1].t)
        self.assertTrue(s is xs[1].object)

    def test_ray_misses_sphere(self):
        r = Ray(Point(0, 2, -5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(0, xs.count)

    def test_ray_originates_inside_sphere(self):
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(2, xs.count)
        self.assertEqual(-1.0, xs[0].t)
        self.assertTrue(s is xs[0].object)
        self.assertEqual(1.0, xs[1].t)
        self.assertTrue(s is xs[1].object)

    def test_sphere_is_behind_ray(self):
        r = Ray(Point(0, 0, 5), Vector(0, 0, 1))
        s = Sphere()
        xs = s.intersect(r)
        self.assertEqual(2, xs.count)
        self.assertEqual(-6.0, xs[0].t)
        self.assertTrue(s is xs[0].object)
        self.assertEqual(-4.0, xs[1].t)
        self.assertTrue(s is xs[1].object)

    def test_ray_translation(self):
        r = Ray(Point(1, 2, 3), Vector(0, 1, 0))
        m = Matrix.translation(3, 4, 5)
        r2 = r.transform(m)
        self.assertEqual(r2.origin, Point(4, 6, 8))
        self.assertEqual(r2.direction, Vector(0, 1, 0))

    def test_ray_scaling(self):
        r = Ray(Point(1, 2, 3), Vector(0, 1, 0))
        m = Matrix.scaling(2, 3, 4)
        r2 = r.transform(m)
        self.assertEqual(r2.origin, Point(2, 6, 12))
        self.assertEqual(r2.direction, Vector(0, 3, 0))
