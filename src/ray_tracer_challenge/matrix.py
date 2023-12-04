import math
from src.ray_tracer_challenge.constants import EPSILON as EPSILON


class Matrix:
    def __init__(self, *args):
        if len(args) == 1 and type(args[0]) is list:
            # TODO: Validate that all rows are the same length?
            self._matrix = args[0]
        elif len(args) == 2 and type(args[0]) is int and type(args[1]) is int:
            self._matrix = [[0 for i in range(args[1])] for j in range(args[0])]

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
                if not math.isclose(self[row, column], other[row, column], rel_tol=EPSILON):
                    return False
        return True
