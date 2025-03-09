import cv2
import pytesseract
import os

# If Tesseract is not in PATH, point to its install location:
# pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"


def detect_text_bounding_boxes(image_path: str):
    """
    Uses Tesseract's 'image_to_data' to get bounding boxes for all recognized text.
    Returns a list of (text, x, y, w, h, conf).
    """
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return []

    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Could not read: {image_path}")
        return []

    # Optionally preprocess image for better OCR:
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Invert or threshold if text is too faint...
    # For now, let's pass the raw image.

    # Tesseract can parse bounding boxes using 'image_to_data' with '--psm 6' for block-based
    data = pytesseract.image_to_data(image, config="--psm 6", output_type=pytesseract.Output.DICT)

    results = []
    for i in range(len(data["text"])):
        text = data["text"][i].strip()
        conf = int(data["conf"][i])
        x = data["left"][i]
        y = data["top"][i]
        w = data["width"][i]
        h = data["height"][i]

        if conf > 50 and text != "":  # confidence threshold, skip empty
            results.append((text, x, y, w, h, conf))

    return results
