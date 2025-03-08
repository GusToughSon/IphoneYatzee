import time
import subprocess
import pyautogui
import os
import sys
from focus_app import ensure_app_is_active
from window_capture import capture_window_screenshot, get_window_bounds
from object_detection import detect_objects
from dice_recognition import extract_dice_values
from score_analysis import extract_scoreboard
from ai_decision import determine_best_score
from region_selector import select_region  # ✅ Import the region selector

# ✅ Toggle this flag to enable/disable region selection
ENABLE_REGION_SELECTION = True  # Set to False when not needed

def get_running_apps():
    """Returns a list of currently open GUI applications."""
    script = 'tell application "System Events" to get name of (processes where background only is false)'
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    return [app.strip() for app in result.stdout.split(",")]

if __name__ == "__main__":
    running_apps = get_running_apps()

    if "iPhone Mirroring" in running_apps:
        app_name = "iPhone Mirroring"

        if ensure_app_is_active(app_name):
            time.sleep(2)  # ✅ Let the UI settle

            # ✅ Step 1: Allow Region Selection If Enabled
            if ENABLE_REGION_SELECTION:
                print("🔲 Press ENTER to select a region.")
                input()
                print("🟢 Launching Region Selector...")
                select_region()  # ✅ Call the selector
                print("✅ Region selection completed. Restarting script with new coordinates.")
                sys.exit(0)  # ✅ Exit so it restarts with new coordinates

            # ✅ Step 2: Capture Screenshot
            screenshot_path = capture_window_screenshot(app_name)

            if screenshot_path:
                print(f"✅ Screenshot successfully taken: {screenshot_path}")

                # ✅ Step 3: Detect Objects (First Time Setup)
                object_positions, labeled_image = detect_objects(screenshot_path)
                print(f"✅ Labeled Screenshot: {labeled_image}")
                print(f"📝 Detected Objects: {object_positions}")

                print("⚠️ No clicking performed yet. Rename images in `Objects/` and re-run the script.")
                sys.exit(0)  # ✅ Ensure script exits so user can rename images

            else:
                print("❌ Screenshot failed.")
                sys.exit(1)  # Exit if the screenshot fails

    else:
        print("❌ iPhone Mirroring is not running.")
        sys.exit(1)  # Exit if the app isn't running
