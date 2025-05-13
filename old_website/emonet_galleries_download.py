import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin, urlparse, unquote

# --- Configuration ---
# List of gallery URLs to scrape
GALLERY_URLS = [
    "https://emonet.biology.yale.edu/gallery/pictures-our-lab-2018-2019",
    "https://emonet.biology.yale.edu/gallery/lab-photos-2021-2022",
    "https://emonet.biology.yale.edu/gallery/lab-photos-2022-2023",
    "https://emonet.biology.yale.edu/gallery/lab-photos-2023-2024"
]

# Base directory to save downloaded images
BASE_SAVE_DIR = "/Users/gumadeiras/Downloads/downloaded_lab_galleries"

# User-Agent to mimic a browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
# --- End Configuration ---
def sanitize_filename(name):
    """Sanitizes a string to be used as a filename."""
    name = re.sub(r'[^\w\s-]', '', name).strip() # Remove non-alphanumeric (except whitespace, hyphens)
    name = re.sub(r'[-\s]+', '-', name) # Replace spaces/multiple hyphens with single hyphen
    return name

def download_image(image_url, save_path, session):
    """Downloads an image from a URL to a given path."""
    try:
        print(f"    Attempting to download: {image_url}")
        img_response = session.get(image_url, headers=HEADERS, stream=True, timeout=15)
        img_response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in img_response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"    Successfully downloaded to {save_path}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"    Failed to download {image_url}: {e}")
        return False

