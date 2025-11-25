# Emonet Lab Website

See it live at: [https://emonetlab.github.io/emonetlab](https://emonetlab.github.io/emonetlab)

This repository contains the Jekyll-based website for the Emonet Lab. This guide will help you edit and maintain the website.

## Table of Contents

- [Posting News](#posting-news)
- [Editing the Navigation Menu](#editing-the-navigation-menu)
- [Adding Lab Members and Alumni](#adding-lab-members-and-alumni)
- [Adding Publications](#adding-publications)
- [Updating the Gallery](#updating-the-gallery)
- [Customizing Footer and Social Links](#customizing-footer-and-social-links)
- [Local Development and Testing](#local-development-and-testing)
- [GitHub Actions and Deployment](#github-actions-and-deployment)
- [Troubleshooting](#troubleshooting)
- [Additional Documentation](#additional-documentation)

---

## Posting News

Follow these steps to add a new news post:

1. **Create a new post file:**
   - Duplicate an existing `.md` file from `_posts/` as a starting template.
   - Rename the file using this format: `YYYY-MM-DD-title-separated-by-dashes.md`
   - Example: `2025-11-25-new-research-published.md`

2. **Add images (if needed):**
   - Create a folder in `assets/posts/` with the **exact same name** as your post file (without `.md`)
   - Example: If your post is `2025-11-25-new-research-published.md`, create folder `assets/posts/2025-11-25-new-research-published/`
   - Place all images for the post in this folder

3. **Edit the frontmatter:**
   Required fields at the top of the `.md` file:
   ```yaml
   ---
   title: "Your News Title Here"
   background: "assets/posts/2025-11-25-new-research-published/main-image.jpg"
   date: "2025-11-25"
   ---
   ```
   - `title`: The headline that appears on the news post
   - `background`: Path to the main image (used on the homepage and archive page)
   - `date`: Publication date in YYYY-MM-DD format

4. **Write your content:**
   - Add your news content below the frontmatter using Markdown syntax
   - Reference images using: `![Alt text]({{ site.baseurl }}/assets/posts/your-folder/image.jpg)`

5. **Push and deploy:**
   - Commit and push your changes to the `main` branch
   - Monitor the [GitHub Actions](https://github.com/emonetlab/emonetlab/actions) tab for build status
   - The site will automatically rebuild and deploy in 2-5 minutes
   - Force refresh your browser (Ctrl+F5 or Cmd+Shift+R) to see changes


---

## Editing the Navigation Menu

The top navigation menu is configured in `_data/navigation.yml`.

**Structure:**
```yaml
- text: Menu Item Name
  href: /page-url/
- text: Dropdown Menu
  menu:
    - text: Sub-item 1
      href: /sub-page-1/
    - text: Sub-item 2
      href: /sub-page-2/
```

**Example:** To add a new menu item, edit `_data/navigation.yml`:
```yaml
- text: Resources
  href: /resources/
```

For multi-level navigation or custom section navigation, see the [configuration documentation](assets/docs/configuration.md#navigation).

**Tips:**
- Menu items appear in the order they're listed
- Dropdown menus only support 2 levels
- Use `new_window: true` for external links


---

## Adding Lab Members and Alumni

Lab members and alumni data is stored in separate YAML files and automatically sorted alphabetically.

### Adding a New Lab Member

1. **Add member data to `_data/team.yml`:**

   ```yaml
   - name: Gustavo Madeira Santana
     role: Graduate Student
     program: >
       [Interdepartmental Neuroscience Program](https://medicine.yale.edu/inp/), [Program in Physics, Engineering and Biology](https://physics-engineering-biology.yale.edu)
     image: gustavo-santana.jpg
     description: >
       Gustavo completed his undergraduate in Computer Engineering at the Federal University of Rio Grande do Sul in Brazil, where he studied the ontogeny of vocal communication in mice. He is currently interested in understanding how flies explore spatiotemporal features of odor plumes for optimal navigation. In his free time, he spends too much money going to concerts, and enjoys playing guitar.
     googlescholar: L603SPwAAAAJ
     twitter: gumadeiras
     github: gumadeiras
     email: gustavo.santana@yale.edu
     website: https://gumadeiras.com
   ```

2. **Add profile photo:**
   - Place a square aspect ratio image in `assets/team/`
   - Name it to match the `image` field (e.g., `gustavo-santana.jpg`)
   - If no photo is available, use `empty.jpg`

3. **Available fields:**
   - **Required:** `name`, `role`, `image`
   - **Optional:** `program`, `description`, `email`, `website`, `googlescholar`, `twitter`, `github`, `orcid`, `researchgate`, `mastodon`, `when`

### Moving Members to Alumni

When a lab member leaves:

1. **Move their entry** from `_data/team.yml` to `_data/alumni.yml`
2. **Move their photo** from `assets/team/` to `assets/team/alumni/`
3. **Add a `when` field** indicating their time in the lab:
   ```yaml
   - name: Jane Smith
     when: "2020-2024"
     role: "Postdoctoral Fellow"
     image: jane-smith.jpg
   ```

**Important Notes:**
- No need to manually sort entries - the layouts handle alphabetical ordering automatically
- The `_layouts/team.html` and `_layouts/alumni.html` pages look for photos in their respective folders automatically
- Use Markdown in the `description` and `program` fields for formatting and links


---

## Adding Publications

Publications are organized by research area and automatically sorted by date.

### Publication Files

- **Neuroscience publications:** `_data/publications-neuro.yml`
- **Microbiology publications:** `_data/publications-micro.yml`
- **PDFs and supplementary files:** `assets/papers/`

The "Everything" publications page automatically combines all publication files.

### Adding a New Publication

1. **Add publication entry** to the appropriate YAML file:

   ```yaml
   - authors: "Kadakia N, Demir M, Michaelis BT, DeAngelis, BD, Reidenbach MA, Clark DA*, Emonet T*"
     title: "Odour motion sensing enhances complex plume navigation"
     journal: "Nature"
     edition: "611, pages 754–761 (2022)"
     doi: "10.1038/s41586-022-05423-4"
     date: "2022-11-09"
     html: "https://www.nature.com/articles/s41586-022-05423-4"
     pdf: "/assets/papers/2022/2022_KadakiaNature.pdf"
     suppinfo: "/assets/papers/2022/2022_KadakiaNatureSuppInfo.pdf"
     preprint: "https://www.biorxiv.org/content/10.1101/2021.09.29.462473v3"
     github: "https://github.com/emonetlab/opto-track"
     twitter: "https://twitter.com/EmonetLab/status/1590465867589988354"
     extra: |-
       \* co-corresponding authors.
       - [News and Views: Flies catch wind of where smells come from](https://doi.org/10.1038/d41586-022-03561-3), by Floris van Breugel and Bingni W. Brunton, Nature, [10.1038/d41586-022-03561-3](https://doi.org/10.1038/d41586-022-03561-3), Nov 9 2022
       - [Yale News article](https://news.yale.edu/2022/11/09/flies-smell-motion-odors-and-use-it-navigate-yale-study-finds) by Bill Hathaway
   ```

2. **Add PDF files** (if applicable):
   - Create a year-based folder in `assets/papers/` (e.g., `assets/papers/2022/`)
   - Upload your PDF with a descriptive name (e.g., `2022_KadakiaNature.pdf`)
   - Upload supplementary info if available (e.g., `2022_KadakiaNatureSuppInfo.pdf`)

3. **Publication fields:**
   - **Required:** `authors`, `title`, `journal`, `date`
   - **Optional:** `edition`, `doi`, `html`, `pdf`, `suppinfo`, `preprint`, `github`, `twitter`, `extra`
   - Use `extra` field for additional notes, awards, or media coverage (supports Markdown)

**Tips:**
- No need to manually sort - publications are automatically sorted by date (newest first)
- Use YAML multiline strings (`>` or `|-`) for long author lists or extra information
- The `date` field (YYYY-MM-DD format) controls the sort order


---

## Updating the Gallery

The website features a gallery page displaying photo albums from lab parties, outings, and conferences. Galleries are organized by year and use the [LightGallery JS library](https://www.lightgalleryjs.com/) for an elegant viewing experience.

### Gallery Structure

- **Gallery page:** `pages/gallery.md`
- **Layout template:** `_layouts/layout-with-gallery.html`
- **Album component:** `_includes/album.html`
- **Image directories:** `assets/images/gallery/<album_year>/`
- **Caption files:** `_data/galleries/<album_year>_details.yml`

### Adding a New Gallery (New Year)

Follow these steps to add a gallery for a new year:

1. **Create the image folder:**
   ```bash
   mkdir -p assets/images/gallery/2024-2025
   ```

2. **Add your images:**
   - Place all photos for the year in the folder you just created
   - Supported formats: `.jpg`, `.jpeg`, `.png`
   - Images will be displayed as clickable thumbnails in the gallery

3. **Create a captions file (optional but recommended):**
   
   Create a new file: `_data/galleries/2024-2025_details.yml`
   
   ```yaml
   - filename: "raclette-day.jpg"
     caption: "Raclette day"
   - filename: "birthday-boy-part-1.jpg"
     caption: "Birthday boy part 1"
   - filename: "group-photo.jpg"
     caption: "Lab retreat 2024"
   ```
   
   **Notes:**
   - The `filename` must exactly match the image filename in your gallery folder
   - Captions are optional - leave `caption: ""` for images without captions
   - Captions appear in the lightbox view when clicking on images

4. **Update the gallery page:**
   
   Edit `pages/gallery.md` and add your new year to the `album_names` list:
   
   ```liquid
   {% assign album_names = "2024-2025,2023-2024,2022-2023,2021-2022" | split: "," %}
   ```
   
   **Important:** Albums should be listed in reverse chronological order (newest first)

5. **Commit and push:**
   ```bash
   git add assets/images/gallery/2024-2025/
   git add _data/galleries/2024-2025_details.yml
   git add pages/gallery.md
   git commit -m "Add 2024-2025 gallery"
   git push
   ```

### Adding Photos to an Existing Gallery

To add more photos to an existing year:

1. **Add new images** to the appropriate folder (e.g., `assets/images/gallery/2023-2024/`)

2. **Update the captions file** at `_data/galleries/2023-2024_details.yml`:
   ```yaml
   - filename: "new-photo.jpg"
     caption: "New lab event"
   ```

3. **Commit and push** your changes

### Gallery Features

- **Responsive thumbnails:** Images automatically display as thumbnails on the page
- **Lightbox viewer:** Click any image to open the full-size gallery viewer
- **Navigation:** Use arrows or keyboard to navigate between photos
- **Zoom:** Click on images in the lightbox to zoom in/out
- **Captions:** Captions display below images in the lightbox view
- **Table of contents:** Jump to specific years using the links at the top

### Advanced: Automated Gallery Download

For bulk importing galleries from external sources, you can use the automation script:

**Script location:** `old_website/emonet_galleries_download.py`

This Python script can:
- Scrape images from specified gallery URLs
- Automatically download and organize images into year folders
- Generate caption YAML files based on image metadata

**To use:**
1. Edit the script to configure gallery URLs and output directory
2. Run: `python old_website/emonet_galleries_download.py`
3. Review generated files and move them to the appropriate directories
4. Update `pages/gallery.md` with the new album names

See the script comments for detailed usage instructions.

### Troubleshooting Gallery Issues

#### Gallery Not Displaying

**Solutions:**
- ✅ Verify LightGallery dependencies are installed: `npm install`
- ✅ Check that `layout-with-gallery` is specified in `pages/gallery.md` frontmatter
- ✅ Ensure image paths follow the pattern: `assets/images/gallery/<year>/`

#### Images Not Appearing in Gallery

**Solutions:**
- ✅ Check folder structure: images must be in `assets/images/gallery/<album_year>/`
- ✅ Verify album name in `pages/gallery.md` matches your folder name exactly
- ✅ Ensure images are committed and pushed to the repository
- ✅ Check file extensions are lowercase (`.jpg`, not `.JPG`)

#### Captions Not Showing

**Solutions:**
- ✅ Verify caption file exists: `_data/galleries/<album_year>_details.yml`
- ✅ Check that `filename` in YAML exactly matches image filename
- ✅ Ensure YAML syntax is valid (proper indentation, quotes around strings)
- ✅ Captions only appear in the lightbox view, not on thumbnails

---

## Customizing Footer and Social Links

### Social Media Links

Social profile icons appear in the footer. Configure them in `_config.yml`:

```yaml
social:
  email: thierry.emonet@yale.edu
  twitter: emonetlab
  github: emonetlab
  # mastodon: https://mastodon.social/@username
  # facebook: https://www.facebook.com/groups/group_id/
```

**Supported platforms:** email, Twitter, GitHub, Mastodon, Facebook

### Footer Columns

Customize footer content in `_data/footer.yml`:

```yaml
columns:
  - description: |
      Optional text or Markdown content
    links:
      - text: Team
        href: /team/
        new_window: false
      - text: Gallery
        href: /gallery/

  - description: |
      [Join the Lab! ❤](mailto:thierry.emonet@yale.edu)

# Copyright and license text
license: >
  Content available under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
```

### "Edit This Page" Link

Enable contributor editing in `_config.yml`:

```yaml
github_edit: true  # Uses 'main' branch by default
# Or specify a different branch:
# github_edit: develop
```

This adds an "Edit this page" link in the footer that opens the file in GitHub's editor.

For more footer customization options, see [configuration documentation](assets/docs/configuration.md#footer).

---

## Local Development and Testing

To test changes locally before pushing to GitHub:

### Prerequisites

1. **Install Ruby** (version 2.5 or higher)
   - macOS: Ruby comes pre-installed, but use [rbenv](https://github.com/rbenv/rbenv) or [RVM](https://rvm.io/) for better version management
   - Linux: `sudo apt-get install ruby-full` (Ubuntu/Debian)
   - Windows: Use [RubyInstaller](https://rubyinstaller.org/)

2. **Install Bundler:**
   ```bash
   gem install bundler
   ```

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/emonetlab/emonetlab.git
   cd emonetlab
   ```

2. **Install dependencies:**
   ```bash
   bundle install
   ```
   
   If you encounter ImageMagick-related errors:
   - macOS: `brew install imagemagick pkg-config`
   - Linux: `sudo apt-get install imagemagick libmagickwand-dev pkg-config`

3. **Install Node.js dependencies** (for asset management):
   ```bash
   npm install
   ```

### Running Locally

1. **Start the Jekyll server:**
   ```bash
   bundle exec jekyll serve
   ```

2. **View the site:**
   - Open your browser to `http://localhost:4000/`
   - The site will auto-reload when you make changes to files

3. **Stop the server:**
   - Press `Ctrl+C` in the terminal

### Common Local Development Commands

```bash
# Build the site without serving
bundle exec jekyll build

# Serve with drafts visible
bundle exec jekyll serve --drafts

# Serve with incremental builds (faster)
bundle exec jekyll serve --incremental

# Clear cache and rebuild
bundle exec jekyll clean
bundle exec jekyll build
```

### Updating Dependencies

```bash
# Update Ruby gems
bundle update

# Update Node.js packages
npm update
```

For detailed local setup instructions, see [installation documentation](assets/docs/installation.md).

---

## GitHub Actions and Deployment

The website uses GitHub Actions for automated building and deployment.

### How It Works

1. **Trigger:** Any push to the `main` branch triggers a build
2. **Build Process:**
   - Installs Ruby, Node.js, and ImageMagick dependencies
   - Runs `bundle exec jekyll build`
   - Creates a deployment artifact
3. **Deployment:** Automatically deploys to GitHub Pages
4. **Timeline:** The entire process takes 2-5 minutes

### Monitoring Builds

- View build status: [GitHub Actions tab](https://github.com/emonetlab/emonetlab/actions)
- Check for errors in the workflow logs
- Green checkmark ✓ = successful deployment
- Red X ✗ = build failed (see logs for details)

### Manual Deployment

You can manually trigger a deployment:
1. Go to [Actions tab](https://github.com/emonetlab/emonetlab/actions)
2. Select "Deploy Jekyll with GitHub Pages"
3. Click "Run workflow" → "Run workflow"

### Build Configuration

The workflow is defined in `.github/workflows/jekyll-gh-pages.yml`. It handles:
- Ruby and Jekyll setup
- Node.js and npm package installation
- ImageMagick for image processing
- GitHub Pages deployment

---

## Troubleshooting

### Common Issues and Solutions

#### Posts Not Appearing

**Problem:** New post doesn't show up on the website

**Solutions:**
- ✅ Verify the filename format: `YYYY-MM-DD-title.md`
- ✅ Check the `date` field in frontmatter matches the filename
- ✅ Ensure the file is in `_posts/` directory
- ✅ Check that `date` is not in the future
- ✅ Force refresh browser (Ctrl+F5 or Cmd+Shift+R)

#### Images Not Loading

**Problem:** Images appear broken on the site

**Solutions:**
- ✅ Verify image path: `assets/posts/YYYY-MM-DD-post-name/image.jpg`
- ✅ Use `{{ site.baseurl }}/assets/...` in image paths
- ✅ Check that folder name matches post filename exactly
- ✅ Ensure image files are committed and pushed
- ✅ Verify image file extensions are lowercase (.jpg, not .JPG)

#### YAML Frontmatter Errors

**Problem:** Build fails with YAML parsing errors

**Solutions:**
- ✅ Check for proper indentation (use spaces, not tabs)
- ✅ Wrap values with special characters in quotes: `title: "Title: With Colon"`
- ✅ Use `>` or `|-` for multi-line strings
- ✅ Validate YAML syntax: [yamllint.com](http://www.yamllint.com/)

Example correct frontmatter:
```yaml
---
title: "Research Update: New Findings"
background: "assets/posts/2025-11-25-research-update/image.jpg"
date: "2025-11-25"
---
```

#### GitHub Actions Build Failures

**Problem:** Deployment fails in GitHub Actions

**Solutions:**
1. Check the [Actions tab](https://github.com/emonetlab/emonetlab/actions) for error logs
2. Common causes:
   - ✅ Invalid YAML syntax in data files
   - ✅ Missing image files referenced in posts
   - ✅ Broken Markdown links
   - ✅ Ruby gem dependency issues
3. Look for the red X and click to see detailed logs
4. Fix the error and push again

#### Local Build Issues

**Problem:** `bundle exec jekyll serve` fails

**Solutions:**

**ImageMagick errors:**
```bash
# macOS
brew install imagemagick pkg-config
gem install rmagick

# Linux
sudo apt-get install imagemagick libmagickwand-dev pkg-config
gem install rmagick
```

**Ruby version issues:**
```bash
# Check Ruby version (need 2.5+)
ruby --version

# Update if needed
gem update --system
bundle update
```

**Port already in use:**
```bash
# Use a different port
bundle exec jekyll serve --port 4001
```

#### Changes Not Visible After Deployment

**Problem:** Pushed changes but website hasn't updated

**Solutions:**
- ✅ Wait 2-5 minutes for GitHub Actions to complete
- ✅ Check [Actions tab](https://github.com/emonetlab/emonetlab/actions) - build might still be running
- ✅ Force refresh browser: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
- ✅ Clear browser cache
- ✅ Try viewing in incognito/private mode

#### Team/Alumni Photos Not Displaying

**Problem:** Profile photos show as broken images

**Solutions:**
- ✅ Verify photo is in correct directory: `assets/team/` or `assets/team/alumni/`
- ✅ Check that `image` field in YAML matches actual filename
- ✅ Ensure image has square aspect ratio
- ✅ Use lowercase file extensions (.jpg, .png)
- ✅ Use `empty.jpg` as placeholder if no photo available

---

## Additional Documentation

For more detailed information about Jekyll and the Petridish theme:

- **[Installation Guide](assets/docs/installation.md)** - Setting up Jekyll and the theme
- **[Configuration Guide](assets/docs/configuration.md)** - Detailed configuration options including:
  - Custom navigation setups
  - Page organization strategies  
  - Home and team page customization
  - Colors, fonts, and theming
  - Logo and favicon setup
- **[Markdown Guide](assets/docs/markdown.md)** - Markdown syntax reference for content

### Helpful Resources

- [Jekyll Documentation](https://jekyllrb.com/docs/) - Official Jekyll docs
- [GitHub Pages Documentation](https://docs.github.com/en/pages) - GitHub Pages guide
- [Petridish Theme Repository](https://github.com/peterdesmet/petridish) - Theme documentation
- [Markdown Cheatsheet](https://www.markdownguide.org/cheat-sheet/) - Quick Markdown reference

### Need Help?

- Check the [GitHub Issues](https://github.com/emonetlab/emonetlab/issues) for known problems
- Review [GitHub Actions logs](https://github.com/emonetlab/emonetlab/actions) for build errors
- Contact the lab webmaster or lab manager for assistance

---

## Legacy Tools

The `old_website/emonet_to_jekyll.py` script was used to migrate content from the old Drupal website to Jekyll. This script is no longer needed for regular website updates but is kept for reference.

The `old_website/emonet_galleries_download.py` script can be used to automate downloading and organizing gallery images from external sources. See the [Updating the Gallery](#updating-the-gallery) section for details.