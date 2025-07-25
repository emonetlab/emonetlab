import os
from urllib.parse import urlparse

def update_markdown_file(file_path):
    """
    Reads a markdown file, finds the 'original_url', and adds a 'redirect_from'
    field with the path from that URL.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Ensure the file has a YAML front matter
        if not content.startswith('---'):
            print(f"Skipping: No front matter found in {file_path}")
            return

        # Split the file into front matter and content
        parts = content.split('---', 2)
        if len(parts) < 3:
            print(f"Skipping: Malformed front matter in {file_path}")
            return

        front_matter = parts[1]
        main_content = parts[2]

        # Check if 'original_url' exists and 'redirect_from' does not
        if 'original_url:' not in front_matter:
            print(f"Skipping: 'original_url' not found in {file_path}")
            return

        if 'redirect_from:' in front_matter:
            print(f"Skipping: 'redirect_from' already exists in {file_path}")
            return

        # Find the original_url and create the redirect
        lines = front_matter.strip().split('\n')
        new_lines = []
        for line in lines:
            new_lines.append(line)
            if line.strip().startswith('original_url:'):
                # Extract the URL value
                url_value = line.split('original_url:', 1)[1].strip().strip('"\'')

                # Parse the URL to get the path
                path = urlparse(url_value).path

                # Add the redirect_from block
                if path:
                    redirect_block = f"redirect_from:\n  - {path}"
                    new_lines.append(redirect_block)

        # Rebuild the file content
        new_front_matter = '\n'.join(new_lines)
        new_content = f"---\n{new_front_matter}\n---{main_content}"

        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"Successfully processed: {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_all_files(folder_path):
    """
    Iterates through all files in a directory and its subdirectories
    and processes any markdown files found.
    """
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.md', '.markdown')):
                file_path = os.path.join(root, file)
                update_markdown_file(file_path)

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # IMPORTANT: Change this to the path of your folder
    target_folder = "/Users/gumadeiras/git/emonetlab/_posts"

    if not os.path.isdir(target_folder):
        print("Error: The specified folder does not exist.")
        print("Please update the 'target_folder' variable in the script.")
    else:
        print(f"Starting to process files in: {target_folder}")
        process_all_files(target_folder)
        print("Processing complete.")
