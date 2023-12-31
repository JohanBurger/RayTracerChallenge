import unittest

from src.ray_tracer_challenge.intersection import Intersection, Intersections
from src.ray_tracer_challenge.ray import Ray
from src.ray_tracer_challenge.sphere import Sphere
from src.ray_tracer_challenge.tuple import Point, Vector


class TestIntersection(unittest.TestCase):
    def test_intersection_encapsulates_time_and_object(self):
        s = Sphere()
        i = Intersection(3.5, s)
        self.assertEqual(i.t, 3.5)
        self.assertIs(i.object, s)

    def test_aggregating_intersections(self):
        s = Sphere()
        i1 = Intersection(1, s)
        i2 = Intersection(2, s)
        xs = Intersections(i1, i2)
        self.assertEqual(2, xs.count)
        self.assertEqual(1, xs[0].t)
        self.assertEqual(2, xs[1].t)

    def test_hit_when_all_intersections_have_positive_t(self):
        s = Sphere()
        i1 = Intersection(1, s)
        i2 = Intersection(2, s)
        xs = Intersections(i1, i2)
        i = xs.hit()
        self.assertIs(i1, i)

    def test_hit_when_some_intersections_have_negative_t(self):
        s = Sphere()
        i1 = Intersection(-1, s)
        i2 = Intersection(1, s)
        xs = Intersections(i1, i2)
        i = xs.hit()
        self.assertIs(i2, i)

    def test_hit_when_all_intersections_have_negative_t(self):
        s = Sphere()
        i1 = Intersection(-2, s)
        i2 = Intersection(-1, s)
        xs = Intersections(i1, i2)
        i = xs.hit()
        self.assertIsNone(i)

    def test_hit_is_always_lowest_nonnegative_intersection(self):
        s = Sphere()
        i1 = Intersection(5, s)
        i2 = Intersection(7, s)
        i3 = Intersection(-3, s)
        i4 = Intersection(2, s)
        xs = Intersections(i1, i2, i3, i4)
        i = xs.hit()
        self.assertIs(i4, i)

    def test_precomputing_state_of_intersection(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        shape = Sphere()
        i = Intersection(4, shape)
        comps = i.prepare_computations(r)
        self.assertEqual(i.t, comps.t)
        self.assertIs(i.object, comps.object)
        self.assertEqual(Point(0, 0, -1), comps.point)
        self.assertEqual(Vector(0, 0, -1), comps.eye_vector)
        self.assertEqual(Vector(0, 0, -1), comps.normal_vector)

    def test_precomputing_state_of_outside_hit(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        shape = Sphere()
        i = Intersection(4, shape)
        comps = i.prepare_computations(r)
        self.assertFalse(comps.inside)

    def test_precomputing_state_of_inside_hit(self):
        r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        shape = Sphere()
        i = Intersection(1, shape)
        comps = i.prepare_computations(r)
        self.assertEqual(Point(0, 0, 1), comps.point)
        self.assertEqual(Vector(0, 0, -1), comps.eye_vector)
        self.assertTrue(comps.inside)
        self.assertEqual(Vector(0, 0, -1), comps.normal_vector)
