from src.ray_tracer_challenge.color import Color
from src.ray_tracer_challenge.intersection import Computations, Intersection, Intersections
from src.ray_tracer_challenge.ray import Ray
from src.ray_tracer_challenge.tuple import Point, Vector


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

    def shade_hit(self, computations: Computations) -> Color:
        return computations.object.material.lighting(self.light,
                                                     computations.point,
                                                     computations.eye_vector,
                                                     computations.normal_vector,
                                                     self.is_shadowed(computations.point))

    def color_at(self, ray: Ray) -> Color:
        intersections = self.intersect(ray)
        hit = intersections.hit()
        if hit is None:
            return Color(0, 0, 0)
        comps = hit.prepare_computations(ray)
        return self.shade_hit(comps)

    def is_shadowed(self, point: Point) -> bool:
        v = self.light.position - point
        distance = v.magnitude()
        direction = Vector.normalize(v)
        r = Ray(point, direction)
        intersections = self.intersect(r)
        hit = intersections.hit()
        return hit is not None and hit.t < distance
