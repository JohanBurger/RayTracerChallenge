from src.ray_tracer_challenge.color import Color
from src.ray_tracer_challenge.intersection import Computations, Intersection, Intersections
from src.ray_tracer_challenge.ray import Ray


class World:
    def __init__(self):
        self.objects = []
        self.light = None

    def intersect(self, ray: Ray) -> []:
        intersections = Intersections()
        for obj in self.objects:
            intersections.extend(obj.intersect(ray))
        intersections.sort(key=lambda x: x.t)
        return intersections

    def shade_hit(self, comps: Computations) -> Color:
        return comps.object.material.lighting(self.light,
                                              comps.point,
                                              comps.eye_vector,
                                              comps.normal_vector)

    def color_at(self, ray: Ray) -> Color:
        intersections = self.intersect(ray)
        hit = intersections.hit()
        if hit is None:
            return Color(0, 0, 0)
        comps = hit.prepare_computations(ray)
        return self.shade_hit(comps)
