import utils


class Canvas:
    def __init__(self, WIDTH: int, HEIGHT: int, bgcolor: tuple = (255, 255, 255)):
        self.WIDTH: int = WIDTH
        self.HEIGHT: int = HEIGHT
        self.bgcolor: tuple = bgcolor

        # Fill the pixel buffer with colors
        self.pixels = [
            [(0, 0, 0) for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)
        ]
        self.set_bgcolor()

    # Fill the pixel buffer with the given background color
    def set_bgcolor(self):
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                self.pixels[i][j] = self.bgcolor

    # Save the pixel buffer to a PPM file
    def save(self, file_name):
        with open(file_name, "w") as f:
            f.write("P3\n")
            f.write(f"{self.WIDTH} {self.HEIGHT}\n")
            for row in self.pixels:
                for pixel in row:
                    f.write(
                        f"{int(pixel[0]):03d} {int(pixel[1]):03d} {int(pixel[2]):03d} "
                    )
                f.write("\n")

    # DRAW A RECTANGLE
    def draw_rectangle(self, x1: int, y1: int, x2: int, y2: int, color: tuple):
        for i in range(max(0, y1 - 1), min(len(self.pixels), y2 + 1)):
            for j in range(max(0, x1 - 1), min(len(self.pixels[0]), x2 + 1)):
                self.pixels[i][j] = color

    # DRAW A LINE
    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color: tuple):
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        if dx >= dy:
            steps = dx
        else:
            steps = dy
        x_increment = (x2 - x1) / steps
        y_increment = (y2 - y1) / steps
        x = x1
        y = y1
        for _ in range(steps):
            self.pixels[int(y)][int(x)] = color
            x += x_increment
            y += y_increment

    # DRAW A CIRCLE
    def draw_circle(self, center: tuple, radius, color):
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if (
                    utils.square_root((x - center[0]) ** 2 + (y - center[1]) ** 2)
                    <= radius
                ):
                    self.pixels[y][x] = color


def main():
    import math

    HEIGHT = 400
    WIDTH = 400

    img = Canvas(WIDTH, HEIGHT)

    img.draw_circle(center=(WIDTH // 2, HEIGHT // 2), radius=50, color=(255, 0, 0))
    img.draw_circle(center=(25, 20), radius=15, color=(255, 200, 0))
    img.save("outputs/circle.ppm")


if __name__ == "__main__":
    main()
