# Fill the pixel buffer with colors
pixels = [[(0, 0, 0) for _ in range(400)] for _ in range(400)]

# Fill the pixel buffer with a red background
for i in range(400):
    for j in range(400):
        pixels[i][j] = (255, 255, 255)


def draw_rectangle(x1, y1, x2, y2):
    for i in range(max(0, y1 - 1), min(len(pixels), y2 + 1)):
        for j in range(max(0, x1 - 1), min(len(pixels[0]), x2 + 1)):
            pixels[i][j] = (255, 0, 0)


# Save the pixel buffer to a PPM file
draw_line(0, 0, 100, 100)
with open("output.ppm", "w") as f:
    f.write("P3\n")
    f.write(f"{400} {400}\n")
    for row in pixels:
        for pixel in row:
            f.write(f"{int(pixel[0]):03d} {int(pixel[1]):03d} {int(pixel[2]):03d} ")
        f.write("\n")
