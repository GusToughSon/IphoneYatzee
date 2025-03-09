import time
import sys
import pyautogui
import os

from focus_app import ensure_app_is_active
from window_capture import get_window_bounds, capture_window_screenshot
from object_detection import detect_objects

def main():
    app_name = "iPhone Mirroring"

    # Ensure app is active
    if not ensure_app_is_active(app_name):
        print(f"❌ {app_name} is not running or not active.")
        sys.exit(1)

    time.sleep(2)  # Let it settle

    # Get window bounds
    wb = get_window_bounds(app_name)
    if not wb:
        print("❌ Could not get window bounds.")
        sys.exit(1)

    (wx, wy, ww, wh) = wb
    print(f"🖥️ iPhone Mirroring Window: X={wx}, Y={wy}, W={ww}, H={wh}")

    # Take a screenshot
    shot_path = capture_window_screenshot(app_name)
    if not shot_path:
        print("❌ Screenshot failed.")
        sys.exit(1)

    # Run detection
    obj_positions, _ = detect_objects(shot_path)
    print(f"📝 Final Objects: {obj_positions}")

    print("✅ Done!")

if __name__ == "__main__":
    main()
