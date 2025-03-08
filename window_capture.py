import subprocess
import time
import cv2
import os

def get_window_bounds(app_name):
    """Gets the position and size of the iPhone Mirroring window."""

    script = f'''
    tell application "System Events"
        set frontApp to first application process whose frontmost is true
        tell frontApp
            set winBounds to position of window 1 & size of window 1
        end tell
    end tell
    return winBounds
    '''
    
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    window_data = result.stdout.strip().split(", ")

    try:
        x, y, width, height = map(int, window_data)
        print(f"📏 Window Bounds: X={x}, Y={y}, Width={width}, Height={height}")
        return x, y, width, height
    except ValueError:
        print("❌ Failed to retrieve window bounds.")
        return None

def capture_window_screenshot(app_name):
    """Captures a screenshot of the iPhone Mirroring window."""
    
    # Get window position using AppleScript
    script = f'''
    tell application "System Events"
        set frontApp to first application process whose frontmost is true
        tell frontApp
            set winBounds to position of window 1 & size of window 1
        end tell
    end tell
    return winBounds
    '''
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    window_data = result.stdout.strip().split(", ")

    try:
        x, y, width, height = map(int, window_data)
        print(f"📏 Window Bounds: X={x}, Y={y}, Width={width}, Height={height}")

        screenshot_path = "iPhone_Mirroring_window.png"

        # Take a screenshot of the window
        os.system(f"screencapture -R{x},{y},{width},{height} {screenshot_path}")
        print(f"📸 Screenshot saved: {screenshot_path}")

        return screenshot_path

    except ValueError:
        print("❌ Failed to retrieve window bounds.")
        return None
