# emonet lab website

see it live [here](https://emonetlab.github.io/emonetlab)

# Posting News

1. Duplicate a `.md` file in `_posts` (any old news post) as a starting template.
1. Edit the file name using the following format: `YYYY-MM-DD-title-separated-by-dashes.md`.
1. If using an image in the post, create a folder with the same name as the news posts `.md` file in `assets/posts`.
  - Place any images to be used in that folder
1. Edit the contents of the file with your post content.
  - Make sure to edit the frontmatter header:
    - `title`
    - `background` (this will be used as the photo on the the news blurb on the home/archive page)
    - `date`  

# Editing

## Navigation Menu

Navigation menu items and links are located in `_data/navigation.yml`.

## Lab Members, alumni, publications...

All data is sorted alphabetically or by year depending on the content type. No need to reorder entries in the data files when adding/removing information.

- Lab members data is located in `_data/team.yml`.
- Alumni data is located in `_data/alumni.yml`.
 - Once a lab member leaves:
   - Move their picture from `assets/team` to `assets/team/alumni`.
   - Move their data from `team.yml` to `alumni.yml`.
   ***Note:** the `team.html` and `alumni.html` pages look for pictures in their respective folders automatically.*
- Neuroscience publications data is located in `_data/publications-neuro.yml`.
- Microbiology publications data is located in `_data/publications-micro.yml`.
***Note:** the "Everything" publications page populates automatically by combining both data files.*
