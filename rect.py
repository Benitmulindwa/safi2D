from safi import Canvas

rows = 10
cols = 10
img = Canvas("dame.ppm", 400, 400, bgcolor=(0, 0, 0))
img.draw_rectangle(100, 100, 300, 300, color=(0, 0, 0))
for y in range(0, rows):
    for x in range(0, cols):
        if (x + y) % 2 == 0:
            color = (200, 100, 200)
        else:
            color = (0, 255, 100)
        img.draw_rectangle(x * (400 // rows), y * (400 // rows), 400, 400, color=color)
img.save()
