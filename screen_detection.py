import os

# Folder where detected objects will be stored
OBJECTS_FOLDER = "Objects"

# Ensure the Objects folder exists
if not os.path.exists(OBJECTS_FOLDER):
    os.makedirs(OBJECTS_FOLDER)
    print(f"📁 Created folder: {OBJECTS_FOLDER}")
