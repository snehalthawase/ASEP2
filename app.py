import streamlit as st
import pytesseract
import cv2
import numpy as np
from PIL import Image
from utils import format_text

st.markdown("---")  # horizontal line
st.title("📝 Smart Handwriting to Notes Converter")
st.markdown("Upload your handwritten notes and get clean, structured digital text!")
st.markdown("---")

uploaded_file = st.file_uploader("Upload your handwritten note", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    img_np = np.array(image)
    img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    extracted_text = pytesseract.image_to_string(thresh)

    st.subheader("Formatted Notes")
    formatted_text = format_text(extracted_text)

    st.text_area("Formatted Output", formatted_text, height=300)
    st.text_area("OCR Output", extracted_text, height=300)

    st.download_button(
        label="📥 Download Notes as .txt",
        data=formatted_text,
        file_name="notes.txt",
        mime="text/plain"
    )
