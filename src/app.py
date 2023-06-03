import tkinter as tk
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageGrab


def main():
    app = App()
    app.mainloop()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Screenshot before 10 min")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.geometry(f"+{self.winfo_screenwidth() - 400}+{self.winfo_screenheight() - 300}")

        self.canvas = tk.Canvas(self, width=384, height=216)
        self.canvas.pack()

        Path("Screenshot").mkdir(exist_ok=True)
        for i, image in enumerate([Image.new("RGBA", (384, 216), "black") for i in range(10)]):
            ImageDraw.Draw(image).text((10, 0), str(i), "white", ImageFont.truetype("arial.ttf", 72))
            image.save(f"Screenshot/{i}.png")
        ImageGrab.grab().resize((384, 216)).save("Screenshot/10.png")

        self.display_image = tk.PhotoImage(file="Screenshot/0.png")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)

        self.after(60000, self.update_canvas)

    def update_canvas(self):
        Path("Screenshot/0.png").unlink()
        for i in range(10):
            Path(f"Screenshot/{i + 1}.png").rename(f"Screenshot/{i}.png")
        ImageGrab.grab().resize((384, 216)).save("Screenshot/10.png")

        self.display_image = tk.PhotoImage(file="Screenshot/0.png")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)

        self.after(60000, self.update_canvas)
