# merge_publications.py

import yaml
from thefuzz import fuzz

# --- Configuration ---
# The main file with the new/updated information
SOURCE_FILE = 'publications.yml'

# The destination files to be updated
TARGET_FILES = [
    'publications-micro.yml',
    'publications-neuro.yml',
    'publications-physics.yml'
]

# The similarity score required to consider two titles a match (out of 100).
# Adjust this value if you get too many false positives or miss obvious matches.
# 95 is a good starting point for very similar titles.
MATCH_THRESHOLD = 95

# --- Main Script ---

def load_yaml_file(filename):
    """Safely loads a YAML file and returns its content."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: File not found -> {filename}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file {filename}: {e}")
        return None

def save_yaml_file(filename, data):
    """Saves data to a YAML file, preserving order and formatting."""
    print(f"Saving updated data to {filename}...")
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # Use sort_keys=False to maintain original key order from the file
            yaml.dump(data, f, sort_keys=False, allow_unicode=True, default_flow_style=False, indent=2)
    except Exception as e:
        print(f"Error saving file {filename}: {e}")

def main():
    """
    Main function to merge publication data based on fuzzy title matching.
    """
    print("--- Starting Publication Merge Process ---")
    print("IMPORTANT: This script will overwrite target files. Make sure you have a backup.\n")

    # 1. Load the source publications file
    source_pubs = load_yaml_file(SOURCE_FILE)
    if not source_pubs:
        print(f"Could not load source file {SOURCE_FILE}. Aborting.")
        return

    # 2. Load all target publications files
    target_data = {}
    for filename in TARGET_FILES:
        data = load_yaml_file(filename)
        if data:
            target_data[filename] = data

    if not target_data:
        print("No target files could be loaded. Aborting.")
        return

    # Keep track of changes and unmatched entries
    update_count = 0
    unmatched_titles = []

    # 3. Iterate through each publication in the source file
    for source_entry in source_pubs:
        source_title = source_entry.get('title')
        if not source_title:
            continue

        best_match_info = {
            'score': 0,
            'entry': None,
            'file': None
        }

        # Find the best match across all target files
        for filename, publications in target_data.items():
            for target_entry in publications:
                target_title = target_entry.get('title')
                if not target_title:
                    continue
                
                # Calculate the similarity ratio
                score = fuzz.ratio(source_title, target_title)
                
                if score > best_match_info['score']:
                    best_match_info['score'] = score
                    best_match_info['entry'] = target_entry
                    best_match_info['file'] = filename

        # 4. Check if the best match is good enough and update the entry
        if best_match_info['score'] >= MATCH_THRESHOLD:
            print(f"\n✅ Match Found (Score: {best_match_info['score']})")
            print(f"   Source Title: '{source_title}'")
            print(f"   Target Title: '{best_match_info['entry']['title']}' in '{best_match_info['file']}'")
            
            # Update the matched entry with keys from the source entry
            # .update() will add new keys and overwrite existing ones
            best_match_info['entry'].update(source_entry)
            update_count += 1
        else:
            print(f"\n❌ No close match found for title: '{source_title}'")
            print(f"   (Best attempt was '{best_match_info['entry'].get('title', 'N/A')}' with score {best_match_info['score']})")
            unmatched_titles.append(source_title)

    # 5. Save the updated data back to the files
    print("\n--- Saving all changes ---")
    for filename, data in target_data.items():
        save_yaml_file(filename, data)

    # 6. Final report
    print("\n--- Merge Process Complete ---")
    print(f"Total entries updated: {update_count}")
    if unmatched_titles:
        print(f"\nCould not find a match for {len(unmatched_titles)} titles:")
        for title in unmatched_titles:
            print(f"  - {title}")
    print("----------------------------")


if __name__ == "__main__":
    main()
