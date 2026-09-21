---
name: note
description: Save an informal working note and optional files (screenshots, emails) without a requirement or change record. Use for polish, a look tweak, or "just do this" after a slice is built. /note
allowed-tools: Read, Grep, Glob, Write, Bash
---

# note

Saves **the words they typed** and any files they attached. Not a REQ. Not a CHG.
Shows on the dashboard **Working** tab.

**Invoke as** `/note` plus the words. Attach files in the chat if there are any.

---

## Before running a vendored script

```bash
[ -f .claude/itm-sdlc/scripts/note.js ] || echo "vendored toolkit predates note.js - re-run install.js"
```

If it is missing, say that and stop. If `.claude/itm-sdlc/node_modules/` is missing:

```bash
cd .claude/itm-sdlc && npm ci --omit=dev --no-audit --no-fund
```

Then return to the project root.

---

## 1. Write the note

Copy any attached files into the project first if they are only in the chat.
Then:

```bash
node .claude/itm-sdlc/scripts/note.js --project . --text "THEIR WORDS HERE"
```

Add `--file path/to/shot.png` once per file.

**Show the script output as written.**

## 2. Refresh the dashboard if they want it on screen

```bash
node .claude/itm-sdlc/scripts/dashboard.js --project . --open
```

The **Working** tab lists the note and a table of files in `.brain/docs/ref/`
(serial, filename, type, icon).

## 3. Do not

- Do not open `/feedback-capture` from here unless they said it is client UAT
  that must be classified.
- Do not version a requirement.
- Do not start `/tdd`.

---

## Then

That is the record. Code the polish if it is not done yet. Lost? `/help`
