# Emonet Lab website: agent instructions

## Scope and source of truth

- Read [README.md](README.md) for content editing and local setup.
- This is a Jekyll site with a customized Petridish theme. Use the local code and configuration to verify behavior; `assets/docs/` describes the original theme and can differ from this site.
- Write the README and public instructions in simple English. Use short steps and small examples. Explain any technical term a lab member needs.
- Check `git status` and the relevant diff before edits. Preserve existing local work. Keep changes within the request; do not update packages as a repair step.
- A local edit request does not authorize a commit, push, merge, or publication. Publishing requires authorization. Pushes to `main` and manual workflow runs publish the site.

## Where changes belong

- Content: `pages/`, `_posts/`, and `_data/`; use the README's file map.
- HTML: `_layouts/` and shared pieces in `_includes/`.
- Styles: `_sass/` and `assets/theme/css/`; browser code: `assets/theme/js/`.
- Site settings and image presets: `_config.yml`.
- Custom Ruby plugins: `_plugins/`.
- Edit source files. Do not edit `_site/`, generated image copies, caches, or installed packages in `node_modules/`. Do not run old import scripts for routine content updates.
- Keep agent guidance here. The files under `.github/` that provide agent instructions should point here. Keep `AGENTS.md` excluded in `_config.yml`.

## Content rules that are easy to miss

- Keep existing page addresses and old-post redirects working. New posts must not inherit another post's `original_url` or `redirect_from` values.
- Alumni appear only for the four exact `role` values in the README. Their page renders `now` and `past`, not `description` or `when`.
- Use approved career facts with dates where available. Leave `now` empty when no later position is supplied. Do not put “last known,” “not confirmed,” or research-status comments into individual profiles. Keep evidence gaps and open questions in private review notes, outside this public repository.
- Put each paper in one data list. Both research-area pages include the shared and physics lists; Everything combines all four lists. Check each affected page. The Everything and Microbiology layouts currently hardcode their GitHub links to `emonetlab/opto-track`; do not assume the `github` field works there.
- Use `relative_url` for local page and image links so a site path prefix works.

## Images and gallery

- Keep originals and point data fields at them. Team and alumni use photo file names; collaborators use paths starting with `assets/`.
- `_includes/profile-photo.html` selects profile previews from `site.data.profile_images` and links to originals. The `profile` preset leaves photos below 100,000 bytes unchanged. Larger files get WebP copies at quality 85, with a 300-pixel short edge and no enlargement. Orientation is applied before metadata is removed. The page displays 100-pixel circles.
- `_data/gallery.yml` controls published albums and their order. Album IDs must be unique `YYYY-YYYY` strings. Each album needs supported images and a cover that exists. `_plugins/gallery.rb` builds one complete page and `photos.json` per album; `_includes/album.html` and `assets/theme/js/gallery.js` display them.
- Gallery captions are plain text. Preserve escaping in HTML and literal text in JSON. Keep original-photo links usable if the viewer cannot load.
- Keep the gallery list to at most six covers, with no viewer scripts or styles. Load album metadata on first open. Keep a bounded set of slides and preload one neighboring photo on each side, without a full-album thumbnail strip.
- The gallery plugin copies nine required LightGallery files from installed packages. Run `npm ci` for missing files; do not publish all of `node_modules/`.
- Image output is reused based on source modification times. After changing presets, use a fresh build destination as shown in the README.

## Validation

- Use Ruby from `.ruby-version`, Bundler with `Gemfile.lock`, and npm with `package-lock.json`. The workflow uses Node 20. ImageMagick 7 is needed for `magick` in the tests. Setup commands are in the README.
- For site content, code, configuration, or build-output changes, run `bundle exec jekyll build` and inspect affected pages, images, and links.
- For gallery or image-processing changes, also run `bundle exec ruby tests/gallery_test.rb`. For viewer changes, check keyboard and touch navigation, Escape to close and return focus, zoom, downloads, and behavior when scripts cannot load.
- For documentation-only changes, verify paths, examples, and command claims, and run `git diff --check`. Build if the change affects which files are published.
- Report what was checked and any failures. The workflow builds and publishes; it does not run the gallery test or check every link.
