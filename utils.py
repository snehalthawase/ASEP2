import re
import cv2
import numpy as np

def preprocess_image(image):
    """
    Preprocess the image using advanced upscaling, adaptive thresholding, and noise reduction.
    """
    # Upscale image (e.g., 1.5x size)
    scale_percent = 150  # Increase size by 150%
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    image = cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Denoising using GaussianBlur
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive thresholding (better contrast for handwriting)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )
    
    return thresh


def clean_extracted_text(text):
    """
    Clean the OCR text by removing non-ASCII characters and unnecessary whitespace.
    """
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
    text = re.sub(r'[\n\t]+', ' ', text)  # Replace newlines/tabs with spaces
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with one
    return text.strip()


def save_text_to_file(text, filename="notes.txt"):
    """
    Save cleaned text to a .txt file.
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    return filename


def format_text(text, correct_spelling=False):  # `correct_spelling` kept for API compatibility
    text = text.replace("—", "-").replace("–", "-").replace("_", " ")
    text = re.sub(r"[|~•*]", "", text)  # remove common OCR border artifacts
    text = re.sub(r"[-=]{2,}", "-", text)  # clean long dashes
    text = re.sub(r"\s{2,}", " ", text)  # normalize spaces
    text = re.sub(r"\n{2,}", "\n", text)  # clean multiple newlines

    # Manual OCR error corrections
    corrections = {
        "Improoved": "Improved",
        "Nowe": "Noise",
        "etrective": "Effective",
        "monsuntfonn handiwrie": "non-uniform handwriting",
        "handiwrie": "handwriting",
        "multple": "multiple",
        "te": "to",
        "etye": "style",
        "bettor": "better",
    }
    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)

    # Skip spell correction entirely

    lines = text.split("\n")
    formatted_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Apply formatting
        if line.isupper() and len(line) > 3:
            formatted_lines.append(f"\n### {line.title()}\n")
        elif re.match(r"^[\-+*]", line):
            formatted_lines.append(f"- {line[1:].strip()}")
        else:
            formatted_lines.append(line)

    return "\n".join(formatted_lines)
