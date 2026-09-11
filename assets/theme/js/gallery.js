(() => {
  const grid = document.querySelector('[data-gallery-manifest]');
  if (!grid || !window.lightGallery || !window.lgZoom) return;

  const status = document.querySelector('.gallery-status');
  const baseurl = grid.dataset.baseurl || '';
  const assetUrl = path => baseurl + path.split('/').map(encodeURIComponent).join('/');
  const escaped = text => {
    const span = document.createElement('span');
    span.textContent = text;
    return span.innerHTML.replace(/"/g, '&quot;');
  };
  let viewer;
  let albumRequest;
  let opener;
  let pendingIndex;
  let requestId = 0;

  grid.addEventListener('lgAfterClose', () => opener?.focus({ preventScroll: true }));

  grid.addEventListener('click', async event => {
    const link = event.target.closest('a[data-photo-index]');
    if (!link || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    opener = link;
    pendingIndex = Number(link.dataset.photoIndex);
    const currentRequest = ++requestId;

    if (viewer) {
      viewer.openGallery(pendingIndex, opener);
      return;
    }

    status.textContent = 'Opening album…';
    grid.setAttribute('aria-busy', 'true');
    try {
      // Metadata loads once, on demand. No other album or image is fetched here.
      albumRequest ||= fetch(grid.dataset.galleryManifest).then(response => {
        if (!response.ok) throw new Error(`Album request failed: ${response.status}`);
        return response.json();
      });
      const album = await albumRequest;
      if (currentRequest !== requestId) return;
      const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      viewer = lightGallery(grid, {
        dynamic: true,
        dynamicEl: album.photos.map(photo => ({
          src: assetUrl(photo.viewer),
          downloadUrl: assetUrl(photo.original),
          alt: escaped(photo.alt),
          subHtml: `<p>${escaped(photo.caption || `Photo ${photo.index + 1} · ${album.title}`)}</p>`
        })),
        plugins: [lgZoom],
        preload: 1,
        numberOfSlideItemsInDom: 3,
        controls: true,
        showCloseIcon: true,
        counter: true,
        ariaLabelledby: 'gallery-album-title',
        mobileSettings: { controls: true, showCloseIcon: true, download: true },
        speed: reducedMotion ? 0 : 250,
        backdropDuration: reducedMotion ? 0 : 150,
        hideBarsDelay: 0,
        // Keep controls visible while reading a caption or deciding where to go.
        hideScrollbar: true
      });
      viewer.openGallery(pendingIndex, opener);
      status.textContent = '';
    } catch (error) {
      albumRequest = null;
      if (currentRequest !== requestId) return;
      const original = document.createElement('a');
      original.href = link.href;
      original.textContent = 'Open this photo directly';
      status.replaceChildren('The album viewer could not load. Try again, or ', original, '.');
    } finally {
      if (currentRequest === requestId) grid.removeAttribute('aria-busy');
    }
  });

  // Escape can also cancel a slow album request before the viewer appears.
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && grid.hasAttribute('aria-busy')) {
      requestId++;
      grid.removeAttribute('aria-busy');
      status.textContent = '';
    }
  });
})();
