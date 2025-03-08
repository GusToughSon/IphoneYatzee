import subprocess
import time

def bring_app_to_front(app_name):
    """Brings the specified application to the front."""
    script = f'tell application "{app_name}" to activate'
    subprocess.run(["osascript", "-e", script])

def ensure_app_is_active(app_name):
    """Brings the app to the front and verifies it's active."""
    bring_app_to_front(app_name)
    time.sleep(1)  # Give it a moment to actually come to the front

    script = '''
    tell application "System Events"
        set frontApp to name of first application process whose frontmost is true
    end tell
    return frontApp
    '''
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    active_app = result.stdout.strip()

    if active_app == app_name:
        print(f"✅ {app_name} is now active.")
        return True
    else:
        print(f"❌ Failed to bring {app_name} to the front. Current active app: {active_app}")
        return False
