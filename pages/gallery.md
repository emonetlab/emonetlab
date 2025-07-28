---
layout: layout-with-gallery
title: Gallery
description: Photos from lab parties, outings, conferences...
background:
  img: /assets/backgrounds/AdobeStock_561560383.jpeg
  by: Adobe
permalink: /gallery/
---

{% comment %}
=============================================================================
  Step 1: Automatically Discover and Sort All Galleries
=============================================================================
This block inspects the `_data/galleries` directory, extracts the album
names from the filenames (e.g., '2021-2022' from '2021-2022_details.yml'),
and sorts them in reverse chronological order.
{% endcomment %}

{% assign temp_album_names = "" | split: "" %}
{% for gallery_file in site.data.galleries %}
  {% assign album_name = gallery_file[0] | remove_suffix: '_details' %}
  {% assign temp_album_names = temp_album_names | push: album_name %}
{% endfor %}
 
{% assign sorted_albums = temp_album_names | sort | reverse %}


{% comment %}
=============================================================================
  Step 2: Build the Table of Contents from the Sorted List
=============================================================================
This loops through the sorted list of album names to create the TOC.
{% endcomment %}

<nav id="toc" style="margin-bottom:40px;">
  <h3>Galleries by Year</h3>
  <ul>
    {% for album in sorted_albums %}
      <li>
        <a href="#{{ album | slugify }}">{{ album }}</a>
      </li>
    {% endfor %}
  </ul>
</nav>


{% comment %}
=============================================================================
  Step 3: Render Each Gallery Section from the Sorted List
=============================================================================
This loops through the same sorted list to create the section header and
include the album, ensuring they appear in the correct order on the page.
{% endcomment %}

{% for album in sorted_albums %}
  <h3 id="{{ album | slugify }}">{{ album }}</h3>
  {% include album.html albumname=album %}
  <br>
{% endfor %}
