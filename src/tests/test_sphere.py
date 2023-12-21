import math
import unittest

from src.ray_tracer_challenge.material import Material
from src.ray_tracer_challenge.matrix import Matrix
from src.ray_tracer_challenge.ray import Ray
from src.ray_tracer_challenge.sphere import Sphere
from src.ray_tracer_challenge.tuple import Point, Vector


class TestSphere(unittest.TestCase):
    def test_default_transformation(self):
        s = Sphere()
        self.assertEqual(Matrix.identity(), s.transform)

    def test_change_transformation(self):
        s = Sphere()
        t = Matrix.translation(2, 3, 4)
        s.transform = t
        self.assertIs(s.transform, t)

    def test_intersect_scaled_sphere_with_ray(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        s.transform = Matrix.scaling(2, 2, 2)
        xs = s.intersect(r)
        self.assertEqual(2, xs.count)
        self.assertEqual(3, xs[0].t)
        self.assertEqual(7, xs[1].t)

    def test_intersect_translated_sphere_with_ray(self):
        r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
        s = Sphere()
        s.transform = Matrix.translation(5, 0, 0)
        xs = s.intersect(r)
        self.assertEqual(0, xs.count)

    def test_calculate_normal_at_point_on_x_axis(self):
        s = Sphere()
        n = s.normal_at(Point(1, 0, 0))
        self.assertEqual(Vector(1, 0, 0), n)

    def test_calculate_normal_at_point_on_y_axis(self):
        s = Sphere()
        n = s.normal_at(Point(0, 1, 0))
        self.assertEqual(Vector(0, 1, 0), n)

    def test_calculate_normal_at_point_on_z_axis(self):
        s = Sphere()
        n = s.normal_at(Point(0, 0, 1))
        self.assertEqual(Vector(0, 0, 1), n)

    def test_calculate_normal_at_non_axial_point(self):
        s = Sphere()
        n = s.normal_at(Point(3 ** 0.5 / 3, 3 ** 0.5 / 3, 3 ** 0.5 / 3))
        self.assertEqual(Vector(3 ** 0.5 / 3, 3 ** 0.5 / 3, 3 ** 0.5 / 3), n)

    def test_normal_is_normalized(self):
        s = Sphere()
        n = s.normal_at(Point(3 ** 0.5 / 3, 3 ** 0.5 / 3, 3 ** 0.5 / 3))
        self.assertEqual(n, n.normalize())

    def test_normal_on_translated_sphere(self):
        s = Sphere()
        s.transform = Matrix.translation(0, 1, 0)
        n = s.normal_at(Point(0, 1.70711, -0.70711))
        self.assertEqual(Vector(0, 0.70711, -0.70711), n)

    def test_normal_on_transformed_sphere(self):
        s = Sphere()
        m = Matrix.scaling(1, 0.5, 1) * Matrix.rotation_z(math.pi / 5)
        s.transform = m
        n = s.normal_at(Point(0, 2 ** 0.5 / 2, -(2 ** 0.5) / 2))
        self.assertEqual(Vector(0, 0.97014, -0.24254), n)

    def test_sphere_has_default_material(self):
        s = Sphere()
        self.assertEqual(Material(), s.material)

    def test_sphere_may_be_assigned_material(self):
        s = Sphere()
        m = Material()
        m.ambient = 1
        s.material = m
        self.assertIs(m, s.material)
