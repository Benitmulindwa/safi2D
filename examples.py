from safi2D.safi import Canvas


HEIGHT = 400
WIDTH = 400


# DRAW A DAME
# ------------------------#

dame = Canvas(WIDTH, HEIGHT)
rows = 10
cols = 10


for y in range(0, rows):
    for x in range(0, cols):
        if (x + y) % 2 == 0:
            color = (200, 100, 200)  # cyan-like color
        else:
            color = (0, 255, 100)  # Orange
        dame.draw_rectangle(x * (400 // rows), y * (400 // rows), 400, 400, color=color)
dame.save("outputs/dame.ppm")

# DRAW TWO PARALLEL LINES
# ------------------------#

# create a 400x400 canvas to draw on
crossinglines = Canvas(WIDTH, HEIGHT)

# Draw an horizontal line
crossinglines.draw_line(0, HEIGHT // 2, 400, HEIGHT // 2, color=(0, 255, 0))

# Draw a vertical line
crossinglines.draw_line(WIDTH // 2, 0, WIDTH // 2, 400, color=(255, 0, 0))
crossinglines.save("outputs/crossinglines.ppm")
