from safi2D.safi import Canvas


HEIGHT = 400
WIDTH = 400


# DRAW A CHECKERBOARD
# ------------------------#

dame = Canvas(WIDTH, HEIGHT)
rows = 8
cols = 8

for y in range(0, rows):
    for x in range(0, cols):
        if (x + y) % 2 == 0:
            color = (200, 100, 200)  # cyan-like color
        else:
            color = (0, 255, 100)  # Orange
        dame.draw_rectangle(x * (400 // rows), y * (400 // rows), 400, 400, color=color)
dame.save("outputs/checherboard.ppm")

# DRAW TWO PARALLEL LINES
# ------------------------#

# create a 400x400 canvas to draw on
crossinglines = Canvas(WIDTH, HEIGHT)

# Draw an horizontal line
crossinglines.draw_line(0, HEIGHT // 2, 400, HEIGHT // 2, color=(0, 255, 0))

# Draw a vertical line
crossinglines.draw_line(WIDTH // 2, 0, WIDTH // 2, 400, color=(255, 0, 0))
crossinglines.save("outputs/crossinglines.ppm")

# DRAW A TRIANGLE
# ----------------#
p1 = (100, 100)
p2 = (350, 100)
p3 = (300, 350)
triangle = Canvas(WIDTH, HEIGHT)
# draw a blue triangle
triangle.draw_triangle(p1, p2, p3, (255, 0, 0))

triangle.save("outputs/triangle.ppm")


# DRAW A POLYGON
# ---------------#
HEIGHT = 600
WIDTH = 600

polygon = Canvas(WIDTH, HEIGHT)

# List of 8 vertices(to draw an octogon)
vertices = [
    (300, 100),
    (450, 150),
    (500, 300),
    (450, 450),
    (300, 500),
    (150, 450),
    (100, 300),
    (150, 150),
]

# Draw an OCTOGON
polygon.draw_filled_polygon(vertices, (255, 200, 0))

polygon.save("outputs/filled_polygon.ppm")
