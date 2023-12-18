from src.ray_tracer_challenge.matrix import Matrix
from src.ray_tracer_challenge.tuple import Point, Vector


class Ray:
    def __init__(self, origin: Point, direction: Vector):
        self._origin = origin
        self._direction = direction

    def __repr__(self):
        return f"Ray(origin:{self._origin}, direction:{self._direction})"

    @property
    def origin(self) -> Point:
        return self._origin

    @property
    def direction(self) -> Vector:
        return self._direction

    def position(self, t: float) -> Point:
        return self._origin + (self._direction * t)

    def transform(self, transformation: Matrix):
        return Ray(transformation * self._origin, transformation * self._direction)
