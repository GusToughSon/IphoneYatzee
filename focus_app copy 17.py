import subprocess

def bring_app_to_front(app_name):
    """Brings the specified application to the front."""
    script = f'tell application "{app_name}" to activate'
    subprocess.run(["osascript", "-e", script])

if __name__ == "__main__":
    app_name = "iPhone Mirroring"  # Change this if needed
    bring_app_to_front(app_name)
