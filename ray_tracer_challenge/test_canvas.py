import unittest

from ray_tracer_challenge.canvas import Canvas
from ray_tracer_challenge.color import Color, Colors


class TestCanvas(unittest.TestCase):
    def test_canvas_has_correct_width_and_height(self):
        c = Canvas(10, 20)
        self.assertEqual(c.width, 10)
        self.assertEqual(c.height, 20)

    def test_canvas_initializes_with_all_black_pixels(self):
        c = Canvas(10, 20)
        for row in c.pixels:
            for pixel in row:
                self.assertEqual(pixel, Colors.BLACK)

    def test_canvas_writes_pixel(self):
        c = Canvas(10, 20)
        (x, y) = (2, 3)
        c.set_pixel(x, y, Colors.RED)
        self.assertEqual(c.get_pixel(x, y), Colors.RED)

    def test_canvas_to_ppm(self):
        (width, height) = (5, 3)
        c = Canvas(width, height)
        c1 = Color(1.5, 0, 0)
        c2 = Color(0, 0.5, 0)
        c3 = Color(-0.5, 0, 1)
        c.set_pixel(0, 0, c1)
        c.set_pixel(2, 1, c2)
        c.set_pixel(4, 2, c3)
        ppm = c.to_ppm()
        lines = ppm.splitlines()
        self.assertEqual(3 + height, len(lines))
        self.assertEqual("P3", lines[0])
        self.assertEqual("5 3", lines[1])
        self.assertEqual("255", lines[2])
        self.assertEqual("255 0 0 0 0 0 0 0 0 0 0 0 0 0 0", lines[3])
        self.assertEqual("0 0 0 0 0 0 0 127 0 0 0 0 0 0 0", lines[4])
        self.assertEqual("0 0 0 0 0 0 0 0 0 0 0 0 0 0 255", lines[5])

    def test_canvas_to_ppm_long_lines_are_split(self):
        (width, height) = (10, 2)
        c = Canvas(width, height)
        for y in range(height):
            for x in range(width):
                c.set_pixel(x, y, Color(1, 0.8, 0.6))

        ppm = c.to_ppm()
        lines = ppm.splitlines()
        self.assertEqual(7, len(lines))
        self.assertEqual("255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204", lines[3])
        self.assertEqual("153 255 204 153 255 204 153 255 204 153 255 204 153", lines[4])
        self.assertEqual("255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204", lines[5])
        self.assertEqual("153 255 204 153 255 204 153 255 204 153 255 204 153", lines[6])

    def test_canvas_to_ppm_ends_with_newline(self):
        c = Canvas(5, 3)
        ppm = c.to_ppm()
        self.assertEqual("\n", ppm[-1])
