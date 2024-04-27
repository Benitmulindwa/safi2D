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

    # DRAW A POLYGON
    def draw_polygon(self, points: list, color: tuple):
        num_points = len(points)
        for i in range(num_points):
            # Connect each point to the next one
            self.draw_line(*points[i], *points[(i + 1) % num_points], color)

    # DRAW FILLED POLYGON

    def draw_filled_polygon(self, points: list, color: tuple):
        # Find the minimum and maximum y-coordinates of the polygon
        min_y = min(point[1] for point in points)
        max_y = max(point[1] for point in points)

        # Iterate over each scanline within the polygon's bounding box
        for y in range(min_y, max_y + 1):
            intersections = []  # List to store x-coordinates of intersections
            num_points = len(points)

            # Iterate over each edge of the polygon
            for i in range(num_points):
                x1, y1 = points[i]
                x2, y2 = points[(i + 1) % num_points]

                # Check if the edge intersects with the current scanline
                if (y1 <= y < y2) or (y2 <= y < y1):
                    # Calculate the x-coordinate of the intersection point
                    x_intersection = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                    intersections.append(x_intersection)

            # Sort the intersection points in increasing order
            intersections.sort()

            # Fill the pixels between pairs of intersection points
            for i in range(0, len(intersections), 2):
                x_start = max(0, int(intersections[i]))
                x_end = min(self.WIDTH - 1, int(intersections[i + 1]))
                for x in range(x_start, x_end + 1):
                    self.pixels[y][x] = color

    # DRAW A FILLED CIRCLE
    def draw_filled_circle(self, center: tuple, radius: int, color: tuple):
        cx, cy = center

        # Iterate over each scanline within the circle's bounding box
        for y in range(cy - radius, cy + radius + 1):
            # Calculate the width of the span at this y coordinate
            span_width = int(utils.square_root(radius**2 - (y - cy) ** 2))

            # Calculate the starting and ending x-coordinates of the span
            x_start = max(0, cx - span_width)
            x_end = min(self.WIDTH - 1, cx + span_width)

            # Fill the pixels within the span with the specified color
            for x in range(x_start, x_end + 1):
                self.pixels[y][x] = color

    # DRAW AN ELLIPSE
    def draw_filled_ellipse(self, center: tuple, rx: int, ry: int, color: tuple):
        cx, cy = center
        rx_sq = rx * rx
        ry_sq = ry * ry
        x = 0
        y = ry
        px = 0
        py = 2 * rx_sq * y

        # Region 1
        p = round(ry_sq - (rx_sq * ry) + (0.25 * rx_sq))
        while px < py:
            x += 1
            px += 2 * ry_sq
            if p < 0:
                p += ry_sq + px
            else:
                y -= 1
                py -= 2 * rx_sq
                p += ry_sq + px - py
            self._plot_ellipse_points(cx, cy, x, y, color)

        # Region 2
        p = round(ry_sq * (x + 0.5) ** 2 + rx_sq * (y - 1) ** 2 - rx_sq * ry_sq)
        while y > 0:
            y -= 1
            py -= 2 * rx_sq
            if p > 0:
                p += rx_sq - py
            else:
                x += 1
                px += 2 * ry_sq
                p += rx_sq - py + px
            self._plot_ellipse_points(cx, cy, x, y, color)

    # Helper method to plot points symmetrically
    def _plot_ellipse_points(self, cx: int, cy: int, x: int, y: int, color: tuple):
        self.pixels[cy + y][cx + x] = color
        self.pixels[cy + y][cx - x] = color
        self.pixels[cy - y][cx + x] = color
        self.pixels[cy - y][cx - x] = color


def main():
    import time

    start = time.time()
    HEIGHT = 400
    WIDTH = 400

    # TESTs
    img = Canvas(WIDTH, HEIGHT)
    # img.draw_rectangle(100, 100, 300, 300, color=(0, 0, 0))
    img.draw_filled_ellipse(
        center=(WIDTH // 2, HEIGHT // 2), rx=100, ry=50, color=(0, 255, 0)
    )

    img.save("outputs/ellipse.ppm")

    end = time.time()

    print(f"Execution time: {end-start} secondes")


if __name__ == "__main__":
    main()
