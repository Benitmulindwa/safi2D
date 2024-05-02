import tkinter as tk
from PIL import Image, ImageTk


class GUIWindow:
    def __init__(self, image_path):
        self.root = tk.Tk()
        self.root.title("Image Viewer")

        self.image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(self.image)

        self.label = tk.Label(self.root, image=self.photo)
        self.label.pack()

    def run(self):
        self.root.mainloop()


def main():
    # image_path = "outputs/filled_polygon.ppm"
    # window = GUIWindow(image_path)
    # window.run()
    
# Load the PPM file
    with Image.open('outputs/filled_polygon.ppm') as im:
        # Save it in JPG format (you can replace 'jpg' with 'png' for PNG format)
        im.save('outputs/filled_polygon.jpg')



if __name__ == "__main__":
    main()
