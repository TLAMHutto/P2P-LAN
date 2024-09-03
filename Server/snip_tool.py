from tkinter import Toplevel, Canvas
from PIL import ImageGrab

class SnipTool:
    def __init__(self, app):
        self.app = app
        self.snip_surface = None
        self.canvas = None
        self.rect = None

    def start_snip(self):
        self.app.root.withdraw()
        self.snip_surface = Toplevel(self.app.root)
        self.snip_surface.attributes("-fullscreen", True)
        self.snip_surface.attributes("-alpha", 0.3)
        self.snip_surface.configure(cursor="cross")

        self.canvas = Canvas(self.snip_surface, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.snip_surface.bind("<ButtonPress-1>", self.on_button_press)
        self.snip_surface.bind("<B1-Motion>", self.on_snip_drag)
        self.snip_surface.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_snip_drag(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x, end_y = (event.x, event.y)

        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)

        self.snip_surface.withdraw()
        self.app.root.deiconify()

        image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.app.image_handler.show_image(image)

        self.snip_surface.destroy()
