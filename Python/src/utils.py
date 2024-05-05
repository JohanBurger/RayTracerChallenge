import math
from collections import namedtuple

from PIL import Image

from src.ray_tracer_challenge.camera import Camera
from src.ray_tracer_challenge.canvas import Canvas
from src.ray_tracer_challenge.color import Color, Colors
from src.ray_tracer_challenge.ray import Ray
from src.ray_tracer_challenge.sphere import Sphere
from src.ray_tracer_challenge.tuple import Light, Point, Vector
from src.ray_tracer_challenge.matrix import Matrix
from src.ray_tracer_challenge.world import World


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


def render_sphere(with_ligthing: False):
    ray_origin = Point(0, 0, -5)
    wall_z = 10
    wall_size = 7.0
    canvas_pixels = 1024
    pixel_size = wall_size / canvas_pixels
    half = wall_size / 2

    canvas = Canvas(canvas_pixels, canvas_pixels)
    sphere = Sphere()
    sphere.material.color = Color(1, 0.2, 1)

    light_position = Point(-10, 10, -10)
    light_color = Color(1, 1, 1)
    light = Light(light_position, light_color)

    # Scale and rotate with: sphere.transform = Matrix.rotation_z(math.pi / 4) * Matrix.scaling(0.5, 1, 1)
    # Shear with: sphere.transform = Matrix.shearing(1, 0, 0, 0, 0, 0) * Matrix.scaling(0.5, 1, 1)

    # For each row of pixels in the canvas
    for y in range(canvas_pixels):
        # Compute the world y coordinate (top = +half, bottom = -half)
        world_y = half - (pixel_size * y)
        print('{y} of {canvas_pixels}'.format(y=y, canvas_pixels=canvas_pixels))
        # For each pixel in the row
        for x in range(canvas_pixels):
            # Compute the world x coordinate (left = -half, right = half)
            world_x = -half + (pixel_size * x)
            position = Point(world_x, world_y, wall_z)
            r = Ray(ray_origin, (position - ray_origin).normalize())
            xs = sphere.intersect(r)
            hit = xs.hit()
            if hit is not None:
                if with_ligthing:
                    position = r.position(hit.t)
                    color = sphere.material.lighting(light, position, -r.direction.normalize(),
                                                     sphere.normal_at(position))
                else:
                    color = Colors.RED
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


def adjust_plane(sphere):
    scaling = Matrix.scaling(10, 0.01, 10)
    color = Color(1, 0.9, 0.9)
    specular = 0
    sphere.transform = sphere.transform * scaling
    sphere.material.color = color
    sphere.material.specular = specular


def render_with_camera(resolution):
    floor = Sphere()
    adjust_plane(floor)

    left_wall = Sphere()
    left_wall.transform = (Matrix.translation(0, 0, 5) *
                           Matrix.rotation_y(-math.pi / 4) *
                           Matrix.rotation_x(math.pi / 2))
    adjust_plane(left_wall)

    right_wall = Sphere()
    right_wall.transform = (Matrix.translation(0, 0, 5) *
                            Matrix.rotation_y(math.pi / 4) *
                            Matrix.rotation_x(math.pi / 2))
    adjust_plane(right_wall)

    middle = Sphere()
    middle.transform = Matrix.translation(-0.5, 1, 0.5)
    middle.material.color = Color(0.1, 1, 0.5)
    middle.material.diffuse = 0.7
    middle.material.specular = 0.3

    right = Sphere()
    right.transform = Matrix.translation(1.5, 0.5, -0.5) * Matrix.scaling(0.5, 0.5, 0.5)
    right.material.color = Color(0.5, 1, 0.1)
    right.material.diffuse = 0.7
    right.material.specular = 0.3

    left = Sphere()
    left.transform = Matrix.translation(-1.5, 0.33, -0.75) * Matrix.scaling(0.33, 0.33, 0.33)
    left.material.color = Color(1, 0.8, 0.1)
    left.material.diffuse = 0.7
    left.material.specular = 0.3

    world = World()
    world.objects.extend([floor, left_wall, right_wall, middle, right, left])
    world.light = Light(Point(-10, 10, -10), Colors.WHITE)
    print('Created world!')

    camera = Camera(resolution.horizontal_pixels, resolution.vertical_pixels, math.pi / 3)
    camera.transform = Matrix.view_transform(Point(0, 1.5, -5), Point(0, 1, 0), Vector(0, 1, 0))
    print('Created camera!')

    print('Rendering world!')
    canvas = camera.render(world)
    name = 'render_with_camera'
    ppm_file = f'{name}.ppm'
    with open(ppm_file, 'w') as f:
        f.write(canvas.to_ppm())
    image = Image.open(ppm_file)
    image.save(f'{name}.jpg')
    print('Done!')


Resolution = namedtuple("Resolution", "horizontal_pixels vertical_pixels")
resolution_480p = Resolution(640, 480)  # 307 200 px
resolution_720p = Resolution(1280, 720)  # 921 600 px
resolution_1080p = Resolution(1920, 1080)  # 2 073 600 px

if __name__ == "__main__":
    # Create a test image with `create_test_image()`, or
    # Plot the trajectory of a projectile with `plot_projectile_trajectory()`
    # Plot the face of a clock with `plot_clock()`
    # Render a pretty sphere with render_sphere(with_ligthing=True)
    render_with_camera(resolution_720p)
