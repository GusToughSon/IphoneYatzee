import time
import subprocess
import pyautogui
import os
from focus_app import ensure_app_is_active
from window_capture import capture_window_screenshot, get_window_bounds  # ✅ Fix: Import the function
from dice_recognition import extract_dice_values
from score_analysis import extract_scoreboard
from ai_decision import determine_best_score

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
            time.sleep(2)  # Let the UI settle

            # ✅ Fix: Now properly importing capture_window_screenshot
            screenshot_path = capture_window_screenshot(app_name)

            if screenshot_path:
                print(f"✅ Screenshot successfully taken: {screenshot_path}")

                # Step 1: Recognize Dice
                dice_values = extract_dice_values(screenshot_path)

                # Step 2: Analyze Scoreboard
                scoreboard_data = extract_scoreboard(screenshot_path)

                # Step 3: AI Chooses Best Score
                best_category = determine_best_score(dice_values, scoreboard_data)

                # Step 4: Click the Best Score
                if best_category:
                    print(f"🤖 Selecting {best_category}...")
                    # Call function to click the category (you may need a function like `click_score_category(best_category)`)
                    
            else:
                print("❌ Screenshot failed.")

    else:
        print("❌ iPhone Mirroring is not running.")
