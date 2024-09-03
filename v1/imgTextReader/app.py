# app_gui.py

import tkinter as tk
from tkinter import filedialog, Text
from textReader import recognize_text_from_image, detect_text_regions

class TextOnImageReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text on Image Reader")

        self.label = tk.Label(root, text="Select an image file:")
        self.label.pack()

        self.select_button = tk.Button(root, text="Select File", command=self.select_file)
        self.select_button.pack()

        self.transcription_area = Text(root, wrap=tk.WORD, width=50, height=15)
        self.transcription_area.pack()

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff")])
        if file_path:
            self.process_file(file_path)

    def process_file(self, image_file):
        text_image = detect_text_regions(image_file)
        text = recognize_text_from_image(image_file)
        self.transcription_area.delete(1.0, tk.END)
        self.transcription_area.insert(tk.END, text)

if __name__ == "__main__":
    root = tk.Tk()
    app = TextOnImageReaderApp(root)
    root.mainloop()
