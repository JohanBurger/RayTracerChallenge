import math

from src.ray_tracer_challenge.color import Color, Colors
from src.ray_tracer_challenge.constants import EPSILON
from src.ray_tracer_challenge.tuple import Light, Point, Vector


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

    def lightning(self, light: Light, position: Point, eye_v: Vector, normal_v: Vector) -> Color:
        # Combine the surface color with the light's color/intensity.
        effective_color = self.color * light.intensity

        # Compute the diffuse contribution.
        light_v = (light.position - position).normalize()
        ambient = effective_color * self.ambient

        light_dot_normal = normal_v.dot(light_v)

        if light_dot_normal < 0:
            diffuse = Colors.BLACK
            specular = Colors.BLACK
        else:
            diffuse = effective_color * self.diffuse * light_dot_normal

            # reflect_dot_eye represents the cosine of the angle between the reflection vector
            # and the eye vector. A negative number means the light reflects away from the eye.
            reflect_v = -light_v.reflect(normal_v)
            reflect_dot_eye = reflect_v.dot(eye_v)

            if reflect_dot_eye <= 0:
                specular = Colors.BLACK
            else:
                # Compute the specular contribution.
                factor = reflect_dot_eye ** self.shininess
                specular = light.intensity * self.specular * factor

        return ambient + diffuse + specular
