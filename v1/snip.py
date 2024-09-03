import tkinter as tk
from PIL import ImageGrab, ImageTk
import pyautogui

class SnippingTool:
    def __init__(self, master):
        self.master = master
        self.master.title("Python Snipping Tool")
        self.master.geometry("400x300")
        self.start_x = None
        self.start_y = None
        self.current_image = None

        self.snip_button = tk.Button(self.master, text="New Snip", command=self.start_snip)
        self.snip_button.pack(pady=20)

        self.image_label = tk.Label(self.master)
        self.image_label.pack(pady=10)

    def start_snip(self):
        self.master.withdraw()
        self.snip_surface = tk.Toplevel(self.master)
        self.snip_surface.attributes("-fullscreen", True)
        self.snip_surface.attributes("-alpha", 0.3)
        self.snip_surface.configure(cursor="cross")

        self.canvas = tk.Canvas(self.snip_surface, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.snip_surface.bind("<ButtonPress-1>", self.on_button_press)
        self.snip_surface.bind("<B1-Motion>", self.on_snip_drag)
        self.snip_surface.bind("<ButtonRelease-1>", self.on_button_release)

        self.rect = None

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
        self.master.deiconify()

        image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.show_image(image)

        self.snip_surface.destroy()

    def show_image(self, image):
        self.current_image = image
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

if __name__ == "__main__":
    root = tk.Tk()
    app = SnippingTool(root)
    root.mainloop()