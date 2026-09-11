---
layout: layout-with-gallery
title: Gallery
gallery: true
description: Photos from lab parties, outings, conferences...
background:
  img: /assets/backgrounds/AdobeStock_561560383.jpeg
  by: Adobe
permalink: /gallery/
---

<div class="gallery-index-heading">
  <h2>Albums through the years</h2>
</div>
<ul class="gallery-albums">
  {% for album in site.data.gallery_albums limit:6 %}
    <li id="{{ album.id }}">
      <a class="gallery-album-link" href="{{ album.url | relative_url }}">
        <div class="gallery-album-label">
          <h3>{{ album.title }}</h3>
          <span class="gallery-album-count">{{ album.count }} photos <span aria-hidden="true">→</span></span>
        </div>
        <img src="{{ album.cover.preview | relative_url }}" alt="" width="{{ album.cover.width }}" height="{{ album.cover.height }}" loading="{% if forloop.index <= 2 %}eager{% else %}lazy{% endif %}" decoding="async">
      </a>
    </li>
  {% endfor %}
</ul>
{% if site.data.gallery_albums.size > 6 %}
  <nav class="gallery-earlier" aria-label="Earlier albums">
    <h2>Earlier albums</h2>
    <ul>
      {% for album in site.data.gallery_albums offset:6 %}
        <li id="{{ album.id }}"><a href="{{ album.url | relative_url }}">{{ album.title }} <span>{{ album.count }} photos</span></a></li>
      {% endfor %}
    </ul>
  </nav>
{% endif %}
