from PIL import Image
import pytesseract

# Function to perform OCR
def ocr_from_image(image_path):
    # Open the image file
    img = Image.open(image_path)
    
    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(img)
    
    return text

# Replace 'your_image.png' with the path to the image file you want to process
image_path = r"C:\Users\tanma\Downloads\jk.jpg"
extracted_text = ocr_from_image(image_path)

# Output the extracted text
print(extracted_text)