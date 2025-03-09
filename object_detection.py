import cv2
import numpy as np
import os
from PIL import Image, ImageChops

OBJECTS_FOLDER = "Objects"

def create_mask(image: np.ndarray, invert=False, method="canny", threshold=128):
    """
    Creates a binary mask from the input BGR `image`.

    - method="canny": uses Canny edge detection (with optional invert).
    - method="adapt": uses adaptive threshold + morphology (with optional invert).
    - method="simple": uses a simple global threshold (with optional invert).
    - threshold: used when method="simple".
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Possibly invert the grayscale
    if invert:
        gray = cv2.bitwise_not(gray)

    if method == "canny":
        # Let's do a wide range for edges to catch faint lines
        edges = cv2.Canny(gray, 30, 200)
        mask = np.where(edges > 0, 255, 0).astype(np.uint8)
        return mask

    elif method == "adapt":
        # Adaptive threshold + morphological ops
        th = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            blockSize=11,
            C=2
        )
        kernel = np.ones((3, 3), np.uint8)
        opened = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations=1)
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel, iterations=2)
        return closed

    elif method == "simple":
        # Simple global threshold
        ret, bin_mask = cv2.threshold(
            gray, threshold, 255, cv2.THRESH_BINARY_INV
        )
        return bin_mask

    # Default fallback: return an empty mask
    return np.zeros_like(gray)

def combine_masks(*masks: np.ndarray) -> np.ndarray:
    """
    Combine an arbitrary number of masks via bitwise OR,
    so if an object is visible in any pass, it’s included.
    """
    if not masks:
        return None
    combined = masks[0]
    for m in masks[1:]:
        combined = cv2.bitwise_or(combined, m)
    return combined

def is_duplicate(new_image: Image.Image, existing_images: list[Image.Image]) -> bool:
    """
    Checks if new_image is a duplicate of any in existing_images.
    Returns True if an exact match is found.
    """
    for existing_img in existing_images:
        try:
            diff = ImageChops.difference(existing_img, new_image)
            if not diff.getbbox():  # exact match => no bounding box in difference
                return True
        except Exception:
            pass
    return False

def detect_objects(image_path: str):
    """
    The “from scratch” approach:
      1) Load the image (BGR).
      2) Generate multiple masks (canny normal, canny invert, adapt normal, adapt invert, simple thresholds).
      3) Combine them all via OR => final_mask.
      4) Contour that mask.
      5) For each bounding box, skip if tiny, skip if duplicate, else save unique object.
      6) Return a dict { "object_n.png": (x, y, w, h) } plus the image path.

    If it still misses objects, consider adjusting thresholds or a color-based approach.
    """
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Could not read image: {image_path}")
        return {}, image_path

    # Generate multiple masks (“kitchen sink” approach)
    mask_canny_normal   = create_mask(image, invert=False, method="canny")
    mask_canny_invert   = create_mask(image, invert=True,  method="canny")
    mask_adapt_normal   = create_mask(image, invert=False, method="adapt")
    mask_adapt_invert   = create_mask(image, invert=True,  method="adapt")
    mask_simple64       = create_mask(image, invert=False, method="simple", threshold=64)
    mask_simple128      = create_mask(image, invert=False, method="simple", threshold=128)
    mask_simple192      = create_mask(image, invert=False, method="simple", threshold=192)
    mask_simple128_inv  = create_mask(image, invert=True,  method="simple", threshold=128)

    # Combine them
    final_mask = combine_masks(
        mask_canny_normal,
        mask_canny_invert,
        mask_adapt_normal,
        mask_adapt_invert,
        mask_simple64,
        mask_simple128,
        mask_simple192,
        mask_simple128_inv
    )

    # Find contours on final_mask
    contours, _ = cv2.findContours(final_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Ensure Objects/ folder
    if not os.path.exists(OBJECTS_FOLDER):
        os.makedirs(OBJECTS_FOLDER)

    # Load existing images to prevent duplicates
    existing_images: list[Image.Image] = []
    for fname in os.listdir(OBJECTS_FOLDER):
        path = os.path.join(OBJECTS_FOLDER, fname)
        try:
            existing_images.append(Image.open(path).convert("RGB"))
        except Exception:
            pass

    object_positions = {}
    unique_count = 0

    # Loop through each contour => bounding box
    for idx, contour in enumerate(contours, start=1):
        x, y, w, h = cv2.boundingRect(contour)

        # Filter out super tiny bounding boxes
        if w < 2 or h < 2:
            continue

        # Crop from the original color image
        cropped = image[y:y+h, x:x+w]
        pil_obj = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))

        # Skip duplicates
        if is_duplicate(pil_obj, existing_images):
            print(f"⚠️ Skipped duplicate object at ({x},{y})")
            continue

        # Save unique object
        obj_name = f"object_{unique_count + 1}.png"
        obj_path = os.path.join(OBJECTS_FOLDER, obj_name)
        cv2.imwrite(obj_path, cropped)
        existing_images.append(pil_obj)

        object_positions[obj_name] = (x, y, w, h)
        unique_count += 1
        print(f"📸 Saved unique object {unique_count}: {obj_path}")

    print(f"✅ Detected {unique_count} objects (mega-kitchen-sink).")
    return object_positions, image_path
