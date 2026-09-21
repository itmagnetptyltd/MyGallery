#!/usr/bin/env node
"use strict";

/**
 * Save an informal working note (polish, screenshot, the words they typed).
 * Not a requirement. Not a change record.
 *
 * Usage:
 *   node scripts/note.js --project <path> --text "..." [--file <path>]...
 */

const fs = require("node:fs");
const path = require("node:path");
const yaml = require("js-yaml");
const {
  REF_DIR,
  commandsPath,
  refDir,
  listNotes,
  listRefs,
  nextSerial,
  nextNoteId,
  safeBase,
} = require("./lib/working");

const EXIT_OK = 0;
const EXIT_TOOL_ERROR = 2;

function parseArgs(argv) {
  const options = { project: process.cwd(), text: "", files: [], help: false };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "-h" || arg === "--help") options.help = true;
    else if (arg === "--project") {
      i += 1;
      options.project = argv[i];
    } else if (arg === "--text") {
      i += 1;
      options.text = argv[i] ?? "";
    } else if (arg === "--file") {
      i += 1;
      if (argv[i]) options.files.push(argv[i]);
    } else throw new Error(`unknown option: ${arg}`);
  }
  return options;
}

function copyFiles(projectRoot, sources) {
  const destDir = refDir(projectRoot);
  fs.mkdirSync(destDir, { recursive: true });
  const copied = [];
  let serial = nextSerial(projectRoot);
  for (const source of sources) {
    const abs = path.resolve(source);
    if (!fs.existsSync(abs) || !fs.statSync(abs).isFile()) {
      throw new Error(`not a file: ${source}`);
    }
    const destName = `${serial}-${safeBase(abs)}`;
    fs.copyFileSync(abs, path.join(destDir, destName));
    copied.push(destName);
    serial = String(Number(serial) + 1).padStart(3, "0");
  }
  return copied;
}

function addNote(projectRoot, text, files) {
  const trimmed = String(text || "").trim();
  if (!trimmed) throw new Error("missing --text");
  const copied = copyFiles(projectRoot, files);
  const notes = listNotes(projectRoot).slice().reverse();
  const row = {
    id: nextNoteId(listNotes(projectRoot)),
    at: new Date().toISOString(),
    text: trimmed,
    files: copied,
  };
  notes.push(row);
  const dest = commandsPath(projectRoot);
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.writeFileSync(
    dest,
    yaml.dump(notes, { lineWidth: 88, noRefs: true, quotingType: '"' }),
  );
  return { note: row, refs: listRefs(projectRoot) };
}

function formatReport(result) {
  const files = result.note.files.length
    ? result.note.files.join(", ")
    : "(none)";
  return [
    `Saved ${result.note.id}`,
    `  ${result.note.text}`,
    `  files: ${files}`,
    "",
    "Shown on the dashboard Others tab. Not a REQ. Not a CHG.",
    "",
  ].join("\n");
}

function main(argv) {
  try {
    const options = parseArgs(argv);
    if (options.help) {
      process.stdout.write(
        'Usage: node scripts/note.js --project <path> --text "..." [--file <path>]...\n',
      );
      return EXIT_OK;
    }
    const result = addNote(options.project, options.text, options.files);
    process.stdout.write(formatReport(result));
    return EXIT_OK;
  } catch (err) {
    process.stderr.write(`${err.message}\n`);
    return EXIT_TOOL_ERROR;
  }
}

if (require.main === module) {
  process.exitCode = main(process.argv.slice(2));
}

module.exports = {
  parseArgs,
  addNote,
  copyFiles,
  main,
  REF_DIR,
};
