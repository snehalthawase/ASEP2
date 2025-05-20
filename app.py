import streamlit as st
import pytesseract
import cv2
import numpy as np
from PIL import Image
from utils import preprocess_image, format_text, extract_text_line_by_line

st.markdown("---")  # horizontal line
st.title("📝 Smart Handwriting to Notes Converter")
st.markdown("Upload your handwritten notes and get clean, structured digital text!")
st.markdown("---")

uploaded_file = st.file_uploader("Upload your handwritten note", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    img_np = np.array(image)
    img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    psm_mode = st.selectbox(
    "🔍 Choose OCR Mode (PSM)",
    options=["6 - Block of Text", "7 - Single Line", "11 - Sparse Text"],
    index=0
    )

    psm_value = psm_mode.split(" - ")[0]  # Extract the number part


    # Preprocess the image
    processed_img = preprocess_image(img_cv)
    st.image(processed_img, caption="Processed Image (for OCR)", use_container_width=True, channels="GRAY")

    # Perform OCR using Tesseract
    extracted_text = pytesseract.image_to_string(processed_img, config=f"--psm {psm_value} --oem 1")
    
    
    # Debug OCR data with word-level confidence
    ocr_data = pytesseract.image_to_data(processed_img, config=f"--psm {psm_value} --oem 1", output_type=pytesseract.Output.DICT)
    
    with st.expander("🧪 Debug: Word-Level OCR Confidence"):
      for i in range(len(ocr_data['text'])):
        word = ocr_data['text'][i]
        conf = ocr_data['conf'][i]
        if word.strip() and conf != '-1':
            st.write(f"🔤 **{word}** — Confidence: {conf}")


    # Optional spell correction
    apply_spellcheck = st.checkbox("🛠 Apply Spell Correction (Experimental)", value=False)
 
    st.subheader("Formatted Notes")
    formatted_text = format_text(extracted_text, correct_spelling=apply_spellcheck)

    st.text_area("Formatted Output", formatted_text, height=300)
    st.text_area("Raw OCR Output", extracted_text, height=300)

    st.download_button(
        label="📥 Download Notes as .txt",
        data=formatted_text,
        file_name="notes.txt",
        mime="text/plain"
    )


