import re
import cv2
import numpy as np
import pytesseract
from PIL import Image

def preprocess_image(image):
    """
    Preprocess image: Convert to grayscale, blur to remove noise, and threshold.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def extract_text_from_image(image):
    """
    Extract text from image using pytesseract.
    """
    pil_img = Image.fromarray(image)
    return pytesseract.image_to_string(pil_img)

def clean_extracted_text(text):
    """
    Clean text by removing non-ASCII chars and extra newlines/tabs.
    """
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\t+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text.strip()

def save_text_to_file(text, filename="notes.txt"):
    """
    Save cleaned text to a .txt file.
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    return filename

def format_text(text):
    """
    Format raw OCR text to structured bullet points and headings.
    """
    lines = text.split("\n")
    formatted_lines = []

    for line in lines:
        line = line.strip()

        if line.isupper() and len(line) > 2:
            formatted_lines.append(f"\n### {line}\n")

        elif re.match(r"^[-•]", line):
            formatted_lines.append(f"- {line[1:].strip()}")

        elif line:
            formatted_lines.append(line)

    formatted_text = "\n".join(formatted_lines)
    formatted_text = re.sub(r'\n+', '\n', formatted_text)

    return formatted_text
