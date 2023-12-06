import unittest

from src.ray_tracer_challenge.matrix import Matrix


class TestMatrix(unittest.TestCase):
    def test_matrix_can_construct_4_by_4_matrix(self):
        m = Matrix([[1, 2, 3, 4],
                    [5.5, 6.5, 7.5, 8.5],
                    [9, 10, 11, 12],
                    [13.5, 14.5, 15.5, 16.5]])
        self.assertEqual(4, m.rows)
        self.assertEqual(4, m.columns)
        self.assertEqual(1, m[0, 0])
        self.assertEqual(4, m[0, 3])
        self.assertEqual(5.5, m[1, 0])
        self.assertEqual(7.5, m[1, 2])
        self.assertEqual(11, m[2, 2])
        self.assertEqual(13.5, m[3, 0])
        self.assertEqual(15.5, m[3, 2])

    def test_matrix_can_construct_3_by_3_matrix(self):
        m = Matrix([[-3, 5, 0],
                    [1, -2, -7],
                    [0, 1, 1]])
        self.assertEqual(3, m.rows)
        self.assertEqual(3, m.columns)
        self.assertEqual(-3, m[0, 0])
        self.assertEqual(-2, m[1, 1])
        self.assertEqual(1, m[2, 2])

    def test_matrix_can_construct_2_by_2_matrix(self):
        m = Matrix([[1, 2],
                    [3, 4]])
        self.assertEqual(2, m.rows)
        self.assertEqual(2, m.columns)
        self.assertEqual(1, m[0, 0])
        self.assertEqual(2, m[0, 1])
        self.assertEqual(3, m[1, 0])
        self.assertEqual(4, m[1, 1])

    def test_matrix_4_by_4_equality(self):
        m1 = Matrix([[1, 2, 0.3, 4],
                     [5, 5, 6, 8],
                     [9, 8, 7, 6],
                     [5, 4, 3, 2]])

        m2 = Matrix([[1, 2, (0.1 + 0.2), 4],
                     [5, 5, 6, 8],
                     [9, 8, 7, 6],
                     [5, 4, 3, 2]])

        self.assertEqual(m1, m2)
        m2[0, 3] = 5
        self.assertNotEqual(m1, m2)

    def test_matrix_3_by_3_equality(self):
        m1 = Matrix([[1, 2, 0.3],
                     [4, 5, 6],
                     [7, 8, 9]])

        m2 = Matrix([[1, 2, (0.1 + 0.2)],
                     [4, 5, 6],
                     [7, 8, 9]])

        self.assertEqual(m1, m2)
        m2[0, 2] = 0.4
        self.assertNotEqual(m1, m2)

    def test_matrix_2_by_2_equality(self):
        m1 = Matrix([[1, 2],
                     [0.3, 4]])

        m2 = Matrix([[1, 2],
                     [(0.1 + 0.2), 4]])

        self.assertEqual(m1, m2)
        m2[0, 1] = 3
        self.assertNotEqual(m1, m2)
