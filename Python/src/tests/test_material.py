import unittest

from src.ray_tracer_challenge.color import Color, Colors
from src.ray_tracer_challenge.material import Material
from src.ray_tracer_challenge.tuple import Light, Point, Vector


class TestMaterial(unittest.TestCase):
    def test_material_has_default_values(self):
        m = Material()
        self.assertEqual(m.color, Color(1, 1, 1))
        self.assertEqual(m.ambient, 0.1)
        self.assertEqual(m.diffuse, 0.9)
        self.assertEqual(m.specular, 0.9)
        self.assertEqual(m.shininess, 200.0)

    def test_with_eye_between_light_and_surface(self):
        m = Material()
        position = Point(0, 0, 0)
        normal_v = Vector(0, 0, -1)
        eye_v = Vector(0, 0, -1)
        light = Light(Point(0, 0, -10), Color(1, 1, 1))
        result = m.lighting(light, position, eye_v, normal_v, False)
        self.assertEqual(Color(1.9, 1.9, 1.9), result)

    def test_with_eye_between_light_and_surface_eye_offset_45_degrees(self):
        m = Material()
        position = Point(0, 0, 0)
        normal_v = Vector(0, 0, -1)
        eye_v = Vector(0, 2 ** 0.5 / 2, -2 ** 0.5 / 2)
        light = Light(Point(0, 0, -10), Color(1, 1, 1))
        result = m.lighting(light, position, eye_v, normal_v, False)
        self.assertEqual(Color(1.0, 1.0, 1.0), result)

    def test_with_eye_opposite_surface_light_offset_45_degrees(self):
        m = Material()
        position = Point(0, 0, 0)
        normal_v = Vector(0, 0, -1)
        eye_v = Vector(0, 0, -1)
        light = Light(Point(0, 10, -10), Color(1, 1, 1))
        result = m.lighting(light, position, eye_v, normal_v, False)
        self.assertEqual(Color(0.7364, 0.7364, 0.7364), result)

    def test_eye_in_path_of_reflection_vector(self):
        m = Material()
        position = Point(0, 0, 0)
        normal_v = Vector(0, 0, -1)
        eye_v = Vector(0, -2 ** 0.5 / 2, -2 ** 0.5 / 2)
        light = Light(Point(0, 10, -10), Color(1, 1, 1))
        result = m.lighting(light, position, eye_v, normal_v, False)
        self.assertEqual(Color(1.6364, 1.6364, 1.6364), result)

    def test_light_behind_surface(self):
        m = Material()
        position = Point(0, 0, 0)
        normal_v = Vector(0, 0, -1)
        eye_v = Vector(0, 0, -1)
        light = Light(Point(0, 0, 10), Color(1, 1, 1))
        result = m.lighting(light, position, eye_v, normal_v, False)
        self.assertEqual(Color(0.1, 0.1, 0.1), result)

    def test_lighting_with_surface_in_shadow(self):
        material = Material()
        position = Point(0, 0, 0)
        eye_v = Vector(0, 0, -1)
        normal_v = Vector(0, 0, -1)
        light = Light(Point(0, 0, -10), Colors.WHITE)
        in_shadow = True
        result = material.lighting(light, position, eye_v, normal_v, in_shadow)
        self.assertEqual(Color(0.1, 0.1, 0.1), result)
