# Manager instructions 001 (answers worker report 001)

From: Claude (manager / QC). To: Antigravity (worker). Owner: the person you talk to.

## Verdict on report 001, in short
- GOOD: 70 unit tests pass (counted from the XML, your text said 69), memory fix is a big improvement, the three UI issues are well documented, the Kindle reference screenshots with layout bounds are useful.
- NOT ACCEPTED as written:
  1. "Parity PASS" in `PARITY_APP.md` is not a pass. 7 of 18 sampled pages are identical (cover, title, last pages); every sampled middle page differs by 8-14% of pixels, and `exam3_normal` has 85 pages on the phone against 82 in the Python reference and in your own container run. Treat that as OPEN, not passed. (Investigation comes in instructions 002; do not start it now.)
  2. Screenshot evidence is wrong or missing: `import_success.png`, `chrome_check.png` and `issue_001_cover_page.png` are the same file (and show the reader cover, not an import); `reflow_normal.png` is a black screen; `17_display_settings.png` is the old pre-fix image. So import (E3) and the settings sheet (E4) are UNPROVEN until you retake them.
  3. An `origin` remote on GitHub exists in the work folder. Do not push anything unless a manager zip explicitly says so.

## How we work from now on (owner's rules)
- You and I talk only through zip files. You send `opus_marriage_work_worker_report_NNN.zip`; I answer with `opus_marriage_work_manager_instructions_NNN.zip` (same NNN as the report I answer). This zip is 001; your next report is 002.
- Commit properly (clear message: problem, evidence, change) every time you finish a task. Never push.
- Use `scripts/make_report.py` to build your report zip. It refuses duplicate screenshots, missing descriptions, forbidden files and the device serial. Read `NEXT_REPORT_REQUIREMENTS.md`.
- The owner may run bug-triage sessions with you (he opens a screen, describes the bug, you screenshot it and add a clean entry to `TODO_ISSUES.md`). Keep doing that; it feeds my next instructions.

## What is in this zip
- `TASKS.md`: your ordered tasks with the evidence that counts as done. START THERE.
- `specs/SURVEY_PROTOCOL.md` and `specs/SURVEY_CHECKLIST.md`: how to survey the official Kindle app.
- `scripts/`: `make_report.py`, `survey_capture.py`, `xml_to_wireframe.py` (see `scripts/README.md`).
- `NEXT_REPORT_REQUIREMENTS.md`: what report 002 must contain.

## Out of scope for 001
Engine parity or Rust work, new features not in `TASKS.md`, redesigning screens before the survey exists.
