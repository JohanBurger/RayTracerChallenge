import unittest

from src.ray_tracer_challenge.matrix import Matrix
from src.ray_tracer_challenge.tuple import Tuple


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

    def test_matrix_multiplied_by_matrix(self):
        m1 = Matrix([[1, 2, 3, 4],
                     [5, 6, 7, 8],
                     [9, 8, 7, 6],
                     [5, 4, 3, 2]])

        m2 = Matrix([[-2, 1, 2, 3],
                     [3, 2, 1, -1],
                     [4, 3, 6, 5],
                     [1, 2, 7, 8]])

        expected_product = Matrix([[20, 22, 50, 48],
                                   [44, 54, 114, 108],
                                   [40, 58, 110, 102],
                                   [16, 26, 46, 42]])

        self.assertEqual(expected_product, m1 * m2)

    def test_matrix_multiplied_by_identity_matrix(self):
        m = Matrix([[0, 1, 2, 4],
                    [1, 2, 4, 8],
                    [2, 4, 8, 16],
                    [4, 8, 16, 32]])
        identity = Matrix.identity()
        self.assertEqual(m, m * identity)

    def test_matrix_multiplied_by_tuple(self):
        matrix = Matrix([[1, 2, 3, 4],
                         [2, 4, 4, 2],
                         [8, 6, 4, 1],
                         [0, 0, 0, 1]])
        tuple = Tuple(1, 2, 3, 1)
        expected_product = Tuple(18, 24, 33, 1)
        self.assertEqual(expected_product, matrix * tuple)

    def test_matrix_identity_multiplied_by_tuple(self):
        tuple = Tuple(1, 2, 3, 1)
        identity = Matrix.identity()
        self.assertEqual(tuple, identity * tuple)

    def test_matrix_transposition(self):
        matrix = Matrix([[0, 9, 3, 0],
                         [9, 8, 0, 8],
                         [1, 8, 5, 3],
                         [0, 0, 5, 8]])
        expected_transposition = Matrix([[0, 9, 1, 0],
                                         [9, 8, 8, 0],
                                         [3, 0, 5, 5],
                                         [0, 8, 3, 8]])
        self.assertEqual(expected_transposition, matrix.transpose())

    def test_matrix_identity_transposition(self):
        identity = Matrix.identity()
        self.assertEqual(identity, identity.transpose())

    def test_matrix_determinant_2_by_2(self):
        matrix = Matrix([[1, 5],
                         [-3, 2]])
        self.assertEqual(17, matrix.determinant())

    def test_matrix_determinant_3_by_3(self):
        matrix = Matrix([[1, 2, 6],
                         [-5, 8, -4],
                         [2, 6, 4]])
        self.assertEqual(56, matrix.cofactor(0, 0))
        self.assertEqual(12, matrix.cofactor(0, 1))
        self.assertEqual(-46, matrix.cofactor(0, 2))
        self.assertEqual(-196, matrix.determinant())

    def test_matrix_determinant_4_by_4(self):
        matrix = Matrix([[-2, -8, 3, 5],
                         [-3, 1, 7, 3],
                         [1, 2, -9, 6],
                         [-6, 7, 7, -9]])
        self.assertEqual(690, matrix.cofactor(0, 0))
        self.assertEqual(447, matrix.cofactor(0, 1))
        self.assertEqual(210, matrix.cofactor(0, 2))
        self.assertEqual(51, matrix.cofactor(0, 3))
        self.assertEqual(-4071, matrix.determinant())

    def test_matrix_submatrix_3_by_3(self):
        matrix = Matrix([[1, 5, 0],
                         [-3, 2, 7],
                         [0, 6, -3]])
        expected_submatrix = Matrix([[-3, 2],
                                     [0, 6]])
        self.assertEqual(expected_submatrix, matrix.submatrix(0, 2))

    def test_matrix_submatrix_4_by_4(self):
        matrix = Matrix([[-6, 1, 1, 6],
                         [-8, 5, 8, 6],
                         [-1, 0, 8, 2],
                         [-7, 1, -1, 1]])
        expected_submatrix = Matrix([[-6, 1, 6],
                                     [-8, 8, 6],
                                     [-7, -1, 1]])
        self.assertEqual(expected_submatrix, matrix.submatrix(2, 1))

    def test_matrix_minor_3_by_3(self):
        matrix = Matrix([[3, 5, 0],
                         [2, -1, -7],
                         [6, -1, 5]])
        (row, column) = (1, 0)
        self.assertEqual(matrix.submatrix(row, column).determinant(), matrix.minor(row, column))
        self.assertEqual(25, matrix.submatrix(row, column).determinant())

    def test_matrix_cofactor_3_by_3(self):
        matrix = Matrix([[3, 5, 0],
                         [2, -1, -7],
                         [6, -1, 5]])
        self.assertEqual(-12, matrix.minor(0, 0))
        self.assertEqual(-12, matrix.cofactor(0, 0))
        self.assertEqual(25, matrix.minor(1, 0))
        self.assertEqual(-25, matrix.cofactor(1, 0))

    def test_matrix_invertible(self):
        invertible_matrix = Matrix([[6, 4, 4, 4],
                                    [5, 5, 7, 6],
                                    [4, -9, 3, -7],
                                    [9, 1, 7, -6]])

        not_invertible_matrix = Matrix([[-4, 2, -2, -3],
                                        [9, 6, 2, 6],
                                        [0, -5, 1, -5],
                                        [0, 0, 0, 0]])

        self.assertEqual(-2120, invertible_matrix.determinant())
        self.assertTrue(invertible_matrix.is_invertible())

        self.assertEqual(0, not_invertible_matrix.determinant())
        self.assertFalse(not_invertible_matrix.is_invertible())

    def test_matrix_inverse(self):
        matrix = Matrix([[-5, 2, 6, -8],
                         [1, -5, 1, 8],
                         [7, 7, -6, -7],
                         [1, -3, 7, 4]])

        determinant = matrix.determinant()
        self.assertEqual(532, determinant)
        self.assertEqual(-160, matrix.cofactor(2, 3))
        inverse = matrix.inverse()
        self.assertEqual(matrix.cofactor(2, 3) / determinant, inverse[3, 2])
        self.assertEqual(105, matrix.cofactor(3, 2))
        self.assertEqual(matrix.cofactor(3, 2) / determinant, inverse[2, 3])
        expected_inverse = Matrix(
            [[0.21804511278195488, 0.45112781954887216, 0.24060150375939848, -0.045112781954887216],
             [-0.8082706766917294, -1.4567669172932332, -0.44360902255639095, 0.5206766917293233],
             [-0.07894736842105263, -0.2236842105263158, -0.05263157894736842, 0.19736842105263158],
             [-0.5225563909774437, -0.8139097744360902, -0.3007518796992481, 0.30639097744360905]])
        self.assertEqual(expected_inverse, inverse)

    def test_matrix_divided_by_inverse_is_identity(self):
        matrix = Matrix([[-5, 2, 6, -8],
                         [1, -5, 1, 8],
                         [7, 7, -6, -7],
                         [1, -3, 7, 4]])
        inverse = matrix.inverse()
        self.assertEqual(matrix.identity(), matrix * inverse)

    def test_matrix_multiplying_with_product_of_inverse(self):
        a = Matrix([[3, -9, 7, 3],
                    [3, -8, 2, -9],
                    [-4, 4, 4, 1],
                    [-6, 5, -1, 1]])
        b = Matrix([[8, 2, 2, 2],
                    [3, -1, 7, 0],
                    [7, 0, 5, 4],
                    [6, -2, 0, 5]])
        c = a * b
        self.assertEqual(a, c * b.inverse())
