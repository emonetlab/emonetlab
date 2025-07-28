---
layout: layout-with-gallery
title: Gallery
description: Photos from lab parties, outings, conferences...
background:
  img: /assets/backgrounds/AdobeStock_561560383.jpeg
  by: Adobe
permalink: /gallery/
---

{% assign album_names = "2023-2024,2022-2023,2021-2022,2018-2019" | split: "," %}

<nav id="toc" style="margin-bottom:40px;">
  <h3>Galleries by Year</h3>
  <ul>
    {% for album in album_names %}
      <li><a href="#{{ album | slugify }}">{{ album }}</a></li>
    {% endfor %}
  </ul>
</nav>

{% for album in album_names %}
  <h3 id="{{ album | slugify }}">{{ album }}</h3>
  {% include album.html albumname=album %}
  <br>
{% endfor %}


{%- content_for scripts -%}
<script type="text/javascript">
    document.addEventListener('DOMContentLoaded', function() {
        const galleries = document.querySelectorAll('.lightgallery-album');
        
        galleries.forEach(gallery => {
            lightGallery(gallery, {
                plugins: [lgZoom, lgThumbnail, lgCaptions],
                speed: 500,
                selector: 'a'
            });
        });
    });
</script>
{%- end_content_for -%}