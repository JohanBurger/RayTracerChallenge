from typing import Optional


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
