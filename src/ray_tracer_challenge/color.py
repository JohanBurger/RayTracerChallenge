from __future__ import annotations

import math
from numbers import Number

from src.ray_tracer_challenge.constants import EPSILON as EPSILON


class Color:
    """
    Color class with red, green, and blue attributes.
    """

    def __init__(self, red, green, blue):
        self._red = red
        self._green = green
        self._blue = blue

    @property
    def red(self):
        return self._red

    @property
    def green(self):
        return self._green

    @property
    def blue(self):
        return self._blue

    def __eq__(self, other):
        return (math.isclose(self.red, other.red, rel_tol=EPSILON) and
                math.isclose(self.green, other.green, rel_tol=EPSILON) and
                math.isclose(self.blue, other.blue, rel_tol=EPSILON))

    def __add__(self, other):
        return Color(self.red + other.red,
                     self.green + other.green,
                     self.blue + other.blue)

    def __sub__(self, other):
        return Color(self.red - other.red,
                     self.green - other.green,
                     self.blue - other.blue)

    def __mul__(self, other: Number | Color) -> Color:
        if isinstance(other, Number):
            return Color(self.red * other,
                         self.green * other,
                         self.blue * other)
        elif type(other) is Color:
            return Color(self.red * other.red,
                         self.green * other.green,
                         self.blue * other.blue)
        else:
            raise TypeError(f"Can't multiply Color by {format(type(other))}")

    def __repr__(self):
        return f"Color(red:{self.red}, green:{self.green}, blue:{self.blue})"


class Colors:
    BLACK = Color(0, 0, 0)
    WHITE = Color(1, 1, 1)
    RED = Color(1, 0, 0)
    GREEN = Color(0, 1, 0)
    BLUE = Color(0, 0, 1)
