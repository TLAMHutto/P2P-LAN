# text_on_image_reader.py

import cv2
import pytesseract
from PIL import Image
import numpy as np

# Update this path to the location of your Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows
# For Linux: pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def detect_text_regions(image_path):
    # Load the image
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use OpenCV to detect text regions
    dsize = (800, 600)
    gray_image = cv2.resize(gray_image, dsize)
    
    # Thresholding to get binary image
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Detect text regions
    boxes = pytesseract.image_to_boxes(binary_image)

    # Draw boxes around detected text regions
    h, w, _ = image.shape
    for box in boxes.splitlines():
        b = box.split()
        x, y, w2, h2 = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(image, (x, h - y), (w2, h - h2), (0, 255, 0), 2)
    
    return image

def recognize_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def main(image_path):
    text_image = detect_text_regions(image_path)
    cv2.imshow('Text Detection', text_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    text = recognize_text_from_image(image_path)
    print("Detected Text:", text)

if __name__ == "__main__":
    image_path = 'path_to_your_image.jpg'  # Replace with the path to your image
    main(image_path)
