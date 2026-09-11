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
   - Place the original photo in `assets/team/`; a square crop is not required
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
- Alumni can use `now` for a confirmed position or dated career milestone and
  `past` for past positions and training. Both support Markdown. The alumni
  page shows `past` in an expandable section. Present the latest approved role
  or affiliation directly, with career dates where available. Do not add
  research-status wording such as "last known," "not confirmed," or comments
  about when a client project ended. Leave a role blank if none is supplied;
  keep evidence gaps and unresolved questions in the private review packet.
- Collaborator photos use a site-relative path in `_data/collaborators.yml`,
  such as `image: assets/team/collaborators/damon-clark.jpg`.
- Team, alumni, and collaborator photos are displayed as circular thumbnails
  at 100 × 100 CSS pixels, with a crop aligned to the top. Keep the original
  source image; do not stretch it into a square. During `bundle exec jekyll build`,
  photos below 100 KB are served unchanged. For larger photos,
  the `profile` preset in `_config.yml` generates WebP copies at quality 85,
  with a 300-pixel short edge (up to 3× display density). Smaller photos are
  never enlarged. Orientation is applied before metadata is removed.
  Generated files use `thumbnails/<original path>.webp` in `_site`; do not
  edit these files or change the YAML image fields to point to them.
  The layouts load portraits as needed when the visitor scrolls. Every portrait
  links to its original, full-resolution file in a new tab. The shared
  `_includes/profile-photo.html` uses the build's `site.data.profile_images`
  map to select a generated copy or the unchanged original.


---

## Adding Publications

Publications are organized by research area and automatically sorted by date.

### Publication Files

- **Neuroscience publications:** `_data/publications-neuro.yml`
- **Microbiology publications:** `_data/publications-micro.yml`
- **Publications for both areas:** `_data/publications-shared.yml`
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

The gallery at `/gallery/` lists published albums by year, with a small cover and a prominent photo count. Each album has its own URL and shows all its photos on one page. Previews below the first row use lazy loading. Opening a photo starts a viewer for the whole album: use the visible arrows, Left/Right keys, or a touch swipe to move between photos. Escape closes the viewer and returns focus to the photo you opened. The viewer has zoom and original-image download controls.

### Gallery Structure

- **Published album list and covers:** `_data/gallery.yml`, newest first
- **Index page:** `pages/gallery.md`
- **Page and JSON generation:** `_plugins/gallery.rb`
- **Layouts:** `_layouts/layout-with-gallery.html`, `_layouts/gallery-album.html`
- **Photo grid:** `_includes/album.html`
- **Styles and viewer integration:** `assets/theme/css/gallery.css`, `assets/theme/js/gallery.js`
- **Original photos:** `assets/gallery/<year>/`
- **Captions and descriptions:** `_data/galleries/<year>_details.yml`

The index displays at most six covers; older albums use text links. Each album uses one path, such as `/gallery/2022-2023/`, with no photo pagination. Ordinary links remain usable without JavaScript. Existing `/gallery/#2022-2023` links still reach that year on the index.

### Add an Album or Photos

1. Put lowercase `.jpg`, `.jpeg`, `.png`, `.gif`, or `.webp` images in `assets/gallery/<year>/`. Photos appear in filename order. Use names that preserve the intended order.
2. Add or update `_data/galleries/<year>_details.yml`. Filenames must match exactly. `caption` is the visible caption; `alt` provides an image description when the caption alone is not sufficient. Missing descriptions fall back to the caption or a neutral photo number, so add useful descriptions where possible.

   ```yaml
   - filename: "lab-dinner.jpg"
     caption: "Lab dinner"
     alt: "Lab members gathered around the dinner table."
   ```

3. To publish a new album, add its ID and cover filename to `_data/gallery.yml`, newest first:

   ```yaml
   - id: "2025-2026"
     cover: "lab-dinner.jpg"
   ```

   A folder alone does not add an album to the gallery. The cover must exist and the album must contain at least one supported image. The build reports invalid entries. Counts, pages, and viewer metadata update automatically when photos are added.
4. Run `npm ci` if dependencies are not installed, then `bundle exec jekyll build`. Run `bundle exec ruby tests/gallery_test.rb` for complete album pages, photo ordering, and metadata checks. Inspect the index, the full album grid, and viewer navigation before committing through the normal repository workflow.

### Image Loading and Build Output

The existing MiniMagick generator creates WebP display images through `gallery_preview` and `gallery_viewer` presets in `_config.yml`: maximum 640-pixel and 1600-pixel edges respectively, with orientation corrected and metadata removed. Originals remain unchanged. Generated files belong in the build output, not in source control. Use a clean build destination after changing an image preset so old derivatives are not reused.

Album metadata (`/gallery/<year>/photos.json`) is fetched only when a photo is first opened. One LightGallery instance handles the complete album, keeps a small bounded set of slide elements, and preloads one neighbor on each side. There is no all-photo thumbnail strip. The original file is used only for direct links or explicit downloads.

The gallery generator includes only the nine required files from the installed LightGallery package in the site output. This avoids Jekyll's automatic `node_modules` exclusion without publishing the whole dependency tree. Run `npm ci` if the build reports a missing viewer asset. The index does not load viewer scripts or styles.

### Troubleshooting

- **An album is absent:** Check `_data/gallery.yml`; the ID must match its image folder.
- **A caption is absent:** Match `filename` exactly, including prefixes and case.
- **The viewer does not open:** Check the browser console and confirm the generated LightGallery scripts and album JSON return successfully. Photo links still open originals if viewer scripts cannot load. A failed JSON request shows a direct-photo link and can be retried.
- **A preview is stale:** Rebuild into a fresh destination after changing presets.

For bulk imports, `old_website/emonet_galleries_download.py` can collect images and caption files. Review its output before adding an album to the published list.

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
- ✅ Run the Jekyll build to generate profile thumbnails; check the build log for image errors
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
