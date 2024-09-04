from tkinter import Tk, Label, Text, Scrollbar, VERTICAL, RIGHT, Y, Frame
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

            # Update the text display
            self.update_text_display(text_file_path)

    def update_text_display(self, text_file_path):
        if os.path.exists(text_file_path):
            with open(text_file_path, "r") as text_file:
                content = text_file.read()
                self.app.text_display.delete(1.0, "end")  # Clear existing text
                self.app.text_display.insert("end", content)  # Insert new text

class MyApp(Tk):
    def __init__(self):
        super().__init__()

        self.title("Image and Text Display")

        # Image display setup
        self.image_label = Label(self)
        self.image_label.pack()

        # Text display setup
        self.text_display_frame = Frame(self)
        self.text_display_frame.pack()

        self.text_display = Text(self.text_display_frame, wrap='word', height=10, width=50)
        self.text_display.pack(side="left", fill="both", expand=True)

        self.scrollbar = Scrollbar(self.text_display_frame, orient=VERTICAL, command=self.text_display.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.text_display.config(yscrollcommand=self.scrollbar.set)

if __name__ == "__main__":
    app = MyApp()
    image_handler = ImageHandler(app)
    # For testing purposes, you might load an image and call image_handler.show_image(image)
    app.mainloop()
