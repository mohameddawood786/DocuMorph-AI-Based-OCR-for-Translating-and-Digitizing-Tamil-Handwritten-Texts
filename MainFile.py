
import easyocr
from PIL import Image, ImageDraw

# Initialize the OCR reader
reader = easyocr.Reader(['ta', 'en'])

# Load the image
im = Image.open("2.jpg")

# Perform OCR and get bounding boxes along with text
bounds = reader.readtext('2.jpg')

# Extract the text from the bounding boxes and join them into a single sentence
detected_text = ' '.join([bound[1] for bound in bounds])

# Print the detected text
print("Detected Text: ", detected_text)

# Draw bounding boxes
def draw_boxes(image, bounds, color='blue', width=2):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        p0, p1, p2, p3 = bound[0]
        draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
    return image

# Draw boxes on the image (optional)
draw_boxes(im, bounds)

# Show the image (optional)
im.show()















