import math
import unittest

from src.ray_tracer_challenge.matrix import Matrix
from src.ray_tracer_challenge.tuple import Point, Vector


class TestTranslation(unittest.TestCase):
    def test_translation_multiplying_with_inverse_of_transformation_matrix(self):
        transformation = Matrix.translation(5, -3, 2)
        inverse = transformation.inverse()
        original = Point(-3, 4, 5)
        transform = inverse * original
        self.assertEqual(Point(-8, 7, 3), transform)

    def test_translation_multiplying_with_transformation_matrix(self):
        transformation = Matrix.translation(5, -3, 2)
        original = Point(-3, 4, 5)
        transform = transformation * original
        self.assertEqual(Point(2, 1, 7), transform)

    def test_translation_multiplying_with_transformation_matrix_maintains_vector(self):
        transformation = Matrix.translation(5, -3, 2)
        original = Vector(-3, 4, 5)
        transform = transformation * original
        self.assertEqual(original, transform)


class TestScaling(unittest.TestCase):
    def test_scaling_applied_to_point(self):
        transformation = Matrix.scaling(2, 3, 4)
        original = Point(-4, 6, 8)
        transform = transformation * original
        self.assertEqual(Point(-8, 18, 32), transform)

    def test_scaling_applied_to_vector(self):
        transformation = Matrix.scaling(2, 3, 4)
        original = Vector(-4, 6, 8)
        transform = transformation * original
        self.assertEqual(Vector(-8, 18, 32), transform)

    def test_scaling_multiplying_with_inverse_of_transformation_matrix(self):
        transformation = Matrix.scaling(2, 3, 4)
        inverse = transformation.inverse()
        original = Vector(-4, 6, 8)
        transform = inverse * original
        self.assertEqual(Vector(-2, 2, 2), transform)

    def test_scaling_reflection_is_scaling_by_negative_value(self):
        transformation = Matrix.scaling(-1, 1, 1)
        original = Point(2, 3, 4)
        transform = transformation * original
        self.assertEqual(Point(-2, 3, 4), transform)


class TestRotation(unittest.TestCase):
    def test_rotation_x(self):
        p = Point(0, 1, 0)
        half_quarter = Matrix.rotation_x(math.pi / 4)
        full_quarter = Matrix.rotation_x(math.pi / 2)
        self.assertEqual(Point(0, math.sqrt(2) / 2, math.sqrt(2) / 2), half_quarter * p)
        self.assertEqual(Point(0, 0, 1), full_quarter * p)

    def test_rotation_x_inverse(self):
        p = Point(0, 1, 0)
        half_quarter = Matrix.rotation_x(math.pi / 4)
        inverse = half_quarter.inverse()
        self.assertEqual(Point(0, math.sqrt(2) / 2, -math.sqrt(2) / 2), inverse * p)

    def test_rotation_y(self):
        p = Point(0, 0, 1)
        half_quarter = Matrix.rotation_y(math.pi / 4)
        full_quarter = Matrix.rotation_y(math.pi / 2)
        self.assertEqual(Point(math.sqrt(2) / 2, 0, math.sqrt(2) / 2), half_quarter * p)
        self.assertEqual(Point(1, 0, 0), full_quarter * p)

    def test_rotation_z(self):
        p = Point(0, 1, 0)
        half_quarter = Matrix.rotation_z(math.pi / 4)
        full_quarter = Matrix.rotation_z(math.pi / 2)
        self.assertEqual(Point(-math.sqrt(2) / 2, math.sqrt(2) / 2, 0), half_quarter * p)
        self.assertEqual(Point(-1, 0, 0), full_quarter * p)


class TestShearing(unittest.TestCase):
    def test_shearing_x_y(self):
        transformation = Matrix.shearing(1, 0, 0, 0, 0, 0)
        original = Point(2, 3, 4)
        transform = transformation * original
        self.assertEqual(Point(5, 3, 4), transform)

    def test_shearing_x_z(self):
        transformation = Matrix.shearing(0, 1, 0, 0, 0, 0)
        original = Point(2, 3, 4)
        transform = transformation * original
        self.assertEqual(Point(6, 3, 4), transform)

    def test_shearing_y_x(self):
        transformation = Matrix.shearing(0, 0, 1, 0, 0, 0)
        original = Point(2, 3, 4)
        transform = transformation * original
        self.assertEqual(Point(2, 5, 4), transform)

    def test_shearing_y_z(self):
        transformation = Matrix.shearing(0, 0, 0, 1, 0, 0)
        original = Point(2, 3, 4)
        transform = transformation * original
        self.assertEqual(Point(2, 7, 4), transform)

    def test_shearing_z_x(self):
        transformation = Matrix.shearing(0, 0, 0, 0, 1, 0)
        original = Point(2, 3, 4)
        transform = transformation * original
        self.assertEqual(Point(2, 3, 6), transform)

    def test_shearing_z_y(self):
        transformation = Matrix.shearing(0, 0, 0, 0, 0, 1)
        original = Point(2, 3, 4)
        transform = transformation * original
        self.assertEqual(Point(2, 3, 7), transform)


class TestChainingTransformations(unittest.TestCase):
    def test_chaining_operations(self):
        p0 = Point(1, 0, 1)
        a = Matrix.rotation_x(math.pi / 2)
        b = Matrix.scaling(5, 5, 5)
        c = Matrix.translation(10, 5, 7)
        p1 = a * p0
        p2 = b * p1
        p3 = c * p2
        self.assertEqual(Point(15, 0, 7), p3)

    def test_chaining_in_reverse_order(self):
        p = Point(1, 0, 1)
        a = Matrix.rotation_x(math.pi / 2)
        b = Matrix.scaling(5, 5, 5)
        c = Matrix.translation(10, 5, 7)
        t = c * b * a
        self.assertEqual(Point(15, 0, 7), t * p)


class TestViewTransformation(unittest.TestCase):
    def test_default_view_transformation(self):
        from_point = Point(0, 0, 0)
        to_point = Point(0, 0, -1)
        up_vector = Vector(0, 1, 0)
        transform = Matrix.view_transform(from_point, to_point, up_vector)
        self.assertEqual(Matrix.identity(), transform)

    def test_looking_positive_z_direction(self):
        from_point = Point(0, 0, 0)
        to_point = Point(0, 0, 1)
        up_vector = Vector(0, 1, 0)
        transform = Matrix.view_transform(from_point, to_point, up_vector)
        self.assertEqual(Matrix.scaling(-1, 1, -1), transform)

    def test_view_transformation_moves_world(self):
        from_point = Point(0, 0, 8)
        to_point = Point(0, 0, 0)
        up_vector = Vector(0, 1, 0)
        transform = Matrix.view_transform(from_point, to_point, up_vector)
        self.assertEqual(Matrix.translation(0, 0, -8), transform)

    def test_arbitrary_view_transformation(self):
        from_point = Point(1, 3, 2)
        to_point = Point(4, -2, 8)
        up_vector = Vector(1, 1, 0)
        transform = Matrix.view_transform(from_point, to_point, up_vector)
        self.assertEqual(Matrix([
            [-0.50709, 0.50709, 0.67612, -2.36643],
            [0.76772, 0.60609, 0.12122, -2.82843],
            [-0.35857, 0.59761, -0.71714, 0.00000],
            [0.00000, 0.00000, 0.00000, 1.00000]
        ]), transform)
