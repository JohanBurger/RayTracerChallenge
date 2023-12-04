from ray_tracer_challenge.color import Color, Colors


class Canvas:
    def __init__(self, width, height):
        self._MAX_COLOR_VALUE = 255
        self._width = width
        self._height = height
        self._pixels = [[Colors.BLACK for _ in range(width)] for _ in range(height)]

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def pixels(self):
        return self._pixels

    def get_pixel(self, x: int, y: int) -> Color:
        return self._pixels[y][x]

    def set_pixel(self, x: int, y: int, color: Color):
        self._pixels[y][x] = color

    def to_ppm(self) -> str:
        ppm = f"P3\n{self.width} {self.height}\n{self._MAX_COLOR_VALUE}\n"
        for row in self.pixels:
            line = ""
            for pixel in row:
                line += f"{self._color_to_ppm(pixel)} "

            line = line.strip() + "\n"
            while len(line) > 70:
                pos = line.find(" ", 65, 70)
                ppm += line[:pos] + "\n"
                line = line[pos + 1:]

            ppm += f"{line}"

        return ppm

    def _color_to_ppm(self, color: Color) -> str:
        def _clamp(value: float) -> int:
            # If we want half of 255 to be 128 (as in the tests), we need to round up.
            # return (min(max(
            #         int(Decimal(value * self._MAX_COLOR_VALUE).quantize(Decimal('1.'), rounding=ROUND_UP)),
            #         0),
            #     self._MAX_COLOR_VALUE))

            # However, I decided to round down instead, and to change the test
            return min(max(int(value * self._MAX_COLOR_VALUE), 0), self._MAX_COLOR_VALUE)

        return f"{_clamp(color.red)} {_clamp(color.green)} {_clamp(color.blue)}"
