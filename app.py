import tkinter as tk

from PIL import Image, ImageDraw, ImageFont, ImageGrab, ImageTk


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

        self.screenshots = [Image.new("RGBA", (384, 216), "black") for _ in range(600)]
        for i, image in enumerate(self.screenshots):  # 0～599
            ImageDraw.Draw(image).text(
                (10, 0), f"{(600 - i) // 60} min {(600 - i) % 60} s",
                "white", ImageFont.truetype("arial.ttf", 36),
            )
            self.screenshots[i] = image
        self.screenshots.append(ImageGrab.grab().resize((384, 216)))  # 600

        self.display_image = ImageTk.PhotoImage(self.screenshots[0])
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)

        self.after(1000, self.update_canvas)

    def update_canvas(self):
        for i in range(600):
            self.screenshots[i] = self.screenshots[i + 1]
        self.screenshots[600] = ImageGrab.grab().resize((384, 216))

        self.display_image = ImageTk.PhotoImage(self.screenshots[0])
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)

        self.after(1000, self.update_canvas)


if __name__ == "__main__":
    main()
