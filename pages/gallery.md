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
Step 1: Manually define the list of album names in the desired order (newest first).
This is the most direct and least error-prone method.
{% endcomment %}
{% assign album_names = "2023-2024,2022-2023,2021-2022,2018-2019" | split: "," %}


{% comment %}
Step 2: Build the Table of Contents from this list.
{% endcomment %}
<nav id="toc" style="margin-bottom:40px;">
  <h3>Galleries by Year</h3>
  <ul>
    {% for album in album_names %}
      <li>
        <a href="#{{ album | slugify }}">{{ album }}</a>
      </li>
    {% endfor %}
  </ul>
</nav>


{% comment %}
Step 3: Render each gallery section from the list.
{% endcomment %}
{% for album in album_names %}
  <h3 id="{{ album | slugify }}">{{ album }}</h3>
  
  {%- comment -%} 
    Directly include the album file here.
    This was the missing piece in the previous automated attempt.
  {%- endcomment -%}
  {% include album.html albumname=album %}
  
  <br>
{% endfor %}

