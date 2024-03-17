from src.ray_tracer_challenge.intersection import Intersection
from src.ray_tracer_challenge.ray import Ray


class World:
    def __init__(self):
        self.objects = []
        self.light = None

    def intersect(self, ray: Ray) -> []:
        intersections = []
        for obj in self.objects:
            intersections.extend(obj.intersect(ray))
        intersections.sort(key=lambda x: x.t)
        return intersections
