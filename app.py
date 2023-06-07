import tkinter as tk
from fractions import Fraction
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

        Path("Screenshots").mkdir(exist_ok=True)
        for i, image in enumerate([Image.new("RGBA", (384, 216), "black") for _ in range(60)]):
            ImageDraw.Draw(image).text((10, 0), f"{i // 6} + {Fraction(i % 6, 6)}", "white", ImageFont.truetype("arial.ttf", 36))
            image.save(f"Screenshots/{i}.png")
        ImageGrab.grab().resize((384, 216)).save("Screenshots/60.png")

        self.display_image = tk.PhotoImage(file="Screenshots/0.png")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)

        self.after(10000, self.update_canvas)

    def update_canvas(self):
        Path("Screenshots/0.png").unlink()
        for i in range(60):
            Path(f"Screenshots/{i + 1}.png").rename(f"Screenshots/{i}.png")
        ImageGrab.grab().resize((384, 216)).save("Screenshots/60.png")

        self.display_image = tk.PhotoImage(file="Screenshots/0.png")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)

        self.after(10000, self.update_canvas)


if __name__ == "__main__":
    main()
