import os
import re
import random
import string

# Configuration
IMAGE_DIR = './storeimagealevelphy'

def generate_random_name(length=10):
    """Generates a random string of letters and digits."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def process_files(source_file, image_dir):
    """Reads a markdown file, renames associated images, and updates links."""
    print(f"--- Processing file: {source_file} ---")
    
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex matches: ![[filename|optional_extra]]
    # Group 1 captures the filename, Group 2 (optional) captures the |extra part
    matches = re.findall(r'!\[\[(.*?)(?:\|.*?)?\]\]', content)

    for match in matches:
        # Clean the captured filename (remove trailing backslash if present)
        filename = match.rstrip('\\')
        old_path = os.path.join(image_dir, filename)

        if os.path.exists(old_path):
            new_name = f"{generate_random_name()}.png"
            new_path = os.path.join(image_dir, new_name)
            
            # 1. Rename the physical file
            os.rename(old_path, new_path)
            
            # 2. Update the reference in the content
            # We use re.escape(match) to ensure the search pattern is literal
            # The replacement uses \\1 to keep the |318 or similar extra data
            pattern = f"!\[\[{re.escape(match)}(\|.*?)?\]\]"
            content = re.sub(pattern, f"![[{new_name}\\1]]", content)
            
            print(f"Renamed: {filename} -> {new_name}")
        else:
            # This will skip if the file is already renamed or doesn't exist
            if not filename.startswith("http"):
                print(f"Skipping (File not found): {filename}")

    # Save the updated content
    with open(source_file, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    if not os.path.exists(IMAGE_DIR):
        print(f"Error: Directory '{IMAGE_DIR}' not found.")
    else:
        # Loop through all .md files in the current directory
        for file in os.listdir(os.getcwd()):
            if file.endswith('.md'):
                process_files(file, IMAGE_DIR)
        
        print("\nProcess completed successfully.")