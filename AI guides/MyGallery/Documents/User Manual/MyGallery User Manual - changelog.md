# Change log: MyGallery User Manual

Every iteration of this document, newest version first. Content rows describe what a reader would notice and are the raw material for the release notes. Formatting rows are kept for the record and are not published.

Kinds: `Content` for anything that changes what the reader is told or does. `Formatting` for layout, styles and production only.

## v1.0, in progress

| Date | Draft | Kind | Change | Reason | Evidence |
| --- | --- | --- | --- | --- | --- |
| 2026-09-23 | 02 | Content | Qualified the downloaded filename as usual rather than guaranteed, and stated the fallback naming | QA finding C1 | AI guides/MyGallery/Documents/User Manual/Logs/MyGallery User Manual v1.0 draft 01 - qa-report.md, finding C1; gal.yaml REQ-GAL-006 c4-c5 |
| 2026-09-23 | 02 | Content | Split the Address-already-in-use fix into two steps, so the black window confirms MyGallery is running and the Gallery's appearance is the browser's result alone | QA finding C2 | AI guides/MyGallery/Documents/User Manual/Logs/MyGallery User Manual v1.0 draft 01 - qa-report.md, finding C2 |
| 2026-09-23 | 02 | Content | Cut the Thumbnails folder and the index from the Gallery-folder description, keeping only that Photos are ordinary files there | QA finding C3 | AI guides/MyGallery/Documents/User Manual/Logs/MyGallery User Manual v1.0 draft 01 - qa-report.md, finding C3; config.py:26-29, outside the source pack boundary |
| 2026-09-23 | 02 | Content | Changed the backup instruction to copy the Pictures\MyGallery folder, not the files inside it | QA finding C7 | AI guides/MyGallery/Documents/User Manual/Logs/MyGallery User Manual v1.0 draft 01 - qa-report.md, finding C7; config.py:26-29 |
| 2026-09-23 | 02 | Content | Reframed Controlled folder access as the condition to check, rather than asserting the reader's machine state as fact | QA finding C8 | AI guides/MyGallery/Documents/User Manual/Logs/MyGallery User Manual v1.0 draft 01 - qa-report.md, finding C8; open-questions.md Q1 |
| 2026-09-23 | 02 | Content | Made the two upload-refusal results observable: a new Thumbnail card appears in the Gallery, instead of asserting the file is accepted | QA finding C9 | AI guides/MyGallery/Documents/User Manual/Logs/MyGallery User Manual v1.0 draft 01 - qa-report.md, finding C9; gal.yaml REQ-GAL-009 c6, REQ-GAL-010 |
| 2026-09-23 | 02 | Content | Added a one-line chapter opener, about the subject, to chapters 10 to 14 | QA finding S2 | AI guides/MyGallery/Documents/User Manual/Logs/MyGallery User Manual v1.0 draft 01 - qa-report.md, finding S2 |
| 2026-09-23 | 02 | Content | Folded topic 13.2 into 13.1, renumbered the topics after it, and kept its title as a symptom-index row pointing to 13.1 | QA finding S4 | AI guides/MyGallery/Documents/User Manual/Logs/MyGallery User Manual v1.0 draft 01 - qa-report.md, finding S4 |
| 2026-09-23 | 02 | Content | Cut the paragraph in the not-a-supported-image-type topic that restated 12.1 in full, leaving the link | QA finding S5 | AI guides/MyGallery/Documents/User Manual/Logs/MyGallery User Manual v1.0 draft 01 - qa-report.md, finding S5; manual topic 12.1 |
| 2026-09-23 | 02 | Content | Removed the Gallery-could-not-be-read topic as a separate heading and kept it as a symptom-index row pointing to the Controlled-folder-access topic, until Q3 answers | QA finding S6 | AI guides/MyGallery/Documents/User Manual/Logs/MyGallery User Manual v1.0 draft 01 - qa-report.md, finding S6; open-questions.md Q3 |
| 2026-09-23 | 02 | Content | Cut the repeated one-Upload-carries-up-to-30-files clause from topic 13.1 | QA finding S11 | AI guides/MyGallery/Documents/User Manual/Logs/MyGallery User Manual v1.0 draft 01 - qa-report.md, finding S11; manual topic 7.1 |
| 2026-09-23 | 02 | Content | Replaced the one-column accepted-image-format table with a sentence | QA finding S13 | AI guides/MyGallery/Documents/User Manual/Logs/MyGallery User Manual v1.0 draft 01 - qa-report.md, finding S13 |
| 2026-09-23 | 02 | Content | Led topic 3.1 with a sentence stating the requirements, instead of pre-announcing the table | QA finding T2 | AI guides/MyGallery/Documents/User Manual/Logs/MyGallery User Manual v1.0 draft 01 - qa-report.md, finding T2 |
| 2026-09-23 | 02 | Content | Reframed the glossary's closing sentence as a statement about the named controls | QA finding T5 | AI guides/MyGallery/Documents/User Manual/Logs/MyGallery User Manual v1.0 draft 01 - qa-report.md, finding T5 |
| 2026-09-23 | 02 | Content | Standardised on 'your web browser' in the remaining stray reference to 'the browser' | QA finding T13 | AI guides/MyGallery/Documents/User Manual/Logs/MyGallery User Manual v1.0 draft 01 - qa-report.md, finding T13 |
| 2026-09-23 | 02 | Content | Split the three long sentences flagged by the lint report: the accepted-format sentence in 12.1, and the refusal-reason sentence now in 13.2. The third, in the former 13.2, was removed by the S4 fold | QA finding T10; lint report INFO voice | AI guides/MyGallery/Documents/User Manual/Logs/MyGallery User Manual v1.0 draft 01 - lint-report.md, lines 615, 697, 702 |
| 2026-09-23 | 02 | Content | Changed the Install Python result to the observable installer success message, instead of asserting Python is installed | QA finding P4 | AI guides/MyGallery/Documents/User Manual/Logs/MyGallery User Manual v1.0 draft 01 - qa-report.md, finding P4 |
| 2026-09-23 | 02 | Content | Cut the lifecycle-trailer clause from the chapter 5 opener | Lint WARN, voice: lifecycle trailer | Draft 02 lint report, manual_lint.py voice category |
| 2026-09-23 | 02 | Content | Renumbered topic 6.2 What a Thumbnail card shows to 6.1, with its contents entry and links, after 6.1 was folded into the chapter 6 heading | QA finding S3 follow-through: chapter 6 had a 6.2 with no 6.1 | Manual draft 02, chapter 6 heading list |

## Product versions described

| Document version | Product version | Note |
| --- | --- | --- |
