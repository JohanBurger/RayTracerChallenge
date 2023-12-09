import unittest

from src.ray_tracer_challenge.matrix import Matrix
from src.ray_tracer_challenge.tuple import Point, Vector


class TestTransformation(unittest.TestCase):
    def test_transformation_multiplying_with_transformation_matrix(self):
        transformation = Matrix.translation(5, -3, 2)
        original = Point(-3, 4, 5)
        transform = transformation * original
        self.assertEqual(Point(2, 1, 7), transform)

    def test_transformation_multiplying_with_inverse_of_transformation_matrix(self):
        transformation = Matrix.translation(5, -3, 2)
        inverse = transformation.inverse()
        original = Point(-3, 4, 5)
        transform = inverse * original
        self.assertEqual(Point(-8, 7, 3), transform)

    def test_transformation_multiplying_with_transformation_matrix_maintains_vector(self):
        transformation = Matrix.translation(5, -3, 2)
        original = Vector(-3, 4, 5)
        transform = transformation * original
        self.assertEqual(original, transform)
