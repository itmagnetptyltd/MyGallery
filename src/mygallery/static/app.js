"use strict";

// The Gallery: upload, render Thumbnails newest first, and load more as the
// user scrolls. No numbered page control — REQ-GAL-003 asks for none.

const input = document.querySelector('[data-testid="upload-input"]');
const count = document.querySelector('[data-testid="photo-count"]');
const gallery = document.querySelector('[data-testid="gallery"]');
const empty = document.querySelector('[data-testid="empty-gallery"]');
const errorMessage = document.querySelector('[data-testid="gallery-error"]');
const uploadFailures = document.querySelector(
  '[data-testid="upload-failures"]',
);
const sentinel = document.querySelector('[data-testid="scroll-sentinel"]');
const largerView = document.querySelector('[data-testid="larger-view"]');
const largerViewPhoto = document.querySelector(
  '[data-testid="larger-view-photo"]',
);
const largerViewClose = document.querySelector(
  '[data-testid="larger-view-close"]',
);
const deletePhoto = document.querySelector('[data-testid="delete-photo"]');
const deleteConfirmation = document.querySelector(
  '[data-testid="delete-confirmation"]',
);
const deleteConfirm = document.querySelector('[data-testid="delete-confirm"]');
const deleteDecline = document.querySelector('[data-testid="delete-decline"]');

// The Photo the Larger view is currently showing — what Delete acts on.
let openPhotoId = null;

let nextCursor = null;
let loading = false;
let total = 0;

function tileFor(photo) {
  // createElement and textContent, never innerHTML: the filename came from a
  // user, and a Photo called <img onerror=...> must stay text.
  const tile = document.createElement("img");
  tile.className = "tile";
  tile.src = `/api/photos/${photo.id}/thumbnail`;
  tile.alt = photo.filename;
  tile.dataset.testid = "thumbnail";
  tile.dataset.filename = photo.filename;
  tile.dataset.photoId = photo.id;
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
    const query = !reset && nextCursor !== null ? `?after=${nextCursor}` : "";
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

function showFailures(refused) {
  uploadFailures.replaceChildren();
  if (!refused || refused.length === 0) {
    uploadFailures.hidden = true;
    return;
  }
  for (const item of refused) {
    const row = document.createElement("li");
    row.dataset.testid = "upload-failure";
    row.textContent = `${item.filename}: ${item.reason}`;
    uploadFailures.append(row);
  }
  uploadFailures.hidden = false;
}

async function upload(files) {
  const form = new FormData();
  for (const file of files) {
    form.append("photos", file);
  }
  const response = await fetch("/api/photos", { method: "POST", body: form });
  const body = await response.json();
  showFailures(body.refused);
  nextCursor = null;
  await loadPage({ reset: true });
}

// REQ-GAL-004. Delegated, because tiles arrive as the user scrolls.
gallery.addEventListener("click", (event) => {
  const tile = event.target.closest('[data-testid="thumbnail"]');
  if (!tile) {
    return;
  }
  largerViewPhoto.src = `/api/photos/${tile.dataset.photoId}`;
  largerViewPhoto.alt = tile.dataset.filename;
  largerViewPhoto.dataset.filename = tile.dataset.filename;
  openPhotoId = tile.dataset.photoId;
  largerView.showModal();
});

// Escape is handled by <dialog> itself; this is the close control.
largerViewClose.addEventListener("click", () => {
  largerView.close();
});

// REQ-GAL-005. Asking is not deleting: nothing is removed until confirmed.
deletePhoto.addEventListener("click", () => {
  deleteConfirmation.showModal();
});

deleteDecline.addEventListener("click", () => {
  deleteConfirmation.close();
});

deleteConfirm.addEventListener("click", () => {
  void (async () => {
    await fetch(`/api/photos/${openPhotoId}`, { method: "DELETE" });
    deleteConfirmation.close();
    largerView.close();
    openPhotoId = null;
    nextCursor = null;
    await loadPage({ reset: true });
  })();
});

input.addEventListener("change", (event) => {
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
