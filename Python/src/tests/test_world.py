import unittest

from src.ray_tracer_challenge.color import Color, Colors
from src.ray_tracer_challenge.intersection import Intersection
from src.ray_tracer_challenge.matrix import Matrix
from src.ray_tracer_challenge.ray import Ray
from src.ray_tracer_challenge.sphere import Sphere
from src.ray_tracer_challenge.tuple import Light, Point, Vector
from src.ray_tracer_challenge.world import World


class TestWorld(unittest.TestCase):
    def setup_world(self):
        light = Light(Point(-10, 10, -10), Colors.WHITE)
        s1 = Sphere()
        s1.material.color = Color(0.8, 1.0, 0.6)
        s1.material.diffuse = 0.7
        s1.material.specular = 0.2

        s2 = Sphere()
        s2.transform = Matrix.scaling(0.5, 0.5, 0.5)

        world = World()
        world.light = light
        world.objects.append(s1)
        world.objects.append(s2)

        return world

    def test_create_world(self):
        world = World()
        self.assertEqual(world.objects, [])
        self.assertIsNone(world.light)

    def test_default_world(self):
        world = self.setup_world()
        self.assertEqual(Point(-10, 10, -10), world.light.position)
        self.assertEqual(Colors.WHITE, world.light.intensity)
        self.assertEqual(2, len(world.objects))

    def test_intersect_world_with_ray(self):
        world = self.setup_world()
        ray = Ray(Point(0, 0, -5), Vector(0, 0, 1))

        intersections = world.intersect(ray)
        self.assertEqual(4, intersections.count)
        self.assertEqual(4, intersections[0].t)
        self.assertEqual(4.5, intersections[1].t)
        self.assertEqual(5.5, intersections[2].t)
        self.assertEqual(6, intersections[3].t)

    def test_shading_an_intersection(self):
        world = self.setup_world()
        ray = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        shape = world.objects[0]
        intersection = Intersection(4, shape)
        comps = intersection.prepare_computations(ray)
        color = world.shade_hit(comps)
        self.assertEqual(Color(0.38066, 0.47583, 0.2855), color)

    def test_shading_an_intersection_from_the_inside(self):
        world = self.setup_world()
        world.light = Light(Point(0, 0.25, 0), Colors.WHITE)
        ray = Ray(Point(0, 0, 0), Vector(0, 0, 1))
        shape = world.objects[1]
        intersection = Intersection(0.5, shape)
        comps = intersection.prepare_computations(ray)
        color = world.shade_hit(comps)
        self.assertEqual(Color(0.90498, 0.90498, 0.90498), color)

    def test_color_when_ray_misses(self):
        world = self.setup_world()
        ray = Ray(Point(0, 0, -5), Vector(0, 1, 0))
        color = world.color_at(ray)
        self.assertEqual(Colors.BLACK, color)

    def test_color_when_ray_hits(self):
        world = self.setup_world()
        ray = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        color = world.color_at(ray)
        self.assertEqual(Color(0.38066, 0.47583, 0.2855), color)

    def test_color_with_intersection_behind_ray(self):
        world = self.setup_world()
        outer = world.objects[0]
        outer.material.ambient = 1
        inner = world.objects[1]
        inner.material.ambient = 1
        ray = Ray(Point(0, 0, 0.75), Vector(0, 0, -1))
        color = world.color_at(ray)
        self.assertEqual(inner.material.color, color)

    def test_no_shadow_when_nothing_collinear_with_point_and_light(self):
        world = self.setup_world()
        p = Point(0, 10, 0)
        self.assertFalse(world.is_shadowed(p))

    def test_shadow_when_object_is_between_point_and_light(self):
        world = self.setup_world()
        p = Point(10, -10, 10)
        self.assertTrue(world.is_shadowed(p))

    def test_no_shadow_with_object_behind_light(self):
        world = self.setup_world()
        p = Point(-20, 20, -20)
        self.assertFalse(world.is_shadowed(p))

    def test_no_shadow_with_object_behind_point(self):
        world = self.setup_world()
        p = Point(-2, 2, -2)
        self.assertFalse(world.is_shadowed(p))
