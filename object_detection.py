import cv2
import numpy as np
import os
from PIL import Image, ImageChops

OBJECTS_FOLDER = "Objects"

def canny_mask(image: np.ndarray) -> np.ndarray:
    """
    Basic Canny edge detection.
    Converts BGR -> Grayscale, then Canny(30,200).
    Outputs a binary mask.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 30, 200)
    mask = (edges > 0).astype(np.uint8) * 255
    return mask

def adaptive_threshold_mask(image: np.ndarray) -> np.ndarray:
    """
    Adaptive threshold -> shapes in binary_inv.
    Minimal morphological open to reduce noise.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    th = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        blockSize=11,
        C=2
    )
    # Minimal morphological cleanup
    kernel = np.ones((3,3), np.uint8)
    opened = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations=1)
    return opened

def combine_masks(mask1: np.ndarray, mask2: np.ndarray) -> np.ndarray:
    """ OR the two masks -> final_mask. """
    return cv2.bitwise_or(mask1, mask2)

def is_duplicate(new_image: Image.Image, existing_images: list[Image.Image]) -> bool:
    """
    True if 'new_image' is a pixel-for-pixel match
    of an existing image in memory.
    """
    for existing_img in existing_images:
        try:
            diff = ImageChops.difference(existing_img, new_image)
            if not diff.getbbox():
                return True
        except:
            pass
    return False

def detect_objects(image_path: str):
    """
    1) Read BGR image
    2) Make canny_mask + adaptive_threshold_mask
    3) OR them -> final_mask
    4) Contours -> bounding boxes
    5) Skip duplicates -> store unique
    Return { 'object_#.png': (x,y,w,h) }
    """
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Could not read image: {image_path}")
        return {}, image_path

    # 1) Build the two masks
    mask_canny = canny_mask(image)
    mask_adapt = adaptive_threshold_mask(image)

    # 2) Combine
    final_mask = combine_masks(mask_canny, mask_adapt)

    # 3) Contours
    contours, _ = cv2.findContours(final_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"🔍 Found {len(contours)} contours in final mask.")

    # Ensure the folder
    if not os.path.exists(OBJECTS_FOLDER):
        os.makedirs(OBJECTS_FOLDER)

    # Load existing images to skip duplicates
    from PIL import Image
    existing_images = []
    for fname in os.listdir(OBJECTS_FOLDER):
        fpath = os.path.join(OBJECTS_FOLDER, fname)
        try:
            existing_images.append(Image.open(fpath).convert("RGB"))
        except:
            pass

    object_positions = {}
    unique_count = 0

    # 4) Loop bounding boxes -> skip duplicates -> save
    for idx, contour in enumerate(contours, start=1):
        x, y, w, h = cv2.boundingRect(contour)
        # Filter out too-tiny objects
        if w < 3 or h < 3:
            continue

        cropped = image[y:y+h, x:x+w]
        pil_obj = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))

        if is_duplicate(pil_obj, existing_images):
            print(f"⚠️ Skipped duplicate object at ({x},{y})")
            continue

        obj_name = f"object_{unique_count + 1}.png"
        obj_path = os.path.join(OBJECTS_FOLDER, obj_name)
        cv2.imwrite(obj_path, cropped)
        existing_images.append(pil_obj)

        object_positions[obj_name] = (x, y, w, h)
        unique_count += 1
        print(f"📸 Saved unique object {unique_count}: {obj_path}")

    print(f"✅ Detected {unique_count} objects (simple approach).")
    return object_positions, image_path
