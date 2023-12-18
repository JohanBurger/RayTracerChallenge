from src.ray_tracer_challenge.intersection import Intersection, Intersections
from src.ray_tracer_challenge.matrix import Matrix
from src.ray_tracer_challenge.ray import Ray
from src.ray_tracer_challenge.tuple import Point


class Sphere:
    def __init__(self):
        self.transform = Matrix.identity()

    def __repr__(self):
        return f"Sphere(transform:{self.transform})"

    def intersect(self, ray: Ray) -> Intersections:
        obj_coord_ray = ray.transform(self.transform.inverse())
        sphere_to_ray = obj_coord_ray.origin - Point(0, 0, 0)
        a = obj_coord_ray.direction.dot(obj_coord_ray.direction)
        b = 2 * obj_coord_ray.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1

        discriminant = b ** 2 - 4 * a * c
        if discriminant < 0:
            return Intersections()

        t1 = (-b - discriminant ** 0.5) / (2 * a)
        t2 = (-b + discriminant ** 0.5) / (2 * a)

        return Intersections(Intersection(t1, self), Intersection(t2, self))
