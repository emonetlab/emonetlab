import requests
from bs4 import BeautifulSoup
import yaml
import os
import re
from urllib.parse import urljoin, urlparse

def generate_filename_base(tr_element):
    """
    Generates a unique, short filename base from the publication's table row.
    Format: firstauthor_lastauthor_year
    """
    if not tr_element:
        return "unknown_publication"

    # Use a separator to handle <br> tags and get the author line
    # The authors are typically the first line of text in the cell.
    for br in tr_element.find_all("br"):
        br.replace_with("|||")
    
    full_text = tr_element.get_text(separator=" ", strip=True)
    text_lines = [line.strip() for line in tr_element.get_text().split('|||') if line.strip()]
    
    if not text_lines:
        return "unknown_publication"

    authors_line = text_lines[0]
    
    # Clean up author names by removing markers like *, #, etc.
    cleaned_authors_line = re.sub(r'[\*#ǂ]', '', authors_line).strip()
    
    # Split authors by comma, 'and', or ampersand
    authors = re.split(r',\s*|\s+&\s+|\s+and\s+', cleaned_authors_line)
    
    # Get the last name of the first and last author
    if not authors:
        return "unknown_publication"
        
    first_author_lastname = authors[0].strip().split(' ')[0]
    last_author_lastname = authors[-1].strip().split(' ')[0]

    # Find the year using a robust regex
    year_match = re.search(r'\b(20\d{2}|19\d{2})\b', full_text)
    year = year_match.group(1) if year_match else "no_year"
    
    base = f"{first_author_lastname.lower()}_{last_author_lastname.lower()}_{year}"
    # Sanitize in case of weird characters in names
    return re.sub(r'[^a-z0-9_]', '', base)


def get_download_info(link_text, url):
    """
    Determines the file suffix and extension based on the link text and URL.
    Returns a tuple (suffix, extension) or None if not a downloadable link.
    """
    link_text = link_text.lower().strip()
    
    suffix_map = {
        'pdf': '_paper',
        'supp info': '_suppinfo',
        'code': '_code'
    }

    suffix = None
    if link_text.startswith('movie'):
        suffix = '_' + link_text.replace(' ', '')
    elif link_text in suffix_map:
        suffix = suffix_map[link_text]
    else:
        # Don't download links like 'html', 'biorxiv', etc.
        return None

    try:
        path = urlparse(url).path
        ext = os.path.splitext(path)[1]
        
        # If the URL has no extension, assume .pdf for common doc types
        if not ext and ('pdf' in link_text or 'supp' in link_text):
            ext = '.pdf'
        # If we still don't have an extension, we can't save it reliably
        elif not ext:
             return None
        
        return (suffix, ext)
    except Exception:
        return None


def scrape_publications(url, output_dir='papers'):
    """
    Scrapes a webpage for publication info from a table, saves it to a YAML file,
    and downloads files with unique, short names.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not fetch the URL. {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    all_papers_data = []
    
    # Find the table body and then all rows within it
    table_body = soup.find('tbody')
    if not table_body:
        print("Error: Could not find the 'tbody' element. The page structure may have changed.")
        return
        
    for row in table_body.find_all('tr'):
        # The title is in the <em> tag
        title_em = row.find('em')
        if not title_em:
            continue # Skip rows without a title (e.g., header or malformed rows)
        
        title = title_em.get_text(strip=True)
        
        paper_data = {'title': title}
        
        # Generate the base filename (e.g., "moore_emonet_2024")
        filename_base = generate_filename_base(row)

        links = row.find_all('a')
        for link in links:
            link_text = link.get_text(strip=True)
            href = link.get('href')

            if not href or not link_text:
                continue
            
            full_url = urljoin(url, href)
            # Use link text as the key, sanitized for YAML
            key_name = link_text.lower().replace(' ', '_')
            
            download_info = get_download_info(link_text, full_url)

            if download_info and filename_base:
                suffix, extension = download_info
                new_filename = f"{filename_base}{suffix}{extension}"
                relative_path = os.path.join(output_dir, new_filename)
                
                print(f"Downloading: {title} ({link_text})")
                try:
                    file_response = requests.get(full_url, stream=True)
                    file_response.raise_for_status()
                    
                    with open(relative_path, 'wb') as f:
                        for chunk in file_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    paper_data[key_name] = relative_path
                    print(f"  -> Saved to {relative_path}")

                except requests.exceptions.RequestException as e:
                    print(f"  -> Error downloading file: {e}")
                    paper_data[key_name] = full_url # Fallback to URL on error
            else:
                # For non-downloadable links (e.g., html), use the full URL
                paper_data[key_name] = full_url
        
        all_papers_data.append(paper_data)

    # Write the collected data to a YAML file
    yml_file_path = 'publications.yml'
    with open(yml_file_path, 'w', encoding='utf-8') as yaml_file:
        yaml.dump(all_papers_data, yaml_file, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(f"\nScraping complete!")
    print(f"Publication data saved to '{yml_file_path}'.")
    print(f"Files downloaded to the '{output_dir}' directory.")


if __name__ == '__main__':
    # The URL now points to the new page structure you provided
    target_url = 'https://emonet.biology.yale.edu/publications'
    scrape_publications(target_url)
