# Emonet Lab website

see it live [here](https://emonetlab.github.io/emonetlab)

# Posting News

1. Duplicate a `.md` file in `_posts` (any old news post) as a starting template.
2. Edit the file name using the following format: `YYYY-MM-DD-title-separated-by-dashes.md`.
3. If using an image in the post, create a folder with the same name as the news posts `.md` file in `assets/posts`.
   - Place any images to be used in that folder
4. Edit the contents of the `.md` file with your news content.
   - Make sure to edit the frontmatter header:
     - `title`
     - `background` (this will be used as the photo on the news blurb on the home/archive page)
     - `date`
5. Push your changes to the repository and monitor the [GitHub Actions](https://github.com/emonetlab/emonetlab/actions) tab for any errors.


# Editing

## Navigation Menu

Navigation menu items and links are located in `_data/navigation.yml`.

## Lab members, alumni, publications...

All data is sorted alphabetically or by year depending on the content type. No need to reorder entries in the data files when adding/removing information.

-  Lab members data is located in `_data/team.yml`.
-  Alumni data is located in `_data/alumni.yml`.
  - Once a lab member leaves:
    - Move their picture from `assets/team` to `assets/team/alumni`.
    - Move their data from `team.yml` to `alumni.yml`.
    - ***Note:** the `team.html` and `alumni.html` pages look for pictures in their respective folders automatically.*
-  Neuroscience publications data is located in `_data/publications-neuro.yml`.
-  Microbiology publications data is located in `_data/publications-micro.yml`.
  - ***Note:** the "Everything" publications page populates automatically by combining both data files.*


Example entry for a new lab member:

```
- name: Gustavo Madeira Santana
  role: Graduate Student
  program: >
    [Interdepartmental Neuroscience Program](https://medicine.yale.edu/inp/), [Program in Physics, Engineering and Biology](https://physics-engineering-biology.yale.edu)
  image: empty.jpg
  description: > # Can be Markdown
    Gustavo completed his undergraduate in Computer Engineering at the Federal University of Rio Grande do Sul in Brazil, where he studied the ontogeny of vocal communication in mice. He is currently interested in understanding how flies explore spatiotemporal features of odor plumes for optimal navigation. In his free time, he spends too much money going to concerts, and enjoys playing guitar.
  googlescholar: L603SPwAAAAJ
  twitter: gumadeiras
  github: gumadeiras
  email: gustavo.santana@yale.edu
  website: https://gumadeiras.com
```

Example entry for a new publication:

```
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
    - [YouTube: Flies smell the motion of odors and use it to navigate](https://www.youtube.com/embed/3CC-0t8vPPM)
    - [How animals follow their nose](https://knowablemagazine.org/article/living-world/2023/how-animals-follow-their-nose), Knowable Magazine, by Dana Mackenzie, March 6 2023
```