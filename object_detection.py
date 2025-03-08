import cv2
import os
import numpy as np

# Folder for storing detected objects
OBJECTS_FOLDER = "Objects"

# Ensure the Objects folder exists
if not os.path.exists(OBJECTS_FOLDER):
    os.makedirs(OBJECTS_FOLDER)
    print(f"📁 Created folder: {OBJECTS_FOLDER}")

def images_are_similar(image1, image2, threshold=0.85):
    """Checks if two images are similar using template matching."""
    if image1.shape != image2.shape:
        image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))  # Resize to match

    result = cv2.matchTemplate(image1, image2, cv2.TM_CCOEFF_NORMED)
    similarity = np.max(result)
    
    return similarity >= threshold

def detect_objects(image_path):
    """Detects objects in the screenshot and only saves unique ones."""
    
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)  # Keep original colors
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Regular edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    object_positions = {}
    named_objects = {}
    
    # Load existing objects for comparison
    existing_objects = {file: cv2.imread(os.path.join(OBJECTS_FOLDER, file), cv2.IMREAD_GRAYSCALE)
                        for file in os.listdir(OBJECTS_FOLDER) if file.endswith(".png")}

    for idx, contour in enumerate(contours, start=1):
        x, y, w, h = cv2.boundingRect(contour)

        # Filter out small objects
        if w > 30 and h > 30:
            cropped_object = image[y:y+h, x:x+w]
            detected_gray = cv2.cvtColor(cropped_object, cv2.COLOR_BGR2GRAY)

            # Compare with existing images before saving
            already_exists = False
            for existing_name, existing_img in existing_objects.items():
                if images_are_similar(detected_gray, existing_img):
                    print(f"✅ Detected object matches existing file: {existing_name}")
                    named_objects[existing_name] = (x, y, w, h)
                    already_exists = True
                    break  # Stop checking once a match is found

            if not already_exists:
                object_filename = os.path.join(OBJECTS_FOLDER, f"object_{idx}.png")
                cv2.imwrite(object_filename, cropped_object)
                print(f"📸 Saved new object {idx}: {object_filename}")
                named_objects[object_filename] = (x, y, w, h)

    # Save labeled screenshot
    labeled_image_path = os.path.join(OBJECTS_FOLDER, "labeled_screenshot.png")
    cv2.imwrite(labeled_image_path, image)
    print(f"📸 Labeled screenshot saved: {labeled_image_path}")

    return named_objects, labeled_image_path
