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
        while self.rows > 2:
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
        for row in range(self.rows):
            for column in range(self.columns):
                cofactor = self.cofactor(row, column)
                inverse[column, row] = cofactor / determinant

        return inverse
