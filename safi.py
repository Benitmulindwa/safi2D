# Fill the pixel buffer with colors
pixels = [[(0, 0, 0) for _ in range(400)] for _ in range(400)]

# Fill the pixel buffer with a red background
for i in range(400):
    for j in range(400):
        pixels[i][j] = (255, 255, 255)


def draw_rectangle():
    for i in range(100, 300):
        for j in range(100, 300):
            pixels[i][j] = (255, 0, 0)


# Save the pixel buffer to a PPM file
draw_rectangle()
with open("output.ppm", "w") as f:
    f.write("P3\n")
    f.write(f"{400} {400}\n")
    for row in pixels:
        for pixel in row:
            f.write(f"{int(pixel[0]):03d} {int(pixel[1]):03d} {int(pixel[2]):03d} ")
        f.write("\n")
