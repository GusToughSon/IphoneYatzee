# window_capture.py

import os
import subprocess

def get_window_bounds(app_name: str):
    """
    AppleScript to get position & size of frontmost window of the specified app.
    Returns (x,y,width,height) or None.
    """
    script = r'''
    tell application "System Events"
        set frontApp to first application process whose frontmost is true
        tell frontApp
            set winBounds to position of window 1 & size of window 1
        end tell
    end tell
    return winBounds
    '''
    proc = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if proc.returncode != 0:
        return None
    try:
        parts = proc.stdout.strip().split(", ")
        x, y, w, h = map(int, parts)
        return (x, y, w, h)
    except:
        return None

def capture_region_screenshot(x, y, width, height, output_path="region.png"):
    """
    Uses macOS screencapture command to grab a region: (x, y, width, height) in absolute screen coords.
    Returns the output path if successful, else None.
    """
    if os.path.exists(output_path):
        os.remove(output_path)

    cmd = ["screencapture", "-R", f"{x},{y},{width},{height}", output_path]
    proc = subprocess.run(cmd)
    if proc.returncode == 0 and os.path.exists(output_path):
        return output_path
    return None
