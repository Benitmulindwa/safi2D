import tkinter as tk
from PIL import Image, ImageTk


class GUIWindow:
    def __init__(self, image_path):
        self.root = tk.Tk()
        self.root.title("Safi2D")
        self.root.iconbitmap("logo.ico")
        self.icon_photo = ImageTk.PhotoImage(Image.open("logo.png"))
        self.root.iconphoto(True, self.icon_photo)

        self.image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(self.image)

        self.label = tk.Label(self.root, image=self.photo)
        self.label.pack()

    def run(self):
        self.root.mainloop()


def main():
    image_path = "outputs/filled_circle.png"
    window = GUIWindow(image_path)
    window.run()
    # with Image.open("logo.webp") as img:
    #     img.save("logo.ico")


if __name__ == "__main__":
    main()
