import easyocr
import streamlit as st
from PIL import Image, ImageDraw
import io
import base64


st.markdown(f'<h1 style="color:#000000;text-align: center;font-size:36px;font-family:concat">{"AI-Based OCR Solution for Digitizing and Translating Handwritten Documents in Regional Language"}</h1>', unsafe_allow_html=True)


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('back1.jpg')



# Initialize the OCR reader
reader = easyocr.Reader(['ta', 'en'])

# Function to perform OCR and extract text with bounding boxes
def extract_text_and_boxes(image):
    # Perform OCR and get bounding boxes along with text
    bounds = reader.readtext(image)

    # Extract the text from the bounding boxes and join them into a single sentence
    detected_text = ' '.join([bound[1] for bound in bounds])

    # Draw bounding boxes on the image
    def draw_boxes(image, bounds, color='blue', width=2):
        draw = ImageDraw.Draw(image)
        for bound in bounds:
            p0, p1, p2, p3 = bound[0]
            draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
        return image

    # Draw boxes on the image
    image_with_boxes = image.copy()
    image_with_boxes = draw_boxes(image_with_boxes, bounds)
    
    return image_with_boxes, detected_text

# Streamlit app layout
# st.title("OCR Image Text Extraction")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open image
    image = Image.open(uploaded_file)
    
    # Display the original image
    st.image(image, caption='Original Image', use_column_width=True)
    
    # Extract text and draw boxes on the image
    image_with_boxes, detected_text = extract_text_and_boxes(image)
    
    # Display the image with bounding boxes
    st.image(image_with_boxes, caption='Image with Detected Text', use_column_width=True)
    
    # Display the extracted text
    st.subheader("Extracted Text:")
    st.write(detected_text)

        
    import re

 