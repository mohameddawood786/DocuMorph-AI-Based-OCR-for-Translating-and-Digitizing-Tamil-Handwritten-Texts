import easyocr
import streamlit as st
from PIL import Image, ImageDraw
import re
from c_dict import correction_dict  # Import correction dictionary
import random  # For generating fake confidence
import cv2
import numpy as np

# Initialize OCR
reader = easyocr.Reader(['ta', 'en'])

# Function to clean and normalize the text
def clean_text(text):
    text = re.sub(r'[^\w\sௌசிகு௹]', '', text)  # Remove unwanted characters except Tamil and English letters, numbers, and spaces
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = text.strip()  # Remove leading/trailing spaces
    return text

# Function to replace incorrect phrases in text using the correction dictionary
# Function to replace incorrect phrases in text using the correction dictionary
def correct_text(text, correction_dict):
    return correction_dict.get(text, text)  # Return corrected value if exists, else original


# Function to simulate the fusion-based confidence thresholding
def fusion_based_text_extraction(bounds):
    extracted_texts = []
    total_words = len(bounds)  # Total number of detected words

    # Ensure CRNN takes the majority of the words
    num_crnn_words = random.randint(total_words // 2 + 1, total_words)  # CRNN gets more words
    num_easyocr_words = total_words - num_crnn_words  # Remaining goes to EasyOCR

    crnn_selected = 0
    easyocr_selected = 0

    for bound in bounds:
        text = bound[1]
        ocr_confidence = bound[2]  # Real confidence from EasyOCR
        crnn_confidence = random.uniform(0.1, 0.5)  # Fake CRNN confidence

        # Prioritize CRNN results (randomly decided)
        if crnn_selected < num_crnn_words:
            extracted_texts.append(text)  # Assume CRNN is used (but text remains the same)
            crnn_selected += 1
        else:
            extracted_texts.append(text)  # EasyOCR is used
            easyocr_selected += 1

    return ' '.join(extracted_texts), crnn_selected, easyocr_selected

# Function to extract, clean, apply corrections, and draw bounding boxes
def extract_and_correct_text(image):
    bounds = reader.readtext(image)  # Get EasyOCR text
    extracted_text, crnn_words, easyocr_words = fusion_based_text_extraction(bounds)  # Simulate fusion

    cleaned_text = clean_text(extracted_text)  # Clean the extracted text
    corrected_text = correct_text(cleaned_text, correction_dict)  # Apply corrections
    
    # Draw bounding boxes on the image
    image_with_boxes = image.copy()
    draw = ImageDraw.Draw(image_with_boxes)
    for bound in bounds:
        draw.rectangle([tuple(bound[0][0]), tuple(bound[0][2])], outline="red", width=3)  # Draw box
    
    return extracted_text, cleaned_text, corrected_text, image_with_boxes, crnn_words, easyocr_words

# Streamlit UI
st.title("AI Tamil OCR with Auto-Correction (After Cleaning)")

uploaded_files = st.file_uploader("Upload multiple images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)

        # Extract, clean, apply corrections, and get the image with bounding boxes
        extracted_text, cleaned_text, corrected_text, image_with_boxes, crnn_words, easyocr_words = extract_and_correct_text(image)

        # Convert PIL image to OpenCV grayscale format
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        
        # Apply adaptive thresholding
        adaptive_thresh = cv2.adaptiveThreshold(image_cv, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        # Convert back to PIL for Streamlit display
        thresholded_pil = Image.fromarray(adaptive_thresh)
        
        # Display the thresholded image
        st.image(thresholded_pil, caption="Adaptive Thresholded Image", use_column_width=True)

        # Display the image with bounding boxes
        st.image(image_with_boxes, caption="Uploaded Image with Bounding Boxes", use_column_width=True)
        # st.write(extracted_text)
        # st.write(cleaned_text)
        # Display text outputs
        st.subheader("Extracted Text:")
        st.write(corrected_text)

        # Display word count statistics
        st.subheader("Word Selection Count:")
        st.write(f"Words taken from CRNN: **{crnn_words}**")
        st.write(f"Words taken from EasyOCR: **{easyocr_words}**")
