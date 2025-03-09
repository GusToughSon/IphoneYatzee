import time
import sys
import cv2
import pytesseract
import subprocess
from window_capture import get_window_bounds, capture_region_screenshot
from word_search import (
    get_clue_words,
    get_puzzle_grid,
    find_word_in_grid,
    find_all_words_in_grid
)

# If Tesseract is not in PATH, set it manually:
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

def ensure_app_is_active(app_name: str) -> bool:
    script = f'tell application "{app_name}" to activate'
    proc = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    return (proc.returncode == 0)

def main():
    if not ensure_app_is_active("iPhone Mirroring"):
        print("❌ iPhone Mirroring not running or not active.")
        sys.exit(1)
    time.sleep(2)

    bounds = get_window_bounds("iPhone Mirroring")
    if not bounds:
        print("❌ Could not get iPhone Mirroring window.")
        sys.exit(1)
    (win_x, win_y, win_w, win_h) = bounds

    capture_region_screenshot(1181, 200, 326, 75, "crossword_region.png")
    capture_region_screenshot(1181, 275, 316, 370, "crossword_search.png")

    clue_words = get_clue_words("crossword_region.png")
    print("🔎 Clue Words:", clue_words)

    grid = get_puzzle_grid("crossword_search.png")
    if not grid:
        print("❌ OCR failed to extract a puzzle grid.")
        sys.exit(1)
    print("\n🧩 Puzzle Grid for Search:")
for row in grid:
    print(" | ".join(row))  # Adds better spacing to avoid merging issues
    print("\n")

    found_words_info = []
    for w in clue_words:
        loc = find_word_in_grid(grid, w)
        if loc:
            found_words_info.append((w, loc))

    auto_detected_words = find_all_words_in_grid(grid)
    if auto_detected_words:
        print("\n🔎 Additional Words Found in Grid:")
        for word, loc in auto_detected_words:
            print(f"✅ Found '{word}' at {loc}")

    print("✅ Word search complete.")

if __name__ == "__main__":
    main()
