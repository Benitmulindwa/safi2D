import math, os
from PIL import Image, ImageTk
import tkinter as tk


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
    def save(self, file_name: str):
        format_list = [".png", ".jpg", ".PNG"]  # List of supported formats
        ppm_file = file_name.replace(
            *(f for f in format_list if f in file_name), ".ppm"
        )
        with open(ppm_file, "w") as f:
            f.write("P3\n")
            f.write(f"{self.WIDTH} {self.HEIGHT}\n")
            f.write("255\n")
            for row in self.pixels:
                for pixel in row:
                    f.write(
                        f"{int(pixel[0]):03d} {int(pixel[1]):03d} {int(pixel[2]):03d} "
                    )
                f.write("\n")
        with Image.open(ppm_file) as img:
            img.save(file_name)
        os.remove(ppm_file)

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

    def draw_circle(self, center: tuple, radius: int, color: tuple):
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
            span_width = int(math.sqrt(radius**2 - (y - cy) ** 2))

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

    # DRAW A BÉZIER CURVE
    def draw_bezier_curve(
        self, control_points: list, color: tuple, num_segments: int = 100
    ):
        n = len(control_points)
        if n < 2:
            return

        # Calculate points along the curve using De Casteljau's algorithm
        t_values = [i / num_segments for i in range(num_segments + 1)]
        curve_points = []
        for t in t_values:
            points = control_points[:]
            while len(points) > 1:
                new_points = []
                for i in range(len(points) - 1):
                    x = (1 - t) * points[i][0] + t * points[i + 1][0]
                    y = (1 - t) * points[i][1] + t * points[i + 1][1]
                    new_points.append((x, y))
                points = new_points
            curve_points.append(points[0])

        # Draw the curve by connecting the calculated points
        for i in range(len(curve_points) - 1):
            x1, y1 = curve_points[i]
            x2, y2 = curve_points[i + 1]
            self.draw_line(int(x1), int(y1), int(x2), int(y2), color)

    def show(self):
        root = tk.Tk()
        root.title("Canvas")
        root.iconbitmap("assets/logo.ico")

        # Convert the pixels to an image
        img = Image.new("RGB", (self.WIDTH, self.HEIGHT))
        pixels_flat = [color for row in self.pixels for color in row]
        img.putdata(pixels_flat)

        # Convert the image to a format compatible with Tkinter
        img_tk = ImageTk.PhotoImage(img)

        # Create a label to display the image
        label = tk.Label(root, image=img_tk)
        label.pack()

        root.mainloop()


import time


def animate(canvas):
    # Define keyframes
    keyframes = [
        # Example keyframe: (x, y, color)
        ((100, 100), (255, 0, 0)),
        ((300, 300), (0, 0, 255)),
        ((100, 500), (0, 255, 0)),
    ]

    # Interpolation
    num_frames_between_keyframes = 30  # Adjust as needed
    frames = []
    for i in range(len(keyframes) - 1):
        start_frame = keyframes[i]
        end_frame = keyframes[i + 1]
        for j in range(num_frames_between_keyframes):
            frame = interpolate(
                start_frame, end_frame, j / num_frames_between_keyframes
            )
            frames.append(frame)
    i = 0
    # Rendering
    for frame in frames:
        canvas.set_bgcolor()  # Clear canvas
        canvas.draw_filled_circle(frame[0], 50, frame[1])  # Draw circle
        canvas.save(f"frames/frame{i}.png")  # Save frame as png
        i += 1
        time.sleep(0.01)


def interpolate(start_frame, end_frame, alpha):
    # Linear interpolation
    start_pos, start_color = start_frame
    end_pos, end_color = end_frame
    interp_pos = (
        int(start_pos[0] + alpha * (end_pos[0] - start_pos[0])),
        int(start_pos[1] + alpha * (end_pos[1] - start_pos[1])),
    )
    interp_color = (
        int(start_color[0] + alpha * (end_color[0] - start_color[0])),
        int(start_color[1] + alpha * (end_color[1] - start_color[1])),
        int(start_color[2] + alpha * (end_color[2] - start_color[2])),
    )
    return (interp_pos, interp_color)


def main():
    canvas = Canvas(600, 600, bgcolor=(0, 0, 0))
    canvas.draw_filled_circle((200, 100), 80, (200, 200, 40))
    canvas.draw_filled_circle((200, 300), 80, (100, 250, 90))
    canvas.draw_line(0, 0, 600, 600, (250, 250, 250))
    # animate(canvas)
    canvas.show()


if __name__ == "__main__":
    main()
