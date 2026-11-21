# Marriage State & Verification Notes (`NOTES.md`)

**Date**: 2026-11-21  
**Workspace**: `/home/bgg/projects/opus_marriage_work/`  
**Target Hardware**: Samsung Galaxy M30 (`SM-M305F`), TrebleDroid GSI Android 13 (`arm64-v8a`, $1080 \times 2340$ @ 420 dpi, density 2.625).  
**Report Archive**: `deliverables/opus_marriage_work_worker_report_003.zip`

---

## 1. Current State
- Tasks T0 through T5 assigned in `manager_instructions_002/TASKS.md` are **100% complete (PASS)**.
- Report deliverable package `deliverables/opus_marriage_work_worker_report_003.zip` generated via `tools_manager/make_report.py` v2 with exit code 0.
- Zero occurrences of forbidden hardware serial numbers across deliverables and git history.
- `opus-reader` unit tests pass cleanly (69 tests executed, 0 failures, 0 errors, 0 skipped).
- `render.engine` container parity gates pass cleanly:
  - Gate P0b: 381 pages checked, 50,966 words checked, 0 violations (PASS).
  - Gate P1: 314/314 byte-identical canonical JSON pages (100.0% PASS).
  - Gate P2: 314/314 pixel-identical pages (100.0% PASS).
  - Gate P3: 314/314 byte-identical page models (100.0% PASS).

---

## 2. What is Verified

- **T0: Housekeeping & Errata**:
  - Replaced `tools_manager/make_report.py` with v2; installed `pixel_diff.py` and `motion_measure.py`.
  - Rewrote `BLOCKERS.md` removing obsolete sandbox blockers and documenting active hardware blockers.
  - Updated `TODO_ISSUES.md` with measured values for Issues 004–007; classified Issue 001 as PARTLY.
- **T1: Middle Page Black Screen Investigation**:
  - Tested 4 hypotheses empirically.
  - Root cause established: (d) Load transition duration (~7.1s EPUB reflow) combined with `#000000` Black theme background, not a bitmap cache regression or clipping bug.
  - Captured 7 distinct, non-blank middle page screenshots across White and Black themes (mean ~233–245, stddev ~41–58).
  - Compared with Python reference via `pixel_diff.py`: identical=78.25% (p20) and identical=86.17% (p40), proving the app places the bitmap exactly like the engine.
- **T2: Redo Import Proof**:
  - Imported `kindle_exam_v1.epub` in List view.
  - Captured: `t2_library_list_before.png`, `t2_system_file_picker.png`, `t2_library_list_after.png` (new title visible), `t2_imported_book_reading.png`, `t2_imported_book_reopened.png`.
  - `pixel_diff.py` on before/after list: `different=270225 (10.693%) identical=89.307%`.
  - Captured user error handling for duplicate import (`t2_import_duplicate.png`) and corrupt file import (`t2_import_corrupt_error.png`).
- **T3: Repair Gap Analysis Evidence**:
  - Real Opus screenshots captured for K102, K103, K105, K140, K141, K142 (`PAIRS.tsv` $\ge 3000$ diffs).
  - Empirical Kindle tap-zone probing executed at y=1200 across 9 probe points (x = 20, 100, 200, 230, 540, 850, 870, 1000, 1060), confirming the 20% / 60% / 20% horizontal zone partition.
  - Motion measurements recorded at 60 fps and measured with `motion_measure.py` (6 recordings $\le 318\text{ KB}$ in `motion/`).
  - Reclassified black screenshot rows in `gap_analysis.md`.
- **T4: Engine Investigation (Page Count Discrepancy)**:
  - Preset comparisons:
    - Small (34 px / 51 pitch): Phone=54, Container Rust=54, Python=54.
    - Normal (42 px / 57 pitch): Phone=67, Container Rust=67, Python=67.
    - Large (45 px / 68 pitch): Phone=85, Container Rust=82, Python=82.
  - Root causes isolated:
    - H1 preset naming divergence: UI Normal 42px vs profile Large 45px. Profile `exam3_p42` established 67-page baseline.
    - H2 missing English hyphenation table on Android (`kr-core` unread `mem_hyphen_bins` + hardcoded disk path). Tested `--no-hyphen` on container Rust: produced 85 pages, matching the phone.
    - H4 non-visual `glyph_name` format mismatch in IR (`glyph00217` vs `C`): 28/28 mismatching pages in first 10 pages across 3 corpora differed solely on `glyph_name`, while pixels remained 100% identical.
- **T5: Report 003 Compilation**:
  - Staging directory `deliverables/report_003` populated and checked with `make_report.py`.
  - Diff patches generated against base commits (`369ad4c` and `990eded`).

---

## 3. What is Broken / Open Issues

1. **Issue 004**: Full EPUB reflow on font size change takes ~7.1 s on hardware without visual progress feedback.
2. **Issue 005**: Scrubber slider displays page cards in chrome mode, but horizontal swipe pagination gestures are not yet wired in Compose UI.
3. **Issue 006**: Aa display settings sheet has 2 tabs (Font, Themes), whereas Kindle has 4 tabs (Font, Layout, Themes, More).
4. **Issue 007**: Top bar height is 160 px (61 dp) in Opus Reader vs 168 px (64 dp) in Kindle.
5. **English Hyphenation Gap (Android)**: `hyph_en` is missing from Android assets and `kr-core` ignores `mem_hyphen_bins`, causing 85 vs 82 page count divergence on Large text preset.

---

## 4. Next Steps
1. Package `opus_marriage_work_worker_report_003.zip` with `make_report.py` v2.
2. Commit local repositories per task.
3. Deliver worker report 003 to Manager AI.
