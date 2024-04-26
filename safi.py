class Canvas:
    def __init__(self, file_path: str, HEIGHT: int, WIDTH: int, bgcolor: tuple):
        self.file_path: str = file_path
        self.HEIGHT: int = HEIGHT
        self.WIDTH: int = WIDTH
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
    def save(self):
        with open(self.file_path, "w") as f:
            f.write("P3\n")
            f.write(f"{self.WIDTH} {self.HEIGHT}\n")
            for row in self.pixels:
                for pixel in row:
                    f.write(
                        f"{int(pixel[0]):03d} {int(pixel[1]):03d} {int(pixel[2]):03d} "
                    )
                f.write("\n")

    def draw_rectangle(self, x1: int, y1: int, x2: int, y2: int, color: tuple):
        for i in range(max(0, y1 - 1), min(len(self.pixels), y2 + 1)):
            for j in range(max(0, x1 - 1), min(len(self.pixels[0]), x2 + 1)):
                self.pixels[i][j] = color

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
            self.pixels[y][x] = color


def main():
    rows = 10
    cols = 10
    img = Canvas("output1.ppm", 400, 400, bgcolor=(255, 0, 255))
    # img.draw_rectangle(100, 100, 300, 300, color=(0, 0, 0))
    for y in range(0, rows):
        for x in range(0, cols):
            if (x + y) % 2 == 0:
                color = (255, 0, 0)
            else:
                color = (0, 255, 0)
            img.draw_rectangle(
                x * (400 // rows), y * (400 // rows), 400, 400, color=color
            )
    img.save()
    # img.draw_line(0, 0, 200, 300, color=(255, 0, 0))


if __name__ == "__main__":
    main()
