import glob
from PIL import Image, ImageDraw

dark_blue = (0x2D, 0x29, 0x7A)
purple = (0xB4, 0x3E, 0xB8)


class Visualize:
    scale: int

    def __init__(self, width, height, fg=purple, bg=dark_blue, scale=3):
        self.img = Image.new("RGB", (width, height))
        self.frame = 0
        self.cursor = (width / 2, height / 2)
        self.color = fg
        self.clear(bg)
        self.scale = scale
        self.box = [self.cursor[0], self.cursor[1], self.cursor[0], self.cursor[1]]

    def clear(self, color):
        self.img.paste(color, (0, 0, self.img.size[0], self.img.size[1]))

    def snap(self, area=None):
        if area is None:
            sub = self.img
        else:
            sub = self.img.crop(area)
        w, h = sub.size
        w, h = w * self.scale, h * self.scale
        scaled = sub.resize((w, h), resample=Image.NEAREST)
        scaled.save(f"frame{self.frame:04d}.png", "PNG")
        self.frame += 1

    def _update_box(self, x, y):
        if x < self.box[0]:
            self.box[0] = x
        if x > self.box[2]:
            self.box[2] = x
        if y < self.box[1]:
            self.box[1] = y
        if y > self.box[3]:
            self.box[3] = y

    def move_to(self, x, y):
        self.cursor = (x, y)

    def line_to(self, x, y, color=None):
        if color is None:
            color = self.color
        draw = ImageDraw.Draw(self.img)
        draw.line([self.cursor, (x, y)], color, 3)
        self.cursor = (x, y)
        del draw
        self._update_box(x, y)

    def save_gif(self, duration=None):
        if duration is None:
            duration = 1000 / 60
        frames = glob.glob("frame*.png")
        print(f"Saving {len(frames)} frames to gif...")
        frames = sorted(frames)
        frames = [Image.open(f) for f in frames]
        frames[0].save(
            "vis.gif",
            format="GIF",
            append_images=frames[1:],
            save_all=True,
            duration=duration,
        )
