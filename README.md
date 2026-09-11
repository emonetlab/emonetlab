# Emonet Lab website

This repository holds the [Emonet Lab website](https://emonet.biology.yale.edu/). Use this guide to update its text, people, papers, and photos.

## Find the file to edit

| To change | Edit |
| --- | --- |
| Home page | `pages/home.md` |
| Contact details and other page text | The matching file in `pages/` |
| News | A file in `_posts/` |
| Current members | `_data/team.yml` |
| Alumni | `_data/alumni.yml` |
| Collaborators | `_data/collaborators.yml` |
| Papers | The publication lists described below |
| Photo albums | `_data/gallery.yml` and `_data/galleries/` |
| Top menu | `_data/navigation.yml` |
| Text and links at the bottom of each page | `_data/footer.yml` |
| Lab social links, logo, and site settings | `_config.yml` |

Files ending in `.md` contain text with simple formatting, called Markdown. Files ending in `.yml` contain lists or settings. Keep their spacing, use spaces instead of tabs, and put text that contains a colon inside quotes.

For a small update, edit the file on GitHub or in your local copy. Copy a nearby entry when adding content, then replace its details. Check the result before publishing. The steps below show which details matter.

## Add news

1. Create a file in `_posts/` named `YYYY-MM-DD-short-title.md`, such as `2026-09-11-lab-news.md`.
2. If the post has photos, put them in a matching folder: `assets/posts/2026-09-11-lab-news/`.
3. Start the file with the settings below. Replace the sample text and photo name. Omit `background` if there is no main photo.

   ```yaml
   ---
   title: "Lab news"
   date: "2026-09-11"
   background: "assets/posts/2026-09-11-lab-news/lab.jpg"
   ---
   ```

4. Write the news below the closing `---`. To include a photo in the text, use:

   ```markdown
   ![Lab members at dinner]({{ '/assets/posts/2026-09-11-lab-news/lab.jpg' | relative_url }})
   ```

Keep the date in the file name and the `date` setting the same. Future-dated posts stay hidden until a build runs on or after that date. There is no daily scheduled build.

If you copy an old post, remove its `original_url` and `redirect_from` settings. Those settings preserve links from the old website; a new post must not reuse them.

## Update people

### Current members and collaborators

Add an entry to `_data/team.yml`. Use Gustavo Santana's entry as a starting point and replace the details:

```yaml
- name: Gustavo Madeira Santana
  role: Graduate Student
  image: gustavo-santana.jpg
  description: >
    Gustavo studies how flies use changes in odor to find their way.
  email: gustavo.santana@yale.edu
  website: https://gumadeiras.com
```

Put the photo in `assets/team/`, with a file name that matches `image`. Use `image: empty.jpg` if no photo is available. You can add `program` and `website` fields. Copy other profile links from an existing entry when needed. The page lists people alphabetically by their full `name`, usually their first name.

Collaborators use the same fields in `_data/collaborators.yml`, but their `image` field includes the full path from the repository root. For Gustavo's photo, that path is `assets/team/gustavo-santana.jpg`.

### Move a member to alumni

1. Move the person's entry from `_data/team.yml` to `_data/alumni.yml`.
2. Move their photo to `assets/team/alumni/`. Keep only the file name in `image`. For `empty.jpg`, use the copy already in the alumni folder.
3. Set `role` to exactly one of these values: `Postdoc`, `Graduate Student`, `Postgraduate Student`, or `Undergraduate Student`. Other values do not appear on the alumni page.
4. Use `now` for the latest approved position or a dated career event. Use `past` for earlier positions and training. The page does not show `description` or `when`; put dates that readers need in `now` or `past`.

For a future move to alumni, Gustavo's entry could start like this. Add his confirmed position and dates when available:

```yaml
- name: Gustavo Madeira Santana
  role: Graduate Student
  image: gustavo-santana.jpg
  now:
  past: >
    Undergraduate degree in Computer Engineering, Federal University of Rio Grande do Sul.
```

The page groups alumni by role, then sorts each group by name. Readers can expand “Past positions and training” to see `past`. Use only approved career information. If no later position is supplied, leave `now` empty. Keep open questions in private review notes, outside the public site.

### People photos

Keep original photos. You do not need to make them square. The site displays small circular photos and opens the original when a reader selects one. Use lowercase file endings, such as `.jpg`, `.png`, or `.webp`. The build makes smaller copies when needed; keep `image` pointed at the original.

## Add a paper

Add the paper to **one** of these lists:

| File in `_data/` | Where the paper appears |
| --- | --- |
| `publications-neuro.yml` | Neuroscience and Everything |
| `publications-micro.yml` | Microbiology and Everything |
| `publications-shared.yml` | Both research areas and Everything |
| `publications-physics.yml` | Both research areas and Everything |

Copy a nearby entry and replace its details. Include the authors, title, journal or preprint service, and date:

```yaml
- authors: "Santana GM*, Vashistha H*, Emonet T#, Clark DA#"
  title: "A neural circuit for olfactory motion detection"
  journal: "bioRxiv"
  date: "2026-07-20"
```

Papers appear newest first. Write dates as quoted `"YYYY-MM-DD"` values. Use `edition` for volume and pages, `doi` for a DOI such as `10.64898/2026.07.13.738327`, and `html` for the full journal page address.

Put PDFs in `assets/papers/YYYY/`. Set `pdf` to a path such as `/assets/papers/2026/2026_Santana_etal_biorxiv.pdf`. Use `suppinfo` for a supporting PDF, `preprint` for a preprint link, and `extra` for notes or news links. Check the links on every publication page where the paper appears.

## Add gallery photos

1. Put photos in `assets/gallery/YYYY-YYYY/`, for example `assets/gallery/2025-2026/`. Use lowercase `.jpg`, `.jpeg`, `.png`, `.gif`, or `.webp` endings. Photos appear in file name order.
2. Add captions to `_data/galleries/2025-2026_details.yml`. Match each file name exactly. `alt` describes the photo for readers who cannot see it.

   ```yaml
   - filename: "lab-dinner.jpg"
     caption: "Lab dinner"
     alt: "Lab members gathered around a dinner table."
   ```

3. For a new album, add an entry to `_data/gallery.yml`, with the newest album first. Use a unique `YYYY-YYYY` ID and choose an existing photo as its cover:

   ```yaml
   - id: "2025-2026"
     cover: "lab-dinner.jpg"
   ```

A photo folder alone does not add an album to the site. Each listed album needs at least one photo and a valid cover. The build creates the album page and photo count. Keep the original photos; smaller display copies are made during the build.

Captions are optional. You can omit the caption file or leave it empty or with only comments. To add captions, use a list of entries with a `filename`, as shown above. The build reports the file name if the list format is wrong.

Animated GIF and WebP files keep their animation in the smaller display copies. After updating the image-processing code, use the fresh-folder build command below to replace any older copies that contain only one frame.

Check the gallery list, the album page, and the photo viewer. Try its arrows, keyboard controls, zoom, and download button.

## Change menus and page links

Menu items appear in the order listed in `_data/navigation.yml`:

```yaml
- text: Contact
  href: /contact/
```

Use the page's `permalink` value from its settings for `href`, rather than its file name. For a dropdown menu, copy an existing `menu` list. Only one level of items inside a dropdown is supported. Add `new_window: true` only when a link should open in a new tab.

Edit `_data/footer.yml` for links and text at the bottom of each page. Edit `social` in `_config.yml` for the lab's social links.

## Preview on your computer

The site uses Jekyll, a tool that turns these files into web pages. Install the Ruby version in [`.ruby-version`](.ruby-version), Bundler, Node.js 20 (the version used by the website build), ImageMagick 7, and `pkg-config`. On Linux, the Ruby image tools also need the ImageMagick development libraries (`libmagickwand-dev` on Ubuntu). For Ruby setup, see the [Jekyll installation guide](https://jekyllrb.com/docs/installation/).

In a terminal, open your copy of this repository. For a new copy, run:

```sh
git clone https://github.com/emonetlab/emonetlab.git
cd emonetlab
```

Install the required packages, then start the preview:

```sh
bundle install
npm ci
bundle exec jekyll serve --livereload
```

Open [the local preview](http://localhost:4000/). Saved content changes rebuild the pages and refresh the browser. After changing `_config.yml`, stop the server with `Ctrl+C` and start it again. Use `Ctrl+C` to stop when finished. See [Jekyll's command guide](https://jekyllrb.com/docs/usage/) for other options.

To check the site without starting a server:

```sh
bundle exec jekyll build
```

For gallery or image-processing changes, also run:

```sh
bundle exec ruby tests/gallery_test.rb
```

Generated pages and image copies go in `_site/`. Edit the source files, not `_site/`. If you change image-size or quality settings, build into a new folder outside the repository so old image copies are not reused:

```sh
bundle exec jekyll build --destination "$(mktemp -d)"
```

## Publish a checked update

Have the change reviewed, then merge it into `main`. Each push to `main` automatically builds and publishes the site. Check the [Actions page](https://github.com/emonetlab/emonetlab/actions) for completion or errors, then open the changed pages on the live site.

The build can also be started manually from the Actions page. Its steps are in [the website workflow](.github/workflows/jekyll-gh-pages.yml). There is no fixed completion time, and the workflow does not run the gallery tests.

## If something is wrong

| Problem | What to check |
| --- | --- |
| A post is missing | Check its folder, file name, and date. Future dates stay hidden. |
| An alumnus is missing | Check that `role` matches one of the four values above. |
| An image is missing | Match the path, file name, and letter case. Include the image with the update. |
| An album is missing | Check its entry in `_data/gallery.yml` and its cover file. |
| A caption is missing | Match `filename` to the photo's exact file name. |
| The build reports a missing LightGallery file | Run `npm ci`, then build again. |
| The build reports a YAML error | Check spacing and quotes near the reported line. |
| Old image sizes remain | Use the fresh-folder build command above. |
| The preview port is in use | Run `bundle exec jekyll serve --livereload --port 4001` and open port 4001. |
| Published changes are missing | Check Actions for completion, then refresh the page. |

A successful build does not prove that every link or photo works. Open the changed pages and check them.

For text formatting, see the [Markdown guide](assets/docs/markdown.md). The other files in `assets/docs/` describe the original Petridish theme and may differ from this site. The scripts in `old_website/` were used to copy the old site; they are not needed for routine updates.

AI assistants should read [AGENTS.md](AGENTS.md) before editing.
