import unittest

from src.ray_tracer_challenge.color import Color, Colors
from src.ray_tracer_challenge.matrix import Matrix
from src.ray_tracer_challenge.ray import Ray
from src.ray_tracer_challenge.sphere import Sphere
from src.ray_tracer_challenge.tuple import Light, Point, Vector
from src.ray_tracer_challenge.world import World


class TestWorld(unittest.TestCase):
    _world = None

    @classmethod
    def setUpClass(cls):
        light = Light(Point(-10, 10, -10), Colors.WHITE)
        s1 = Sphere()
        s1.material.color = Color(0.8, 1.0, 0.6)
        s1.material.diffuse = 0.7
        s1.material.specular = 0.2

        s2 = Sphere()
        s2.transform = Matrix.scaling(0.5, 0.5, 0.5)

        w = World()
        w.light = light
        w.objects.append(s1)
        w.objects.append(s2)

        cls._world = w

    def test_create_world(self):
        w = World()
        self.assertEqual(w.objects, [])
        self.assertIsNone(w.light)

    def test_default_world(self):
        self.assertEqual(Point(-10, 10, -10), self._world.light.position)
        self.assertEqual(Colors.WHITE, self._world.light.intensity)
        self.assertEqual(2, len(self._world.objects))

    def test_intersect_world_with_ray(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        xs = self._world.intersect(r)
        self.assertEqual(4, len(xs))
        self.assertEqual(4, xs[0].t)
        self.assertEqual(4.5, xs[1].t)
        self.assertEqual(5.5, xs[2].t)
        self.assertEqual(6, xs[3].t)
