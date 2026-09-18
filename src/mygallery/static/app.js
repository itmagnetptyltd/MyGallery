'use strict';

// The Gallery: upload, render Thumbnails newest first, and load more as the
// user scrolls. No numbered page control — REQ-GAL-003 asks for none.

const input = document.querySelector('[data-testid="upload-input"]');
const count = document.querySelector('[data-testid="photo-count"]');
const gallery = document.querySelector('[data-testid="gallery"]');
const empty = document.querySelector('[data-testid="empty-gallery"]');
const errorMessage = document.querySelector('[data-testid="gallery-error"]');
const sentinel = document.querySelector('[data-testid="scroll-sentinel"]');

let nextCursor = null;
let loading = false;
let total = 0;

function tileFor(photo) {
  // createElement and textContent, never innerHTML: the filename came from a
  // user, and a Photo called <img onerror=...> must stay text.
  const tile = document.createElement('img');
  tile.className = 'tile';
  tile.src = `/api/photos/${photo.id}/thumbnail`;
  tile.alt = photo.filename;
  tile.dataset.testid = 'thumbnail';
  tile.dataset.filename = photo.filename;
  return tile;
}

function showState() {
  empty.hidden = total !== 0;
  gallery.hidden = total === 0;
}

async function loadPage({ reset = false } = {}) {
  if (loading) {
    return;
  }
  if (!reset && nextCursor === null && total > 0) {
    return;
  }
  loading = true;
  try {
    const query = !reset && nextCursor !== null ? `?after=${nextCursor}` : '';
    const response = await fetch(`/api/photos${query}`);
    if (!response.ok) {
      // REQ-GAL-007: a Gallery that cannot be read reports an error, and the
      // no-photos-yet message stays hidden.
      errorMessage.hidden = false;
      empty.hidden = true;
      return;
    }
    errorMessage.hidden = true;
    const body = await response.json();
    if (reset) {
      gallery.replaceChildren();
      total = 0;
    }
    for (const photo of body.photos) {
      gallery.append(tileFor(photo));
    }
    total += body.photos.length;
    nextCursor = body.nextCursor;
    count.textContent = String(total);
    showState();
  } finally {
    loading = false;
  }
}

async function upload(files) {
  const form = new FormData();
  for (const file of files) {
    form.append('photos', file);
  }
  await fetch('/api/photos', { method: 'POST', body: form });
  nextCursor = null;
  await loadPage({ reset: true });
}

input.addEventListener('change', (event) => {
  if (event.target.files.length > 0) {
    void upload(event.target.files);
  }
});

new IntersectionObserver((entries) => {
  if (entries.some((entry) => entry.isIntersecting) && nextCursor !== null) {
    void loadPage();
  }
}).observe(sentinel);

void loadPage({ reset: true });
