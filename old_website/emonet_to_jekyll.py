#!/usr/bin/env python3
"""
sitemap_to_jekyll.py
Archive every URL listed in a sitemap to Jekyll-ready Markdown.

Outputs:
  _posts/YYYY-MM-DD-<slug>.md        – Markdown post
  assets/<slug>/<image_file>         – Downloaded images (referenced locally)

Usage:
  python sitemap_to_jekyll.py https://emonet.biology.yale.edu/sitemap.xml
"""

import os, re, time, argparse, concurrent.futures, urllib.parse, datetime, pathlib
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
# from slugify import slugify
from django.utils.text import slugify
from tqdm import tqdm
from xml.etree import ElementTree as ET
import urllib.parse, time
import dateparser  # Make sure this is imported at the top

# ----------------------------- configuration ---------------------------------
HEADERS           = {"User-Agent": "SiteArchiver/1.0 (+https://example.com)"}
DOWNLOAD_DELAY    = 0.5           # polite crawl delay (s)
MAX_WORKERS       = 6             # adjust for bandwidth / server friendliness
POSTS_DIR         = "_posts"
ASSETS_DIR        = "assets/posts"
TIMEZONE_OFFSET   = "-05:00"      # Yale / US Eastern (no DST handling here)
# -----------------------------------------------------------------------------

session = requests.Session()
session.headers.update(HEADERS)

# Helpers ---------------------------------------------------------------------

def safe_slug_from_title(title_raw: str | None, url: str) -> str:
    """
    Ensure we return a short, filesystem-safe slug.
    Falls back to the URL path + epoch time when the title is unusable.
    """
    if title_raw:
        # title_raw may be a BeautifulSoup NavigableString, bring it to str
        title_clean = str(title_raw).strip()
        slug = slugify(title_clean)           # allow_unicode=True if you prefer
        if slug:
            return slug

    # ---- fallback when <title> is missing or empty ----
    path = urllib.parse.urlparse(url).path.rstrip("/").split("/")[-1]
    if not path:                    # home page etc.
        path = "index"
    return slugify(f"{path}-{int(time.time())}")


def get_sitemap_locations(url: str) -> list[str]:
    """Return every <loc> URL in a sitemap or sitemap index."""
    resp = session.get(url, timeout=30)
    resp.raise_for_status()
    tree = ET.fromstring(resp.content)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    # If it's a plain sitemap
    loc_elems = tree.findall(".//sm:loc", ns)
    urls = [loc.text.strip() for loc in loc_elems]

    # If <loc> entries themselves are sitemap URLs, recurse once
    if tree.tag.endswith("sitemapindex"):
        url_set: list[str] = []
        for sm_url in urls:
            url_set.extend(get_sitemap_locations(sm_url))
        return url_set
    return urls


def fetch_url(url: str) -> tuple[str, requests.Response]:
    """GET a URL, return (url, response object) or raise."""
    time.sleep(DOWNLOAD_DELAY)
    r = session.get(url, timeout=30)
    r.raise_for_status()
    return url, r


def download_img(img_url: str, post_folder: str) -> str:
    """Download an image and return the local relative Jekyll path."""
    parsed = urllib.parse.urlparse(img_url)
    fname  = os.path.basename(parsed.path)
    if not fname:                       # e.g. .../image.php?id=xxx
        fname = slugify(img_url)[:32]
    local_dir  = pathlib.Path(ASSETS_DIR) / post_folder
    local_dir.mkdir(parents=True, exist_ok=True)
    local_path = local_dir / fname

    # Skip if already stored
    if not local_path.exists():
        try:
            resp = session.get(img_url, timeout=30)
            resp.raise_for_status()
            with open(local_path, "wb") as f:
                f.write(resp.content)
        except Exception as e:
            print(f"⚠️  Failed img {img_url}: {e}")
            return img_url  # fall back to original

    return str(local_path).replace("\\", "/")  # Jekyll absolute path


def html_to_markdown(html: str) -> str:
    """Convert HTML to Markdown with markdownify defaults."""
    return md(html, heading_style="ATX")


