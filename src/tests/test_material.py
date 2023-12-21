import unittest

from src.ray_tracer_challenge.color import Color
from src.ray_tracer_challenge.material import Material


class TestMaterial(unittest.TestCase):
    def test_material_has_default_values(self):
        m = Material()
        self.assertEqual(m.color, Color(1, 1, 1))
        self.assertEqual(m.ambient, 0.1)
        self.assertEqual(m.diffuse, 0.9)
        self.assertEqual(m.specular, 0.9)
        self.assertEqual(m.shininess, 200.0)
