"use strict";

// The Gallery: upload, render Thumbnails newest first, and load more as the
// user scrolls. No numbered page control — REQ-GAL-003 asks for none.

const input = document.querySelector('[data-testid="upload-input"]');
const uploadOpen = document.querySelector('[data-testid="upload-open"]');
const uploadPopup = document.querySelector('[data-testid="upload-popup"]');
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
const largerViewCloseButton = document.querySelector(
  '[data-testid="larger-view-close-button"]',
);
const deleteConfirmation = document.querySelector(
  '[data-testid="delete-confirmation"]',
);
const deleteConfirm = document.querySelector('[data-testid="delete-confirm"]');
const deleteDecline = document.querySelector('[data-testid="delete-decline"]');
const uploadPreviews = document.querySelector(
  '[data-testid="upload-previews"]',
);
const uploadDescription = document.querySelector(
  '[data-testid="upload-description"]',
);
const uploadSubmit = document.querySelector('[data-testid="upload-submit"]');
const uploadPopupClose = document.querySelector(
  '[data-testid="upload-popup-close"]',
);
const descriptionCount = document.querySelector(
  '[data-testid="description-count"]',
);
const largerViewDescriptionCount = document.querySelector(
  '[data-testid="larger-view-description-count"]',
);
const largerViewDescription = document.querySelector(
  '[data-testid="larger-view-description"]',
);
const descriptionSave = document.querySelector(
  '[data-testid="description-save"]',
);

// What the popup is holding, chosen but not yet uploaded. REQ-GAL-001@v3
// separates choosing from uploading, so the files have to live somewhere
// between the two.
let chosen = [];

// The Photo the Larger view is currently showing.
let openPhotoId = null;

// The Photo the delete confirmation is about, set by the card's Delete that
// asked (REQ-GAL-003@v4 c14).
let pendingDeletePhotoId = null;

let nextCursor = null;
let loading = false;
let total = 0;

function tileFor(photo) {
  // createElement and textContent, never innerHTML: the filename came from a
  // user, and a Photo called <img onerror=...> must stay text.
  const card = document.createElement("article");
  card.className = "thumbnail-card";
  card.dataset.testid = "thumbnail-card";
  const tile = document.createElement("img");
  tile.className = "tile";
  tile.src = `/api/photos/${photo.id}/thumbnail`;
  // REQ-GAL-003@v3 c9/c10: the client chose alt over a tooltip.
  tile.alt = photo.description || photo.filename;
  // FB-0004 also asked for it "on mousemove". No browser shows alt on hover,
  // so title carries the same text. alt is untouched and still the criterion.
  tile.title = photo.description || photo.filename;
  tile.dataset.description = photo.description || "";
  tile.dataset.testid = "thumbnail";
  tile.dataset.filename = photo.filename;
  tile.dataset.photoId = photo.id;
  // The frame clips the hover zoom to the image's rounded edge. The badge is
  // decoration only: the Photo's text stays in alt, as the client chose.
  const frame = document.createElement("div");
  frame.className = "tile-frame";
  const badge = document.createElement("span");
  badge.className = "tile-zoom";
  badge.setAttribute("aria-hidden", "true");
  frame.append(tile, badge);
  card.append(frame, cardActionsFor(photo));
  return card;
}

// REQ-GAL-003@v4 c11-c15: Download and Delete on every card, always shown.
// Download is a link: the route already sends Content-Disposition, so the
// browser saves the file with no script involved.
function cardActionsFor(photo) {
  const actions = document.createElement("div");
  actions.className = "card-actions";
  const download = document.createElement("a");
  download.className = "outline-button";
  download.dataset.testid = "card-download";
  download.href = `/api/photos/${photo.id}/download`;
  download.download = "";
  download.append(iconFor(DOWNLOAD_ICON), labelFor("Download"));
  const remove = document.createElement("button");
  remove.type = "button";
  remove.className = "danger";
  remove.dataset.testid = "card-delete";
  remove.dataset.photoId = photo.id;
  remove.append(iconFor(DELETE_ICON), labelFor("Delete"));
  actions.append(download, remove);
  return actions;
}

// Inline SVG rather than an image: the CSP allows no data: URLs, and an SVG
// drawn with currentColor follows the button's own colour on hover.
const SVG_NS = "http://www.w3.org/2000/svg";
const DOWNLOAD_ICON = ["M12 4v11", "m7 10 5 5 5-5", "M5 20h14"];
const DELETE_ICON = ["M4 7h16", "M9 7V4h6v3", "M6 7l1 13h10l1-13", "M10 11v6", "M14 11v6"];

function iconFor(paths) {
  const svg = document.createElementNS(SVG_NS, "svg");
  svg.setAttribute("viewBox", "0 0 24 24");
  svg.setAttribute("aria-hidden", "true");
  svg.classList.add("card-action-icon");
  for (const d of paths) {
    const path = document.createElementNS(SVG_NS, "path");
    path.setAttribute("d", d);
    svg.append(path);
  }
  return svg;
}

function labelFor(text) {
  const label = document.createElement("span");
  label.textContent = text;
  return label;
}

