---
title: Gallery
description: Photos from lab parties, outings, conferences...
background:
  img: /assets/backgrounds/AdobeStock_561560383.jpeg
  by: Adobe Stock
permalink: /gallery/
---

<h3>Pictures Our Lab 2018 2019</h3>
<div class="image-gallery" style="display: flex; flex-wrap: wrap; gap: 10px;">
  {% assign gallery_image_path = "assets/img/pictures-our-lab-2018-2019" %}
  {% assign image_files = "'Henry-and-Natalya-showing-their-salsa-moves.jpg', 'img_0546.jpg', 'img_0542.jpg', 'Thierrys-house-post-dinner.jpg', "}" %} <!-- Creates a Liquid array of filenames -->

  {% for image_filename in image_files %}
    {% assign image_data = site.data.galleries.pictures-our-lab-2018-2019 | where: "filename", image_filename | first %} <!-- Optional: For captions from _data -->
    {% assign caption = "" %}
    {% for img_info in site.data.galleries.pictures-our-lab-2018-2019_details %} {% comment %} Assuming you create a data file pictures-our-lab-2018-2019_details.yml {% endcomment %}
        {% if img_info.filename == image_filename %}
            {% assign caption = img_info.caption %}
            {% break %}
        {% endif %}
    {% endfor %}
    {% assign alt_text = caption | default: image_filename | split: '.' | first | replace: '_', ' ' | replace: '-', ' ' | capitalize %}

  <div class="gallery-item">
    <a href="{{ site.baseurl }}/{{ gallery_image_path }}/{{ image_filename }}" data-lightbox="pictures-our-lab-2018-2019" data-title="{{ alt_text }}">
      <img src="{{ site.baseurl }}/{{ gallery_image_path }}/{{ image_filename }}" alt="{{ alt_text }}" style="max-width: 200px; height: auto; margin: 5px; border: 1px solid #ccc;">
    </a>
    {% if caption != "" %}
      <p class="caption" style="text-align: center; font-size: 0.9em;">{{ caption }}</p>
    {% endif %}
  </div>
  {% endfor %}
</div>