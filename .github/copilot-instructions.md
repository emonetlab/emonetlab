# Copilot Instructions for Emonet Lab Website

This repository contains the Jekyll-based website for the Emonet Lab at Yale University.

## Repository Overview

- **Framework**: Jekyll 3.10 static site generator
- **Theme**: Custom theme based on Petridish
- **Deployment**: GitHub Pages via GitHub Actions
- **Live Site**: https://emonetlab.github.io/emonetlab

## Project Structure

- `_config.yml` - Main Jekyll configuration
- `_posts/` - News posts in Markdown format
- `_data/` - YAML data files for team, alumni, publications, navigation, and galleries
- `_layouts/` - HTML layout templates
- `_includes/` - Reusable HTML components
- `_sass/` - SCSS stylesheets
- `_plugins/` - Custom Jekyll plugins
- `assets/` - Images, PDFs, CSS, JS files
- `pages/` - Static pages (team, publications, gallery, etc.)

## Content Management

### Posts

- Location: `_posts/`
- Filename format: `YYYY-MM-DD-title-separated-by-dashes.md`
- Images: Store in `assets/posts/YYYY-MM-DD-post-name/` matching the post filename
- Required frontmatter: `title`, `background`, `date`

### Team Members

- Current members: `_data/team.yml`
- Alumni: `_data/alumni.yml`
- Photos: `assets/team/` (current) and `assets/team/alumni/` (former)
- Required fields: `name`, `role`, `image`

### Publications

- Neuroscience: `_data/publications-neuro.yml`
- Microbiology: `_data/publications-micro.yml`
- PDFs: `assets/papers/YYYY/`
- Required fields: `authors`, `title`, `journal`, `date`

### Gallery

- Images: `assets/images/gallery/<year>/`
- Captions: `_data/galleries/<year>_details.yml`
- Update album list in `pages/gallery.md`

## Development Commands

```bash
# Install Ruby dependencies
bundle install

# Install JavaScript dependencies
npm install

# Run local development server
bundle exec jekyll serve

# Build the site
bundle exec jekyll build

# Clean and rebuild
bundle exec jekyll clean && bundle exec jekyll build
```

## Testing Changes

1. Run local server: `bundle exec jekyll serve`
2. View at: http://localhost:4000/
3. Check for build errors in terminal output
4. Verify YAML syntax if frontmatter errors occur

## YAML Guidelines

- Use spaces, not tabs for indentation
- Wrap values with special characters in quotes
- Use `>` or `|-` for multi-line strings
- Validate syntax if build fails

## Build and Deployment

- Automatic deployment via GitHub Actions on push to `main` branch
- Workflow file: `.github/workflows/jekyll-gh-pages.yml`
- Build takes 2-5 minutes
- Monitor build status in the Actions tab

## Code Style

- Follow existing patterns in the codebase
- Use Kramdown Markdown syntax
- Use Liquid templating for dynamic content
- SCSS files should follow Bootstrap conventions
