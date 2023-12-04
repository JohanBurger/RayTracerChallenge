"""
Unit tests for the Point class.
"""
import math
import unittest
from src.ray_tracer_challenge.tuple import Tuple, Point, Vector


class TestTuple(unittest.TestCase):
    def test_tuple_has_correct_coordinate(self):
        (x, y, z, w) = (4, -4, 3, 1)
        t = Tuple(x, y, z, w)
        self.assertEqual(t.x, x)
        self.assertEqual(t.y, y)
        self.assertEqual(t.z, z)
        self.assertEqual(t.w, w)

    def test_tuple_point_is_returned_for_w_1(self):
        (x, y, z, w) = (4, -4, 3, 1)
        t = Tuple(x, y, z, w)
        self.assertIsInstance(t, Point)
        self.assertFalse(isinstance(t, Vector))

    def test_tuple_vector_is_returned_for_w_0(self):
        (x, y, z, w) = (4, -4, 3, 0)
        t = Tuple(x, y, z, w)
        self.assertIsInstance(t, Vector)
        self.assertFalse(isinstance(t, Point))

    def test_tuple_equality(self):
        t1 = Tuple(0.1, 0.2, (0.2 + 0.1), 1)
        t2 = Tuple(0.1, 0.2, 0.3, 1)
        self.assertEqual(t1, t2)

    def test_tuple_addition_of_point_and_vector(self):
        p = Point(3, -2, 5)
        v = Vector(-2, 3, 1)
        self.assertEqual(p + v, Point(1, 1, 6))

    def test_tuple_addition_of_two_vectors(self):
        v1 = Vector(3, -2, 5)
        v2 = Vector(-2, 3, 1)
        self.assertEqual(v1 + v2, Vector(1, 1, 6))

    def test_tuple_addition_of_two_points(self):
        p1 = Point(3, -2, 5)
        p2 = Point(-2, 3, 1)
        with self.assertRaises(TypeError):
            p1 + p2

    def test_tuple_subtraction_of_points(self):
        p1 = Point(3, 2, 1)
        p2 = Point(5, 6, 7)
        self.assertEqual(p1 - p2, Vector(-2, -4, -6))

    def test_tuple_subtraction_of_vector_from_point(self):
        p = Point(3, 2, 1)
        v = Vector(5, 6, 7)
        self.assertEqual(p - v, Point(-2, -4, -6))

    def test_tuple_subtraction_of_vectors(self):
        v1 = Vector(3, 2, 1)
        v2 = Vector(5, 6, 7)
        self.assertEqual(v1 - v2, Vector(-2, -4, -6))

    def test_tuple_negation_vector(self):
        v = Vector(1, -2, 3)
        self.assertEqual(-v, Vector(-1, 2, -3))

    def test_tuple_negation_point(self):
        p = Point(1, -2, 3)
        self.assertEqual(-p, Point(-1, 2, -3))

    def test_tuple_scalar_multiplication_of_vector(self):
        v = Vector(1, -2, 3)
        self.assertEqual(v * 3.5, Vector(3.5, -7, 10.5))

    def test_tuple_scalar_multiplication_of_point(self):
        p = Point(1, -2, 3)
        self.assertEqual(p * 0.5, Point(0.5, -1, 1.5))

    def test_tuple_scalar_division_of_vector(self):
        v = Vector(1, -2, 3)
        self.assertEqual(v / 2, Vector(0.5, -1, 1.5))

    def test_tuple_scalar_division_of_point(self):
        p = Point(1, -2, 3)
        self.assertEqual(p / 2, Point(0.5, -1, 1.5))


class TestPoint(unittest.TestCase):
    def test_point_has_correct_coordinate(self):
        (x, y, z) = (4, -4, 3)

        p = Point(x, y, z)
        self.assertIsInstance(p, Point)
        self.assertFalse(isinstance(p, Vector))
        self.assertEqual(p.x, x)
        self.assertEqual(p.y, y)
        self.assertEqual(p.z, z)
        self.assertEqual(p.w, 1)


class TestVector(unittest.TestCase):
    def test_vector_has_correct_coordinate(self):
        (x, y, z) = (4, -4, 3)
        v = Vector(x, y, z)
        self.assertIsInstance(v, Vector)
        self.assertFalse(isinstance(v, Point))
        self.assertEqual(v.x, x)
        self.assertEqual(v.y, y)
        self.assertEqual(v.z, z)
        self.assertEqual(v.w, 0)

    def test_vector_magnitude(self):
        v1 = Vector(1, 0, 0)
        v2 = Vector(0, 1, 0)
        v3 = Vector(0, 0, 1)
        v4 = Vector(1, 2, 3)
        v5 = Vector(-1, -2, -3)

        self.assertEqual(v1.magnitude(), 1)
        self.assertEqual(v2.magnitude(), 1)
        self.assertEqual(v3.magnitude(), 1)
        self.assertEqual(v4.magnitude(), math.sqrt(14))
        self.assertEqual(v5.magnitude(), math.sqrt(14))

    def test_vector_normalization(self):
        v1 = Vector(4, 0, 0)
        v2 = Vector(1, 2, 3)
        self.assertEqual(v1.normalize(), Vector(1, 0, 0))
        self.assertEqual(v2.normalize(), Vector((1 / math.sqrt(14)), (2 / math.sqrt(14)), (3 / math.sqrt(14))))
        self.assertEqual(v2.normalize().magnitude(), 1)

    def test_vector_dot_product(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(2, 3, 4)
        self.assertEqual(v1.dot(v2), 20)

    def test_vector_cross_product(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(2, 3, 4)
        self.assertEqual(v1.cross(v2), Vector(-1, 2, -1))
        self.assertEqual(v2.cross(v1), Vector(1, -2, 1))

        x = Vector(1, 0, 0)
        y = Vector(0, 1, 0)
        z = Vector(0, 0, 1)

        self.assertEqual(x.cross(y), z)
        self.assertEqual(y.cross(x), -z)

        self.assertEqual(y.cross(z), x)
        self.assertEqual(z.cross(y), -x)

        self.assertEqual(z.cross(x), y)
        self.assertEqual(x.cross(z), -y)


if __name__ == '__main__':
    unittest.main()
