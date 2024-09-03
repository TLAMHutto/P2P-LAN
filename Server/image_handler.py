from tkinter import messagebox
from PIL import ImageTk, Image
import pytesseract
import os

class ImageHandler:
    def __init__(self, app):
        self.app = app
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    def show_image(self, image):
        # Display the image in the GUI
        photo = ImageTk.PhotoImage(image)
        self.app.image_label.config(image=photo)
        self.app.image_label.image = photo

        # Define directories
        save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
        text_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imgTxt")

        # Save image
        if save_dir:
            filename = "snip_latest.png"
            file_path = os.path.join(save_dir, filename)

            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            image.save(file_path)
            messagebox.showinfo("Image Saved", f"Image saved as {filename} in {save_dir}")

            # Perform OCR on the saved image
            text = pytesseract.image_to_string(Image.open(file_path))

            # Save the extracted text
            if not os.path.exists(text_dir):
                os.makedirs(text_dir)

            text_filename = "snip_latest.txt"
            text_file_path = os.path.join(text_dir, text_filename)

            with open(text_file_path, "w") as text_file:
                text_file.write(text)

            messagebox.showinfo("Text Extracted", f"Text extracted and saved as {text_filename} in {text_dir}")