def build_front_matter(meta: dict) -> str:
    """Return YAML front matter from dict."""
    lines = ["---"]
    for k, v in meta.items():
        lines.append(f"{k}: \"{v}\"")
    lines.append("---\n")
    return "\n".join(lines)


def extract_date_from_content(soup) -> datetime.date | None:
    """
    Try to extract the post date from the content.
    Adjust the selector/regex based on your site's HTML structure.
    """
    # Example 1: <span class="post-date">2020-12-31</span>
    date_elem = soup.find("span", class_="date-display-single")
    if date_elem:
        date_text = date_elem.get_text(strip=True)
        dt = dateparser.parse(date_text)
        if dt:
            return dt.date()
    # Example 2: Regex search for date in the body text (YYYY-MM-DD)
    import re
    match = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", soup.get_text())
    if match:
        dt = dateparser.parse(match.group(1))
        if dt:
            return dt.date()
    return None


def process_page(url: str, lastmod: str | None = None):
    """Download, convert, and save one web page."""
    try:
        _, resp = fetch_url(url)
    except Exception as e:
        print(f"❌ {url}: {e}")
        return
    soup = BeautifulSoup(resp.text, "lxml")

    # 1 – Title
    title = soup.title.string.strip() if soup.title else urllib.parse.urlparse(url).path

    # 2 – Content selection (simple fallback: body)
    main_html = soup.body
    if not main_html:
        print(f"⚠️  No <body> in {url}")
        return

    # 5 – Determine publish date
    date_obj = extract_date_from_content(soup)  # <-------------------- USE THIS

    # fallback to today if not found
    if date_obj is None:
        date_obj = datetime.date.today()

    # 3 – Image handling
    slug = slugify(title)
    post_folder = f"{date_obj:%Y-%m-%d}-{slug}"
    fname = f"{date_obj:%Y-%m-%d}-{slug}.md"
    for img in main_html.find_all("img"):
        src = img.get("src") or ""
        if not src:
            continue
        img_abs = urllib.parse.urljoin(url, src)
        local = download_img(img_abs, post_folder)
        local_long = "{{ site.baseurl }}/" + local
        img["src"] = local
        alt = img.get("alt", "")
        img_markdown = f'![{alt}]({local_long})\n\n'
        img.decompose()

    # 4 – Extract only the main content div
    content_div = soup.find("div", class_="field field-name-body field-type-text-with-summary field-label-hidden")
    content_div = content_div.find("p") if content_div else None
    if not content_div:
        print(f"⚠️  No main content div in {url}")
        content_div = "no main content div found, add it manually"
        fname = f"NO-CONTENT-{date_obj:%Y-%m-%d}-{slug}.md"
        # return

    # 5 – Markdown conversion: only title and content
    title = title.replace("\n", "").replace(".", "").replace("  ", " ").replace('"', "'").replace(' | Emonet Lab', '')
    markdown_body = f"# {title}\n\n" + img_markdown + html_to_markdown(str(content_div))

    # 6 – Filename & front matter
    # print(f"📄 {fname} ({url})")
    fm = build_front_matter({
        "layout":        "post",
        "title":         title,
        "background":    local,
        "background-use": "no",
        "date":          f"{date_obj}",
        "original_url":  url
    })

    pathlib.Path(POSTS_DIR).mkdir(exist_ok=True)
    out_path = pathlib.Path(POSTS_DIR) / fname
    out_path.write_text(fm + markdown_body, encoding="utf-8")



# ------------------------------ main entry -----------------------------------

def main():
    parser = argparse.ArgumentParser(description="Archive sitemap to Jekyll posts")
    parser.add_argument("sitemap_url", help="Full URL of sitemap.xml")
    args = parser.parse_args()

    urls = get_sitemap_locations(args.sitemap_url)
    print(f"Found {len(urls):,} URLs in sitemap")

    # Optional: map sitemap lastmod per URL
    # (very tiny gain; skip to keep script short)
    lastmods: dict[str, str | None] = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(process_page, url, lastmods.get(url)): url for url in urls}
        # tqdm progress bar
        for _ in tqdm(concurrent.futures.as_completed(futures), total=len(futures), ncols=80):
            pass


if __name__ == "__main__":
    main()
