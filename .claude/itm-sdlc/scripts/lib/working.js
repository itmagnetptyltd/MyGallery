"use strict";

/**
 * Informal working notes and reference files.
 *
 * Not FB / CHG / REQ. A developer polish, a screenshot, the words they typed
 * instead of the long loop. Lives under `.brain/docs/`.
 */

const fs = require("node:fs");
const path = require("node:path");
const yaml = require("js-yaml");

const REF_DIR = path.join(".brain", "docs", "ref");
const COMMANDS_FILE = path.join(".brain", "docs", "commands.yaml");

const IMAGE_EXT = new Set([".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"]);

function refDir(projectRoot) {
  return path.join(projectRoot, REF_DIR);
}

function commandsPath(projectRoot) {
  return path.join(projectRoot, COMMANDS_FILE);
}

function fileType(name) {
  const ext = path.extname(name).toLowerCase();
  if (IMAGE_EXT.has(ext)) return "Image";
  if (ext === ".pdf") return "PDF";
  if (ext === ".md" || ext === ".txt") return "Text";
  return "File";
}

function iconKind(type) {
  return String(type || "File").toLowerCase();
}

function listRefs(projectRoot) {
  const dir = refDir(projectRoot);
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir)
    .filter((name) => !name.startsWith("README") && !name.startsWith("."))
    .sort()
    .map((name, index) => {
      const serial =
        (name.match(/^(\d{3})-/) || [])[1] ||
        String(index + 1).padStart(3, "0");
      const type = fileType(name);
      return {
        serial,
        filename: name,
        type,
        kind: iconKind(type),
        path: `${REF_DIR.replace(/\\/g, "/")}/${name}`,
      };
    });
}

function listNotes(projectRoot) {
  const file = commandsPath(projectRoot);
  if (!fs.existsSync(file)) return [];
  let doc;
  try {
    doc = yaml.load(fs.readFileSync(file, "utf8"), {
      schema: yaml.CORE_SCHEMA,
    });
  } catch {
    return [];
  }
  if (!Array.isArray(doc)) return [];
  return doc
    .filter((row) => row && typeof row === "object")
    .map((row) => ({
      id: String(row.id || ""),
      at: String(row.at || ""),
      text: String(row.text || ""),
      files: Array.isArray(row.files) ? row.files.map(String) : [],
    }))
    .reverse();
}

function parsePromptLog(projectRoot) {
  const file = path.join(projectRoot, ".claude", "prompt-changes.md");
  if (!fs.existsSync(file)) return [];
  const text = fs.readFileSync(file, "utf8");
  return text
    .split(/^## /m)
    .slice(1)
    .map((part) => {
      const at = part.split(/\n/, 1)[0].trim();
      const prompt = (part.match(/^Prompt:\s*(.*)$/m) || [])[1] || "";
      return { at, text: prompt.trim() };
    })
    .reverse();
}

function nextSerial(projectRoot) {
  const used = listRefs(projectRoot).map((row) => Number(row.serial) || 0);
  const max = used.length ? Math.max(...used) : 0;
  return String(max + 1).padStart(3, "0");
}

function nextNoteId(notesNewestFirst) {
  const chronological = notesNewestFirst.slice().reverse();
  const last = chronological[chronological.length - 1];
  const n = last && last.id ? Number(String(last.id).replace(/\D/g, "")) : 0;
  return `NOTE-${String((Number.isFinite(n) ? n : 0) + 1).padStart(4, "0")}`;
}

function safeBase(name) {
  const base = path.basename(name).replace(/[^A-Za-z0-9._-]+/g, "-");
  return base.replace(/^-+|-+$/g, "") || "file";
}

module.exports = {
  REF_DIR,
  COMMANDS_FILE,
  refDir,
  commandsPath,
  fileType,
  iconKind,
  listRefs,
  listNotes,
  parsePromptLog,
  nextSerial,
  nextNoteId,
  safeBase,
};
