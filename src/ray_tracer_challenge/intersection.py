from typing import Optional

from src.ray_tracer_challenge.ray import Ray


class Computations:
    def __init__(self, t, object, point, eye_vector, normal_vector, inside):
        self._t = t
        self._object = object
        self._point = point
        self._eye_vector = eye_vector
        self._normal_vector = normal_vector
        self._inside = inside

    @property
    def t(self):
        return self._t

    @property
    def object(self):
        return self._object

    @property
    def point(self):
        return self._point

    @property
    def eye_vector(self):
        return self._eye_vector

    @property
    def normal_vector(self):
        return self._normal_vector

    @property
    def inside(self):
        return self._inside


class Intersection():
    def __init__(self, t, object):
        self._t = t
        self._object = object

    @property
    def t(self):
        return self._t

    @property
    def object(self):
        return self._object

    def prepare_computations(self, r: Ray) -> Computations:
        point = r.position(self.t)
        eye_vector = -r.direction
        normal_vector = self.object.normal_at(point)
        inside = False
        if normal_vector.dot(eye_vector) < 0:
            inside = True
            normal_vector = -normal_vector
        return Computations(self.t, self.object, point, eye_vector, normal_vector, inside)


class Intersections:
    def __init__(self, *args):
        self._intersections = list(args)

    def __getitem__(self, key):
        return self._intersections[key]

    @property
    def count(self):
        return len(self._intersections)

    @property
    def intersections(self):
        return self._intersections

    def hit(self) -> Optional[Intersection]:
        hits = sorted([i for i in self._intersections if i.t >= 0], key=lambda x: x.t)
        if len(hits) == 0:
            return None
        else:
            return hits[0]
