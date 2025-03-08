import cv2
import pytesseract
import numpy as np

def preprocess_image(image):
    """Enhances the image for OCR by converting to grayscale and thresholding."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return thresh

def extract_scoreboard(image_path):
    """Extracts filled and empty score slots from the scoreboard."""
    
    # Load the image
    image = cv2.imread(image_path)

    # Preprocess image for OCR
    processed_image = preprocess_image(image)

    # Use Tesseract to extract text
    custom_config = r'--oem 3 --psm 6'
    extracted_text = pytesseract.image_to_string(processed_image, config=custom_config)

    # Process extracted text into usable data
    scoreboard_status = {}
    valid_categories = [
        "ones", "twos", "threes", "fours", "fives", "sixes",
        "three_of_a_kind", "four_of_a_kind", "full_house",
        "small_straight", "large_straight", "yahtzee", "chance"
    ]

    lines = extracted_text.lower().split("\n")

    for line in lines:
        parts = line.split()
        if len(parts) >= 2:
            category = parts[0]  # Score category (e.g., "threes", "yahtzee")
            value = parts[1]  # Either a score or blank

            # Only add valid categories to the scoreboard data
            if category in valid_categories:
                if value.isdigit():
                    scoreboard_status[category] = int(value)  # Filled score
                else:
                    scoreboard_status[category] = "empty"  # Available slot

    print(f"📋 Processed Scoreboard Data (cleaned): {scoreboard_status}")
    return scoreboard_status

