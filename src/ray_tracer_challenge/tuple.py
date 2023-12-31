"""
Tuple class and derived classes Point and Vector.
"""
from src.ray_tracer_challenge.color import Color
from src.ray_tracer_challenge.constants import EPSILON as EPSILON
import math


class Tuple:
    """
    Tuple class with x, y, z, and w coordinates.
    """

    def __init__(self, x, y, z, w):
        (self._x, self._y, self._z, self._w) = (x, y, z, w)
        if w == 0:
            self.__class__ = Vector
        elif w == 1:
            self.__class__ = Point
        else:
            raise TypeError("w must be 0 or 1")

    @property
    def x(self):
        """
        Get the x coordinate.
        :return:
        """
        return self._x

    @property
    def y(self):
        """
        Get the y coordinate.
        :return:
        """
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def w(self):
        return self._w

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z
        elif item == 3:
            return self.w
        else:
            raise IndexError("Tuple index out of range")

    def __setitem__(self, key, value):
        if key == 0:
            self._x = value
        elif key == 1:
            self._y = value
        elif key == 2:
            self._z = value
        elif key == 3:
            self._w = value
        else:
            raise IndexError("Tuple index out of range")

    def __eq__(self, other):
        return (math.isclose(self.x, other.x, abs_tol=EPSILON) and
                math.isclose(self.y, other.y, abs_tol=EPSILON) and
                math.isclose(self.z, other.z, abs_tol=EPSILON) and
                math.isclose(self.w, other.w, abs_tol=EPSILON))

    def __add__(self, other):
        if self.w and other.w:
            raise TypeError("Can't add two points")

        return Tuple(self.x + other.x,
                     self.y + other.y,
                     self.z + other.z,
                     self.w + other.w)

    def __sub__(self, other):
        return Tuple(self.x - other.x,
                     self.y - other.y,
                     self.z - other.z,
                     self.w - other.w)

    def __neg__(self):
        return Tuple(-self.x, -self.y, -self.z, self.w)

    def __mul__(self, scalar):
        return Tuple(self.x * scalar,
                     self.y * scalar,
                     self.z * scalar,
                     self.w)

    def __truediv__(self, scalar):
        return Tuple(self.x / scalar,
                     self.y / scalar,
                     self.z / scalar,
                     self.w)

    def __repr__(self):
        return f"{self.__class__.__name__}(x:{self.x}, y:{self.y}, z:{self.z}, w:{self.w})"


class Point(Tuple):
    """
    Convenience class for a point in 3D space.
    """

    def __init__(self, x, y, z):
        super().__init__(x, y, z, 1.0)


class Vector(Tuple):
    """
    Convenience class for a vector in 3D space.
    """

    def __init__(self, x, y, z):
        super().__init__(x, y, z, 0.0)

    def magnitude(self) -> float:
        """
        Return the magnitude of the vector.
        :return: float
        """
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):
        """
        Return a normalized vector.
        :return: Vector
        """
        return self / self.magnitude()

    def dot(self, other: 'Vector') -> float:
        """
        Return the dot product of two vectors.
        :return: float
        :param other: Vector
        """
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

    def cross(self, other: 'Vector') -> 'Vector':
        """
        Return the cross product of two vectors.
        :param other: Vector
        :return: Vector
        """
        return Vector((self.y * other.z) - (self.z * other.y),
                      (self.z * other.x) - (self.x * other.z),
                      (self.x * other.y) - (self.y * other.x))

    def reflect(self, normal: 'Vector') -> 'Vector':
        return self - normal * 2 * self.dot(normal)


class Light:
    def __init__(self, position: Point, intensity: Color):
        self.position = position
        self.intensity = intensity
