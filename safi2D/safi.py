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

    # DRAW A LINE(Bresenham's line drawing algorithm)
    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color: tuple):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        if dx >= dy:
            steps = dx
            x_increment = 1 if x2 > x1 else -1
            y_increment = dy / dx if y2 > y1 else -dy / dx
        else:
            steps = dy
            y_increment = 1 if y2 > y1 else -1
            x_increment = dx / dy if x2 > x1 else -dx / dy
        x = x1
        y = y1
        for _ in range(int(steps)):
            self.pixels[int(y)][int(x)] = color
            x += x_increment
            y += y_increment

    """
    DRAW A CIRCLE
    using the Bresenham's circle drawing algorithm: https://www.geeksforgeeks.org/bresenhams-circle-drawing-algorithm/)
    
    """

    def draw_circle(self, center: tuple, radius, color):
        x, y = center
        x = int(x)
        y = int(y)
        radius = int(radius)
        # Initialize variables
        d = 3 - 2 * radius
        x_ = 0
        y_ = radius
        # Draw circle points
        while x_ <= y_:
            self._draw_circle_points(x, y, x_, y_, color)
            x_ += 1
            if d < 0:
                d += 4 * x_ + 6
            else:
                d += 4 * (x_ - y_) + 10
                y_ -= 1

    # Draw circle points
    def _draw_circle_points(self, cx, cy, x, y, color):
        self._plot_point(cx + x, cy + y, color)
        self._plot_point(cx - x, cy + y, color)
        self._plot_point(cx + x, cy - y, color)
        self._plot_point(cx - x, cy - y, color)
        self._plot_point(cx + y, cy + x, color)
        self._plot_point(cx - y, cy + x, color)
        self._plot_point(cx + y, cy - x, color)
        self._plot_point(cx - y, cy - x, color)

    # Helper method to plot a point
    def _plot_point(self, x, y, color):
        if 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT:
            self.pixels[y][x] = color

    """------------------------------------------------------------------"""

    # DRAW A TRIANGLE(by intersection of three lines)
    def draw_triangle(self, p1: tuple, p2: tuple, p3: tuple, color: tuple):
        self.draw_line(*p1, *p2, color)
        self.draw_line(*p2, *p3, color)
        self.draw_line(*p3, *p1, color)


def main():
    import time

    start = time.time()
    HEIGHT = 400
    WIDTH = 400

    # TESTs
    img = Canvas(WIDTH, HEIGHT)
    # img.draw_rectangle(100, 100, 300, 300, color=(0, 0, 0))
    # img.draw_circle(center=(WIDTH // 2, HEIGHT // 2), radius=50, color=(255, 0, 0))
    # img.draw_circle(center=(25, 20), radius=15, color=(255, 200, 0))
    # img.draw_line(0, HEIGHT // 2, 600, HEIGHT // 2, color=(0, 255, 0))
    # img.draw_line(WIDTH // 2, 0, WIDTH // 2, 600, color=(255, 0, 0))
    # img.save("outputs/circle.ppm")
    p1 = (100, 100)
    p2 = (350, 100)
    p3 = (300, 350)

    img.draw_triangle(p1, p2, p3, (255, 0, 0))
    img.save("outputs/triangle.ppm")
    end = time.time()

    print(f"Execution time: {end-start} secondes")


if __name__ == "__main__":
    main()
