import cv2
import pytesseract
import os

# If Tesseract is not in PATH, set it manually:
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

DIRECTIONS = [
    (0, 1),   # right →
    (0, -1),  # left ←
    (1, 0),   # down ↓
    (-1, 0),  # up ↑
    (1, 1),   # down-right ↘
    (1, -1),  # down-left ↙
    (-1, 1),  # up-right ↗
    (-1, -1)  # up-left ↖
]

# -------------------------------------------------------
def get_clue_words(clue_image_path: str):
    """Extracts a list of words from the clue image."""
    if not os.path.exists(clue_image_path):
        print(f"❌ Missing clue image: {clue_image_path}")
        return []

    img = cv2.imread(clue_image_path)
    if img is None:
        print(f"❌ Could not open {clue_image_path}")
        return []

    text = pytesseract.image_to_string(img)
    words_raw = text.upper().split()
    words = []
    for w in words_raw:
        w_alpha = "".join(ch for ch in w if ch.isalpha())  # Keep only letters
        if len(w_alpha) >= 2:
            words.append(w_alpha)
    return words

# -------------------------------------------------------
def get_puzzle_grid(grid_image_path: str):
    """Extracts a structured 2D list of letters from the puzzle image."""
    if not os.path.exists(grid_image_path):
        print(f"❌ Missing puzzle image: {grid_image_path}")
        return []

    img = cv2.imread(grid_image_path)
    if img is None:
        print(f"❌ Could not open {grid_image_path}")
        return []

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding to improve contrast
    processed = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )

    text = pytesseract.image_to_string(processed, config="--psm 6")
    print("🔎 Raw OCR Output of Puzzle Grid:\n", repr(text))  # Debug print

    lines = text.split("\n")
    grid = []

    # Process each row, ensuring equal column count
    max_cols = 0
    for line in lines:
        line = line.strip().upper()
        if not line:
            continue

        # Normalize letters and remove non-alphabetic characters
        parts = [char for char in line if char.isalpha()]
        if parts:
            grid.append(parts)
            max_cols = max(max_cols, len(parts))

    # **Normalize row lengths** to prevent misalignment
    for row in grid:
        while len(row) < max_cols:
            row.append(" ")  # Fill with spaces to maintain alignment

    print("\n📝 Final Parsed Grid:")
    for row in grid:
        print(" ".join(row))

    return grid
# -------------------------------------------------------
def find_word_in_grid(grid, word):
    """Searches for a word in the grid, checking all 8 directions with full debug info."""
    rows = len(grid)
    if rows == 0:
        print("⚠️ The puzzle grid is empty! Cannot search words.")
        return None

    cols = len(grid[0])  # assume rectangular
    if cols == 0:
        print("⚠️ The puzzle grid has no columns!")
        return None

    word_len = len(word)

    # Debug: Print word being searched
    print(f"\n🔍 Searching for '{word}' in the grid...")

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == word[0]:  # potential match start

                # Debug Print: Show position where search starts
                print(f"   ➡️ Checking '{word}' starting at ({r},{c})")

                for (dr, dc) in DIRECTIONS:
                    print(f"   🔍 Checking direction (Δr={dr}, Δc={dc}) from ({r},{c})")
                    rr, cc = r, c
                    match = True
                    found_positions = [(rr, cc)]  # Track where letters are found

                    for i in range(1, word_len):
                        rr += dr
                        cc += dc

                        # If out of bounds, stop searching in this direction
                        if not (0 <= rr < rows and 0 <= cc < cols):
                            match = False
                            break

                        # If character doesn't match, stop searching
                        if grid[rr][cc].strip() != word[i]:  # Ignore extra spaces
                            match = False
                            break

                        found_positions.append((rr, cc))

                    if match:
                        print(f"✅ '{word}' FOUND from {found_positions[0]} to {found_positions[-1]}")
                        return found_positions  # Return a list of positions

                print(f"❌ '{word}' NOT found starting at ({r},{c}) in any direction.")

    print(f"🚫 '{word}' not found in puzzle at all.\n")
    return None

# -------------------------------------------------------
def find_all_words_in_grid(grid):
    """Detects all dictionary words in the grid, even if they are not in the clue list."""
    found_words = []
    
    # Simple built-in dictionary (replace this with a real word list if needed)
    COMMON_WORDS = {"HORN", "AXLE", "TIRE", "SEAT", "TRUNK", "WIPER", "CAR", "RELATED", "ITEMS", "PARK", "ROAD", "RACE"}

    for word in COMMON_WORDS:
        loc = find_word_in_grid(grid, word)
        if loc:
            found_words.append((word, loc))

    return found_words
