import os
from datetime import datetime
import random

def generate_unique_filename(path):
    base_path, ext = os.path.splitext(path)
    date_str = datetime.now().strftime("%d.%m.%Y")
    random_number = random.randint(10, 99)
    modified_path = f"{base_path}_modified_{random_number}_{date_str}{ext}"
    
    while os.path.exists(modified_path):
        random_number = random.randint(10, 99)  # Generate a new random number
        modified_path = f"{base_path}_modified_{random_number}_{date_str}{ext}"

    return modified_path
