import cv2
import pytesseract
import numpy as np
# Set the correct Tesseract path for macOS
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

def preprocess_image(image):
    """Enhances the image for OCR by converting to grayscale and thresholding."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return thresh

def extract_dice_values(image_path):
    """Detects and extracts the dice values from the roll area and identifies empty slots."""
    
    # Load the image
    image = cv2.imread(image_path)

    # Preprocess image for OCR
    processed_image = preprocess_image(image)

    # Use Tesseract to extract text
    custom_config = r'--oem 3 --psm 6 digits'
    detected_text = pytesseract.image_to_string(processed_image, config=custom_config)

    # Extract dice values (only digits)
    dice_values = [int(char) for char in detected_text if char.isdigit()]

    # Convert "empty" to 0
    while len(dice_values) < 5:
        dice_values.append(0)

    print(f"🎲 Detected Dice Values (cleaned): {dice_values}")
    return dice_values

