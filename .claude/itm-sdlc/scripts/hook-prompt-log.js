#!/usr/bin/env node
"use strict";

/**
 * Hook 2 — save the prompt that changed the project.
 *
 * capture  (beforeSubmitPrompt) — remember the last user prompt
 * record   (afterFileEdit)      — append it if a project file changed
 *
 * Skips: /tdd (that skill already owns the slice), and the format hook's
 * second write. Does not write .brain/ — this is a working log.
 *
 * Usage:
 *   node hook-prompt-log.js capture
 *   node hook-prompt-log.js record
 */

const fs = require("node:fs");
const path = require("node:path");

const {
  readStdinJson,
  fileFromPayload,
  promptFromPayload,
  attachmentsFromPayload,
  isTddPrompt,
  projectPaths,
  ensureDir,
  writeJson,
  readJson,
} = require("./lib/hooks");
const {
  copyToRef,
  isToolkitRoot,
  cursorAssetDirs,
  listRecentFiles,
} = require("./lib/working");

const HARVEST_MS = 10 * 60 * 1000;

function lastPromptFile(projectRoot) {
  return path.join(projectPaths(projectRoot).stateDir, "last-prompt.json");
}

function keptRefsFile(projectRoot) {
  return path.join(projectPaths(projectRoot).stateDir, "kept-refs.json");
}

function rememberedSources(projectRoot) {
  const doc = readJson(keptRefsFile(projectRoot));
  return doc && doc.sources && typeof doc.sources === "object"
    ? doc.sources
    : {};
}

function rememberSources(projectRoot, sources, names) {
  const sourcesMap = rememberedSources(projectRoot);
  sources.forEach((src, i) => {
    if (names[i]) sourcesMap[path.resolve(src)] = names[i];
  });
  writeJson(keptRefsFile(projectRoot), { sources: sourcesMap });
}

function isChatAttachment(file) {
  const abs = path.resolve(String(file || ""));
  const n = abs.split(path.sep).join("/");
  return (
    n.includes("/.cursor/projects/") ||
    n.includes("/workspaceStorage/") ||
    /\/assets\//i.test(n)
  );
}

function uniqueExisting(files) {
  const seen = new Set();
  const out = [];
  for (const file of files || []) {
    const abs = path.resolve(file);
    if (seen.has(abs)) continue;
    seen.add(abs);
    try {
      if (fs.existsSync(abs) && fs.statSync(abs).isFile()) out.push(abs);
    } catch {
      /* skip */
    }
  }
  return out;
}

function keepNewFiles(projectRoot, files) {
  if (isToolkitRoot(projectRoot)) return [];
  const known = rememberedSources(projectRoot);
  const fresh = uniqueExisting(files).filter((file) => !known[file]);
  if (!fresh.length) return [];
  const kept = copyToRef(projectRoot, fresh);
  rememberSources(projectRoot, fresh, kept);
  return kept;
}

function harvestFromDisk(projectRoot, extraDirs) {
  const since = Date.now() - HARVEST_MS;
  const dirs = [...cursorAssetDirs(projectRoot), ...(extraDirs || [])];
  return keepNewFiles(projectRoot, listRecentFiles(dirs, since));
}

function capture(raw, options = {}) {
  const projectRoot = options.projectRoot ?? process.cwd();
  const payload = readStdinJson(raw);
  const prompt = promptFromPayload(payload);
  writeJson(lastPromptFile(projectRoot), {
    prompt,
    skip: isTddPrompt(prompt),
    at: Date.now(),
  });
  let kept = [];
  try {
    kept = keepNewFiles(projectRoot, [
      ...attachmentsFromPayload(payload),
      ...listRecentFiles(
        [...cursorAssetDirs(projectRoot), ...(options.assetDirs || [])],
        Date.now() - HARVEST_MS,
      ),
    ]);
  } catch {
    kept = [];
  }
  return { captured: Boolean(prompt), skip: isTddPrompt(prompt), kept };
}

function harvest(raw, options = {}) {
  const projectRoot = options.projectRoot ?? process.cwd();
  let kept = [];
  try {
    kept = harvestFromDisk(projectRoot, options.assetDirs);
  } catch {
    kept = [];
  }
  return { kept };
}

function keepRead(raw, options = {}) {
  const projectRoot = options.projectRoot ?? process.cwd();
  const payload = readStdinJson(raw);
  const nested = payload.tool_input || payload.arguments || payload;
  const file = fileFromPayload(nested) || fileFromPayload(payload);
  let kept = [];
  try {
    if (file && isChatAttachment(file)) {
      kept = keepNewFiles(projectRoot, [file]);
    }
  } catch {
    kept = [];
  }
  return { kept, permission: "allow" };
}

function sameFile(projectRoot, a, b) {
  if (!a || !b) return false;
  return path.resolve(projectRoot, a) === path.resolve(projectRoot, b);
}

function shouldSkip(projectRoot, file) {
  const last = readJson(lastPromptFile(projectRoot));
  if (!last) return "no-prompt";
  if (last.skip) return "tdd";
  if (!last.prompt) return "empty-prompt";

  const stamp = readJson(
    path.join(projectPaths(projectRoot).stateDir, "format-stamp.json"),
  );
  if (
    stamp &&
    sameFile(projectRoot, stamp.file, file) &&
    Date.now() - stamp.at < 4000
  )
    return "format";

  return null;
}

function record(raw, options = {}) {
  const projectRoot = options.projectRoot ?? process.cwd();
  const file = fileFromPayload(readStdinJson(raw));
  if (!file) return { skipped: "no-file" };

  const relative = path
    .relative(projectRoot, path.resolve(projectRoot, file))
    .split(path.sep)
    .join("/");
  if (
    relative.startsWith(".claude/itm-sdlc/") ||
    relative.startsWith(".claude/reports/") ||
    relative.startsWith(".cursor/hook-state/")
  ) {
    return { skipped: "toolkit" };
  }

  const reason = shouldSkip(projectRoot, file);
  if (reason) return { skipped: reason };

  const last = readJson(lastPromptFile(projectRoot));
  const paths = projectPaths(projectRoot);
  ensureDir(path.dirname(paths.logFile));

  const header = fs.existsSync(paths.logFile)
    ? ""
    : "# Prompt changes\n\nPrompts that changed project files. Not /tdd. Not format.\n\n";

  const stamp = new Date().toISOString();
  const block = `${header}## ${stamp}\n\nPrompt: ${last.prompt}\n\nFiles:\n- ${relative}\n\n`;
  fs.appendFileSync(paths.logFile, block);
  return { logged: relative };
}

function run(mode, raw, options = {}) {
  if (mode === "capture") return capture(raw, options);
  if (mode === "record") return record(raw, options);
  if (mode === "harvest") return harvest(raw, options);
  if (mode === "keep-read") return keepRead(raw, options);
  throw new Error(`unknown mode: ${mode}`);
}

if (require.main === module) {
  const mode = process.argv[2];
  const raw = fs.readFileSync(0, "utf8");
  const result = run(mode, raw);
  if (mode === "keep-read") {
    process.stdout.write(`${JSON.stringify({ permission: "allow" })}\n`);
  }
}

module.exports = { run, capture, record, harvest, keepRead };
