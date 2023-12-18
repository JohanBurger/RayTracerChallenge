import math

from src.ray_tracer_challenge.canvas import Canvas
from src.ray_tracer_challenge.color import Color, Colors
from src.ray_tracer_challenge.ray import Ray
from src.ray_tracer_challenge.sphere import Sphere
from src.ray_tracer_challenge.tuple import Point, Vector
from src.ray_tracer_challenge.matrix import Matrix


def create_test_image():
    (width, height) = (1024, 1024)
    c = Canvas(width, height)
    pixels = c.pixels
    for y in range(1024):
        for x in range(1024):
            color = Color(y / 1024, x / 1024, (2024 - x - y) / 2024)
            pixels[y][x] = color
    with open("test_image.ppm", "w") as f:
        f.write(c.to_ppm())


class Projectile:
    def __init__(self, position: Point, velocity: Vector):
        self.position = position
        self.velocity = velocity


class Environment:
    def __init__(self, gravity: Vector, wind: Vector):
        self.gravity = gravity
        self.wind = wind


def tick(environment: Environment, projectile: Projectile):
    position = projectile.position + projectile.velocity
    velocity = projectile.velocity + environment.gravity + environment.wind
    return Projectile(position, velocity)


def plot_projectile_trajectory():
    (width, height) = (1024, 800)
    c = Canvas(width, height)

    start = Point(0, 1, 0)
    velocity = Vector(1, 1.8, 0).normalize() * 11.25
    projectile = Projectile(start, velocity)

    gravity = Vector(0, -0.1, 0)
    wind = Vector(-0.01, 0, 0)
    environment = Environment(gravity, wind)

    while projectile.position.y > 0 and projectile.position.x < width:
        x = int(projectile.position.x)
        y = height - int(projectile.position.y)
        c.set_pixel(x, y, Colors.RED)
        projectile = tick(environment, projectile)

    with open("projectile_trajectory.ppm", "w") as f:
        f.write(c.to_ppm())


def trace_sphere():
    ray_origin = Point(0, 0, -5)
    wall_z = 10
    wall_size = 7.0
    canvas_pixels = 255
    pixel_size = wall_size / canvas_pixels
    half = wall_size / 2

    canvas = Canvas(canvas_pixels, canvas_pixels)
    color = Colors.RED
    sphere = Sphere()
    sphere.transform = Matrix.rotation_z(math.pi / 4) * Matrix.scaling(0.5, 1, 1)
    # sphere.transform = Matrix.shearing(1, 0, 0, 0, 0, 0) * Matrix.scaling(0.5, 1, 1)

    # For each row of pixels in the canvas
    for y in range(canvas_pixels):
        # Compute the world y coordinate (top = +half, bottom = -half)
        world_y = half - (pixel_size * y)
        # For each pixel in the row
        for x in range(canvas_pixels):
            # Compute the world x coordinate (left = -half, right = half)
            world_x = -half + (pixel_size * x)
            position = Point(world_x, world_y, wall_z)
            r = Ray(ray_origin, (position - ray_origin).normalize())
            xs = sphere.intersect(r)
            if xs.count > 0:
                canvas.set_pixel(x, y, color)

    with open("sphere.ppm", "w") as f:
        f.write(canvas.to_ppm())


def plot_clock():
    c = Canvas(200, 200)

    origin = Point(0, 0, 0)
    transformation = Matrix.translation(0, 80, 0)
    with_length = transformation * origin
    for i in range(12):
        with_rotation = Matrix.rotation_z(i * (math.pi / 6)) * with_length
        with_translation = Matrix.translation(100, 100, 0) * with_rotation
        c.set_pixel(int(with_translation.x), int(with_translation.y), Colors.RED)

    with open('clock.ppm', 'w') as f:
        f.write(c.to_ppm())


if __name__ == "__main__":
    # Create a test image with `create_test_image()`, or
    # Plot the trajectory of a projectile with `plot_projectile_trajectory()`
    # Plot the face of a clock with `plot_clock()`
    trace_sphere()
