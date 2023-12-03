from __future__ import annotations

from numbers import Number

from constants import EPSILON as EPSILON


class Color:
    """
    Color class with red, green, and blue attributes.
    """

    @staticmethod
    def red():
        return Color(1, 0, 0)

    @staticmethod
    def green():
        return Color(0, 1, 0)

    @staticmethod
    def blue():
        return Color(0, 0, 1)

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
        return (abs(self.red - other.red) < EPSILON and
                abs(self.green - other.green) < EPSILON and
                abs(self.blue - other.blue) < EPSILON)

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
