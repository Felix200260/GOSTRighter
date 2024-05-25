import os
from datetime import datetime

def generate_unique_filename(path):
    base_path, ext = os.path.splitext(path)
    timestamp = datetime.now().strftime("%H-%M-%S_%d.%m.%Y")
    count = 1
    modified_path = f"{base_path}_modified_{timestamp}_{count}{ext}"

    while os.path.exists(modified_path):
        count += 1
        modified_path = f"{base_path}_modified_{timestamp}_{count}{ext}"

    return modified_path
