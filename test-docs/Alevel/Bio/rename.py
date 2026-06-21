import os
import re
import random
import string

# Base directory for biology images
BASE_IMAGE_DIR = './storeimagealevelbio'

def generate_random_name(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def process_files(source_file):
    print(f"--- Processing file: {source_file} ---")
    
    # Extract the year from the filename (e.g., 'A level bio 66.md' -> '66')
    year_match = re.search(r'(\d+)', source_file)
    if not year_match:
        print(f"Could not find year in filename: {source_file}. Skipping.")
        return
    
    year = year_match.group(1)
    image_dir = os.path.join(BASE_IMAGE_DIR, year)
    
    if not os.path.exists(image_dir):
        print(f"Image directory not found: {image_dir}")
        return

    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find links
    matches = re.findall(r'!\[\[(.*?)(?:\|.*?)?\]\]', content)

    for match in matches:
        filename = match.rstrip('\\')
        old_path = os.path.join(image_dir, filename)

        if os.path.exists(old_path):
            new_name = f"{generate_random_name()}.png"
            new_path = os.path.join(image_dir, new_name)
            
            os.rename(old_path, new_path)
            
            # Update content
            pattern = f"!\[\[{re.escape(match)}(\|.*?)?\]\]"
            content = re.sub(pattern, f"![[{new_name}\\1]]", content)
            print(f"Renamed: {filename} -> {new_name}")
        else:
            if not filename.startswith("http"):
                print(f"Skipping (File not found): {filename}")

    with open(source_file, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    # Loop through .md files in the current directory
    for file in os.listdir(os.getcwd()):
        if file.endswith('.md'):
            process_files(file)
            
    print("\nProcess completed successfully.")