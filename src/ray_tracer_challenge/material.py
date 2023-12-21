import math

from src.ray_tracer_challenge.color import Color
from src.ray_tracer_challenge.constants import EPSILON


class Material:
    def __init__(self):
        self.color = Color(1, 1, 1)
        self.ambient = 0.1
        self.diffuse = 0.9
        self.specular = 0.9
        self.shininess = 200.0

    def __eq__(self, other):
        return self.color == other.color and \
            math.isclose(self.ambient, other.ambient, rel_tol=EPSILON) and \
            math.isclose(self.diffuse, other.diffuse, rel_tol=EPSILON) and \
            math.isclose(self.specular, other.specular, rel_tol=EPSILON) and \
            math.isclose(self.shininess, other.shininess, rel_tol=EPSILON)