function showChosen(files) {
  // REQ-GAL-001@v3 c15/c16. createObjectURL rather than a FileReader: a batch
  // of thirty full-size phone photos read as data URLs is tens of megabytes of
  // string in memory for no gain.
  for (const url of chosen.map((file) => file.previewUrl)) {
    URL.revokeObjectURL(url);
  }
  chosen = Array.from(files).map((file) => {
    file.previewUrl = URL.createObjectURL(file);
    return file;
  });

  uploadPreviews.replaceChildren();
  for (const file of chosen) {
    const item = document.createElement("li");
    item.dataset.testid = "upload-preview";
    const image = document.createElement("img");
    image.className = "upload-preview-image";
    image.src = file.previewUrl;
    image.alt = file.name;
    item.append(image);
    uploadPreviews.append(item);
  }
  uploadPreviews.hidden = chosen.length === 0;
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

async function upload(files, description) {
  const form = new FormData();
  for (const file of files) {
    form.append("photos", file);
  }
  if (description) {
    form.append("description", description);
  }
  const response = await fetch("/api/photos", { method: "POST", body: form });
  const body = await response.json();
  showFailures(body.refused);
  nextCursor = null;
  await loadPage({ reset: true });
}

// REQ-GAL-004. Delegated, because tiles arrive as the user scrolls.
gallery.addEventListener("click", (event) => {
  // c13/c14: a card's own controls act on the card, and never open the
  // Larger view. Delete asks first, exactly as it does from the Larger view.
  const cardDelete = event.target.closest('[data-testid="card-delete"]');
  if (cardDelete) {
    pendingDeletePhotoId = cardDelete.dataset.photoId;
    deleteConfirmation.showModal();
    return;
  }
  if (event.target.closest(".card-actions")) {
    return;
  }
  const card = event.target.closest('[data-testid="thumbnail-card"]');
  const tile =
    event.target.closest('[data-testid="thumbnail"]') ||
    (card ? card.querySelector('[data-testid="thumbnail"]') : null);
  if (!tile) {
    return;
  }
  largerViewPhoto.src = `/api/photos/${tile.dataset.photoId}`;
  largerViewPhoto.alt = tile.dataset.filename;
  largerViewPhoto.dataset.filename = tile.dataset.filename;
  largerViewDescription.value = tile.dataset.description || "";
  showLargerViewDescriptionCount();
  openPhotoId = tile.dataset.photoId;
  largerView.showModal();
});

// Escape is handled by <dialog> itself. The round close control and the
// Close button (REQ-GAL-004@v3 c8) do the same thing.
for (const control of [largerViewClose, largerViewCloseButton]) {
  control.addEventListener("click", () => {
    largerView.close();
  });
}

// REQ-GAL-005. Asking is not deleting: nothing is removed until confirmed.

deleteDecline.addEventListener("click", () => {
  deleteConfirmation.close();
});

deleteConfirm.addEventListener("click", () => {
  void (async () => {
    await fetch(`/api/photos/${pendingDeletePhotoId}`, { method: "DELETE" });
    deleteConfirmation.close();
    pendingDeletePhotoId = null;
    nextCursor = null;
    await loadPage({ reset: true });
  })();
});

// REQ-GAL-017 c4/c5. The limit is read from the field rather than written
// again here: maxlength is what actually stops the typing, so a second copy
// of the number could only ever drift away from it.
function countInto(field, output) {
  const show = () => {
    output.textContent = `${field.value.length}/${field.maxLength}`;
  };
  field.addEventListener("input", show);
  return show;
}

const showDescriptionCount = countInto(uploadDescription, descriptionCount);
showDescriptionCount();

// The Larger view edits against the same 250-character limit, so it shows the
// same count. Refreshed when a Photo is opened, not only when typing starts.
const showLargerViewDescriptionCount = countInto(
  largerViewDescription,
  largerViewDescriptionCount,
);
showLargerViewDescriptionCount();

uploadOpen.addEventListener("click", () => {
  uploadPopup.showModal();
});

// REQ-GAL-013@v2 c4: closing adds no Photo. Nothing here uploads — it only
// puts back what was chosen, so reopening starts clean.
uploadPopupClose.addEventListener("click", () => {
  uploadPopup.close();
});

// REQ-GAL-001@v3: choosing shows previews and stops. The Upload is a
// separate act, because c15 requires the chosen files to be visible before it.
input.addEventListener("change", (event) => {
  showChosen(event.target.files);
});

// REQ-GAL-001@v3 c14: dropping on the popup chooses files, as the picker does.
uploadPopup.addEventListener("dragover", (event) => {
  event.preventDefault();
});

uploadPopup.addEventListener("drop", (event) => {
  event.preventDefault();
  if (event.dataTransfer && event.dataTransfer.files.length > 0) {
    showChosen(event.dataTransfer.files);
  }
});

uploadSubmit.addEventListener("click", () => {
  if (chosen.length === 0) {
    return;
  }
  const files = chosen;
  const description = uploadDescription.value;
  uploadPopup.close();
  uploadPreviews.replaceChildren();
  uploadPreviews.hidden = true;
  chosen = [];
  uploadDescription.value = "";
  input.value = "";
  void upload(files, description);
});

// REQ-GAL-002@v2 c9: the description is changed here, in the Larger view.
descriptionSave.addEventListener("click", () => {
  void (async () => {
    await fetch(`/api/photos/${openPhotoId}/description`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ description: largerViewDescription.value }),
    });
    largerView.close();
    nextCursor = null;
    await loadPage({ reset: true });
  })();
});

new IntersectionObserver((entries) => {
  if (entries.some((entry) => entry.isIntersecting) && nextCursor !== null) {
    void loadPage();
  }
}).observe(sentinel);

void loadPage({ reset: true });
