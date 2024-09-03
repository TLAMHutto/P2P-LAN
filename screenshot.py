import tkinter as tk
from PIL import ImageGrab
from PIL import ImageTk, Image

class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Draggable Screenshot Selector")
        self.root.geometry('800x600')
        
        # Capture the screenshot
        self.screenshot = ImageGrab.grab()
        self.screenshot_image = ImageTk.PhotoImage(self.screenshot)
        
        # Create a Canvas to display the screenshot
        self.canvas = tk.Canvas(root, width=self.screenshot.width, height=self.screenshot.height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor='nw', image=self.screenshot_image)

        # Bind mouse events for dragging
        self.canvas.bind('<ButtonPress-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)

        self.start_x = self.start_y = 0
        self.rect = None

    def on_mouse_down(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_mouse_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_mouse_up(self, event):
        end_x, end_y = event.x, event.y
        x1, y1 = min(self.start_x, end_x), min(self.start_y, end_y)
        x2, y2 = max(self.start_x, end_x), max(self.start_y, end_y)
        region = self.screenshot.crop((x1, y1, x2, y2))
        region.show()  # Display the cropped region in the default image viewer

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotApp(root)
    root.mainloop()
