---
layout: layout-with-gallery
title: Gallery
description: Photos from lab parties, outings, conferences...
background:
  img: /assets/backgrounds/AdobeStock_561560383.jpeg
  by: Adobe
permalink: /gallery/
---

<script type="text/javascript">
    document.addEventListener('DOMContentLoaded', function() {
        // This code will only run after the full HTML page is loaded
        const galleryElement = document.getElementById("{{include.albumname}}");
        if (galleryElement) {
            lightGallery(galleryElement);
        }
    });
</script>

<h3>2023 - 2024</h3>

{% include album.html albumname="2023-2024" %}

<br>
<h3>2022 - 2023</h3>

{% include album.html albumname="2022-2023" %}

<br>
<h3>2021 - 2022</h3>

{% include album.html albumname="2021-2022" %}

<br>
<h3>2018 - 2019</h3>

{% include album.html albumname="2018-2019" %}
