import math
from src.ray_tracer_challenge.constants import EPSILON as EPSILON
from src.ray_tracer_challenge.tuple import Tuple


class Matrix:
    def __init__(self, *args):
        if len(args) == 1 and type(args[0]) is list:
            # Validate that all rows have the same number of columns
            if max(len(row) for row in args[0]) != min(len(row) for row in args[0]):
                raise ValueError("All rows must have the same number of columns")
            self._matrix = args[0]
        elif len(args) == 2 and type(args[0]) is int and type(args[1]) is int:
            self._matrix = [[0 for _ in range(args[1])] for _ in range(args[0])]

    @property
    def rows(self):
        return len(self._matrix)

    @property
    def columns(self):
        return len(self._matrix[0])

    def __getitem__(self, key):
        row = self._matrix[key[0]]
        return row[key[1]]

    def __setitem__(self, key, value):
        row = self._matrix[key[0]]
        row[key[1]] = value

    def __eq__(self, other):
        if self.rows != other.rows or self.columns != other.columns:
            return False
        for row in range(self.rows):
            for column in range(self.columns):
                if not math.isclose(self[row, column], other[row, column], abs_tol=EPSILON):
                    return False
        return True

    def __mul__(self, other):
        if type(other) is Matrix:
            return self._multiply_matrix(other)
        elif isinstance(other, Tuple):
            return self._multiply_tuple(other)
        else:
            raise TypeError(f"Can't multiply Matrix by {format(type(other))}")

    def _multiply_matrix(self, other):
        if self.columns != other.rows:
            raise ValueError("Matrices must have the same number of rows and columns")
        result = Matrix(self.rows, other.columns)
        for row in range(self.rows):
            for column in range(other.columns):
                for i in range(self.columns):
                    result[row, column] += self[row, i] * other[i, column]
        return result

    def _multiply_tuple(self, tuple_multiplier):
        if self.columns != 4:
            raise ValueError("Matrix must have 4 columns")
        result = Tuple(0, 0, 0, 0)
        for row in range(self.rows):
            for column in range(self.columns):
                result[row] += self[row, column] * tuple_multiplier[column]
        return result

    def transpose(self):
        result = Matrix(self.columns, self.rows)
        for row in range(self.rows):
            for column in range(self.columns):
                result[column, row] = self[row, column]
        return result

    @classmethod
    def identity(cls, size=4):
        result = Matrix(size, size)
        for i in range(size):
            result[i, i] = 1
        return result

    @classmethod
    def translation(cls, x, y, z):
        result = cls.identity()
        result[0, 3] = x
        result[1, 3] = y
        result[2, 3] = z
        return result

    @classmethod
    def scaling(cls, x, y, z):
        result = cls.identity()
        result[0, 0] = x
        result[1, 1] = y
        result[2, 2] = z
        return result

    @classmethod
    def rotation_x(cls, radians):
        result = cls.identity()
        result[1, 1] = math.cos(radians)
        result[1, 2] = -math.sin(radians)
        result[2, 1] = math.sin(radians)
        result[2, 2] = math.cos(radians)
        return result

    @classmethod
    def rotation_y(cls, radians):
        result = cls.identity()
        result[0, 0] = math.cos(radians)
        result[0, 2] = math.sin(radians)
        result[2, 0] = -math.sin(radians)
        result[2, 2] = math.cos(radians)
        return result

    @classmethod
    def rotation_z(cls, radians):
        result = cls.identity()
        result[0, 0] = math.cos(radians)
        result[0, 1] = -math.sin(radians)
        result[1, 0] = math.sin(radians)
        result[1, 1] = math.cos(radians)
        return result

    @classmethod
    def shearing(cls, xy, xz, yx, yz, zx, zy):
        result = cls.identity()
        result[0, 1] = xy
        result[0, 2] = xz
        result[1, 0] = yx
        result[1, 2] = yz
        result[2, 0] = zx
        result[2, 1] = zy
        return result

    def submatrix(self, skip_row, skip_column):
        result = Matrix(self.rows - 1, self.columns - 1)
        target_row = 0
        for row in range(self.rows):
            if row == skip_row:
                continue
            target_column = 0
            for column in range(self.columns):
                if column == skip_column:
                    continue
                result[target_row, target_column] = self[row, column]
                target_column += 1
            target_row += 1
        return result

    def determinant(self):
        if self.rows > 2:
            determinant = 0
            for column in range(self.columns):
                determinant += self[0, column] * self.cofactor(0, column)

            return determinant

        return (self[0, 0] * self[1, 1]) - (self[0, 1] * self[1, 0])

    def minor(self, row, column):
        submatrix = self.submatrix(row, column)
        return submatrix.determinant()

    def cofactor(self, row, column):
        minor = self.minor(row, column)
        if (row + column) % 2 == 0:
            return minor
        else:
            return -minor

    def is_invertible(self):
        return self.determinant() != 0

    def inverse(self):
        inverse = Matrix(self.rows, self.columns)
        determinant = self.determinant()
        # if determinant != 0:
        #     raise ValueError("Matrix is not invertible")
        for row in range(self.rows):
            for column in range(self.columns):
                cofactor = self.cofactor(row, column)
                inverse[column, row] = cofactor / determinant

        return inverse

    @classmethod
    def view_transform(cls, from_point, to_point, up_vector):
        forward = (to_point - from_point).normalize()
        left = forward.cross(up_vector.normalize())
        true_up = left.cross(forward)
        orientation = Matrix.identity()
        orientation[0, 0] = left.x
        orientation[0, 1] = left.y
        orientation[0, 2] = left.z
        orientation[1, 0] = true_up.x
        orientation[1, 1] = true_up.y
        orientation[1, 2] = true_up.z
        orientation[2, 0] = -forward.x
        orientation[2, 1] = -forward.y
        orientation[2, 2] = -forward.z
        return orientation * Matrix.translation(-from_point.x, -from_point.y, -from_point.z)