def download_gallery_images(gallery_url, base_save_path, session):
    print(f"Processing gallery: {gallery_url}")
    try:
        parsed_gallery_url = urlparse(gallery_url)
        gallery_name_slug = parsed_gallery_url.path.strip('/').split('/')[-1]
        if not gallery_name_slug:
            gallery_name_slug = parsed_gallery_url.netloc # Fallback

        gallery_save_dir = os.path.join(base_save_path, gallery_name_slug)
        os.makedirs(gallery_save_dir, exist_ok=True)
        print(f"  Saving images to: {gallery_save_dir}")

        response = session.get(gallery_url, headers=HEADERS, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        slides_ul = soup.find('ul', class_='slides')
        if not slides_ul:
            print(f"  Could not find '<ul class=\"slides\">' on {gallery_url}. No images will be downloaded from this URL.")
            return gallery_name_slug, []

        list_items = slides_ul.find_all('li', recursive=False) # Only direct children
        if not list_items:
            print(f"  Found '<ul class=\"slides\">' but no '<li>' items within it on {gallery_url}.")
            return gallery_name_slug, []
            
        print(f"  Found {len(list_items)} list items in the gallery.")
        downloaded_image_files_info = []

        for index, item in enumerate(list_items):
            img_tag = item.find('img', class_='adaptive-image')
            caption_div = item.find('div', class_='flex-caption')
            caption_text = ""
            if caption_div:
                strong_tag = caption_div.find('strong')
                if strong_tag and strong_tag.string:
                    caption_text = strong_tag.string.strip()

            if img_tag and img_tag.get('src'):
                adaptive_image_url = urljoin(gallery_url, img_tag['src']) # Ensure absolute URL
                
                # Derive a filename
                base_filename_from_url = os.path.basename(urlparse(adaptive_image_url).path)
                filename_base, filename_ext = os.path.splitext(base_filename_from_url)

                if caption_text:
                    suggested_filename = sanitize_filename(caption_text) + filename_ext
                else:
                    suggested_filename = sanitize_filename(filename_base) + filename_ext
                
                # If sanitize_filename resulted in empty name (e.g. caption was all special chars)
                if not suggested_filename.strip(filename_ext): 
                    suggested_filename = f"image_{index+1}{filename_ext}"


                image_save_path = os.path.join(gallery_save_dir, suggested_filename)
                
                if os.path.exists(image_save_path):
                    print(f"  Image {suggested_filename} already exists. Skipping.")
                    downloaded_image_files_info.append({"filename": suggested_filename, "caption": caption_text})
                    continue

                print(f"  Processing image: {caption_text or suggested_filename}")

                # Attempt to guess the original image URL
                # From: .../sites/default/files/styles/adaptive/adaptive-image/public/IMAGE.jpg?itok=...
                # To:   .../sites/default/files/public/IMAGE.jpg
                original_image_url_attempt = None
                try:
                    # More robustly remove /styles/.../public/ and itok
                    parsed_adaptive_url = urlparse(adaptive_image_url)
                    path_parts = parsed_adaptive_url.path.split('/')
                    if 'sites' in path_parts and 'default' in path_parts and 'files' in path_parts and 'public' in path_parts:
                        public_index = path_parts.index('public')
                        # Check if 'styles' is before 'public'
                        if 'styles' in path_parts[:public_index]:
                            # Reconstruct path up to 'files' then add 'public' and the actual filename
                            files_index = path_parts.index('files')
                            original_path = "/".join(path_parts[:files_index+1]) + "/public/" + path_parts[-1]
                            original_image_url_attempt = parsed_adaptive_url._replace(path=original_path, query="").geturl()
                except ValueError: # If 'public' or other parts are not found as expected
                    pass


                downloaded_successfully = False
                if original_image_url_attempt and original_image_url_attempt != adaptive_image_url:
                    print(f"    Attempting potential original URL: {original_image_url_attempt}")
                    if download_image(original_image_url_attempt, image_save_path, session):
                        downloaded_successfully = True
                    else:
                        print(f"    Original URL attempt failed. Falling back to adaptive URL.")
                
                if not downloaded_successfully:
                    if not download_image(adaptive_image_url, image_save_path, session):
                        print(f"    Failed to download adaptive image as well: {adaptive_image_url}")
                        continue # Skip adding to list if both failed

                downloaded_image_files_info.append({"filename": suggested_filename, "caption": caption_text})
            else:
                print(f"  Could not find 'img.adaptive-image' with src in list item {index+1}")
        
        print(f"Finished processing gallery: {gallery_url}\n")
        return gallery_name_slug, downloaded_image_files_info

    except requests.exceptions.RequestException as e:
        print(f"Error fetching gallery page {gallery_url}: {e}")
        return None, []
    except Exception as e:
        print(f"An unexpected error occurred while processing {gallery_url}: {e}")
        return None, []

def main():
    if not os.path.exists(BASE_SAVE_DIR):
        os.makedirs(BASE_SAVE_DIR)
        print(f"Created base directory: {BASE_SAVE_DIR}")

    jekyll_gallery_snippets = []
    
    # Use a session object for connection pooling
    with requests.Session() as session:
        for url in GALLERY_URLS:
            gallery_name_slug, image_files_info = download_gallery_images(url, BASE_SAVE_DIR, session)
            if gallery_name_slug and image_files_info:
                jekyll_path_suggestion = f"assets/img/{gallery_name_slug}"
                
                images_liquid_list = ""
                for img_info in image_files_info:
                    img_filename = img_info['filename']
                    img_caption = img_info['caption'].replace("'", "\\'") # Escape single quotes for Jekyll/Liquid
                    alt_text = img_caption if img_caption else img_filename.split('.')[0].replace('-', ' ').replace('_', ' ').capitalize()
                    
                    images_liquid_list += f"""
                          <div class="gallery-item">
                            <a href="{{{{ site.baseurl }}}}/{jekyll_path_suggestion}/{img_filename}" data-lightbox="{gallery_name_slug}" data-title="{alt_text}">
                              <img src="{{{{ site.baseurl }}}}/{jekyll_path_suggestion}/{img_filename}" alt="{alt_text}" style="max-width: 200px; height: auto; margin: 5px; border: 1px solid #ccc;">
                            </a>
                          </div>"""

                    snippet = f"""
                        ## Gallery: {gallery_name_slug.replace('-', ' ').title()}

                        To display this gallery in Jekyll:
                        1. Copy the downloaded images from the folder:
                           '{os.path.join(BASE_SAVE_DIR, gallery_name_slug)}'
                           to your Jekyll site's image directory, for example:
                           '{jekyll_path_suggestion}/'
                        2. You can then use Liquid to display them. Here's an example structure:

                        ```html
                        <!-- In your Jekyll markdown or HTML file -->
                        <h3>{gallery_name_slug.replace('-', ' ').title()}</h3>
                        <div class="image-gallery" style="display: flex; flex-wrap: wrap; gap: 10px;">
                          {{% assign gallery_image_path = "{jekyll_path_suggestion}" %}}
                          {{% assign image_files = "{", ".join(f"'{info['filename']}'" for info in image_files_info)}, "}}" %}} <!-- Creates a Liquid array of filenames -->

                          {{% for image_filename in image_files %}}
                            {{% assign image_data = site.data.galleries.{gallery_name_slug} | where: "filename", image_filename | first %}} <!-- Optional: For captions from _data -->
                            {{% assign caption = "" %}}
                            {{% for img_info in site.data.galleries.{gallery_name_slug}_details %}} {{% comment %}} Assuming you create a data file {gallery_name_slug}_details.yml {{% endcomment %}}
                                {{% if img_info.filename == image_filename %}}
                                    {{% assign caption = img_info.caption %}}
                                    {{% break %}}
                                {{% endif %}}
                            {{% endfor %}}
                            {{% assign alt_text = caption | default: image_filename | split: '.' | first | replace: '_', ' ' | replace: '-', ' ' | capitalize %}}

                          <div class="gallery-item">
                            <a href="{{{{ site.baseurl }}}}/{{{{ gallery_image_path }}}}/{{{{ image_filename }}}}" data-lightbox="{gallery_name_slug}" data-title="{{{{ alt_text }}}}">
                              <img src="{{{{ site.baseurl }}}}/{{{{ gallery_image_path }}}}/{{{{ image_filename }}}}" alt="{{{{ alt_text }}}}" style="max-width: 200px; height: auto; margin: 5px; border: 1px solid #ccc;">
                            </a>
                            {{% if caption != "" %}}
                              <p class="caption" style="text-align: center; font-size: 0.9em;">{{{{ caption }}}}</p>
                            {{% endif %}}
                          </div>
                          {{% endfor %}}
                        </div>

                        <!-- 
                          Alternative/Simpler Jekyll rendering (without separate data file for captions, less flexible):
                          This relies on the image_files_info captured by the Python script.
                          You might need to adapt how image_files_info is passed or stored for Jekyll.
                          The snippet below is a more direct Liquid representation of the downloaded files.
                        -->
                        <!--
                        <h3>{gallery_name_slug.replace('-', ' ').title()} (Simpler Render)</h3>
                        <div class="image-gallery" style="display: flex; flex-wrap: wrap; gap: 10px;">
                          {images_liquid_list}
                        </div>
                        -->

                        <!-- 
                          For the primary example above to work with captions dynamically, you would create a YAML file
                          in your Jekyll site's `_data/galleries/` directory, e.g., `_data/galleries/{gallery_name_slug}_details.yml`,
                          with content like this for each image:
                          
                          - filename: "raclette-day.jpg"
                            caption: "Raclette day"
                          - filename: "birthday-boy-part-1.jpg"
                            caption: "Birthday boy part 1"
                          ... etc. for all images in that gallery
                        -->

                        <!-- Make sure you have a lightbox JavaScript library included if you use data-lightbox -->
                    """
                    jekyll_gallery_snippets.append(snippet)
            # Create the _data file content suggestion
            data_file_path = os.path.join(BASE_SAVE_DIR, gallery_name_slug, f"{gallery_name_slug}_details.yml")
            with open(data_file_path, 'w', encoding='utf-8') as f_data:
                f_data.write(f"# Jekyll data file for gallery: {gallery_name_slug}\n")
                f_data.write(f"# Place this in your Jekyll site's _data/galleries/{gallery_name_slug}_details.yml\n\n")
                for img_info in image_files_info:
                    img_info_proc = img_info['caption'].replace('"', '""')
                    f_data.write(f"- filename: \"{img_info['filename']}\"\n")
                    f_data.write(f"  caption: \"{img_info_proc}\"\n") # Escape quotes for YAML
            print(f"  Suggested Jekyll data file created at: {data_file_path}")


    if jekyll_gallery_snippets:
        print("\n--- Jekyll Gallery Suggestions ---")
        for snippet in jekyll_gallery_snippets:
            print(snippet)

    print("\nAll galleries processed.")


if __name__ == "__main__":
    main()
