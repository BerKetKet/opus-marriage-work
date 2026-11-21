# What report 003 must contain

Built with `python3 tools_manager/make_report.py --n 003 --staging deliverables/report_003 --forbid <device serial>`; it must exit 0. About 25 MB maximum; split as `_003a`, `_003b` if needed.

1. `REPORT.md`: first the verdict per task T0-T5 (PASS / FAIL / NOT RUN: reason) with the key facts (max 5 lines each), then "Errata to report 002", then details, then "What I could not verify and why".
2. `screenshots/`: every image listed in `DESCRIPTIONS.tsv`; `PAIRS.tsv` for every before/after claim; no black or blank image unless described as `EXPECTED-BLANK:`.
3. `specs/kindle_survey/`: updated (`gap_analysis.md`, `interactions.md`, `tokens.md`, `motion/` if any).
4. `ENGINE_INVESTIGATION.md` with its tables and the raw data files it is based on (per-page hash files for the phone, the container Rust, the Python reference, as text/TSV, not images).
5. `test_reports/`: fresh unit-test XML and a counts file computed from the XML; the container Rust tests/gates if you changed Rust.
6. `patches/`: `git_state.txt` (made by the script) plus `opus-reader.diff` and `render.engine.diff`: text diffs from the last commit included in report 002 to HEAD (state both hashes in `REPORT.md`).
7. `docs/`: `TODO_ISSUES.md`, `DECISIONS.md` (new only), `BLOCKERS.md` (rewritten).

Never include fonts, hyphenation tables, `.so`, `.a`, APKs, zips, build output, the device serial, personal Kindle account details.
