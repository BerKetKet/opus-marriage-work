# Marriage State & Verification Notes (`NOTES.md`)

**Date**: 2026-11-20  
**Workspace**: `/home/bgg/projects/opus_marriage_work/`  
**Target Hardware**: Samsung Galaxy M30 (`SM-M305F`), TrebleDroid GSI Android 13 (`arm64-v8a`, $1080 \times 2340$ @ 420 dpi, density 2.625).  
**Report Archive**: `deliverables/opus_marriage_work_worker_report_002.zip` (11.6 MB)

---

## 1. Current State
- Tasks T0 through T5 assigned in `manager_instructions_001/TASKS.md` are **100% complete (PASS)**.
- Report deliverable package `deliverables/opus_marriage_work_worker_report_002.zip` is generated, verified via `tools_manager/make_report.py`, and passes all size, integrity, and privacy checks.
- Zero occurrences of forbidden hardware serial numbers across deliverables and git history.
- `opus-reader` is on branch `master` at commit `369ad4c` with `python3 tools/guard.py .` passing (`GUARD OK`).
- `render.engine` is on branch `master` at commit `990eded` (clean, unedited).

---

## 2. What is Verified
- **T0: Workflow Setup**:
  - `tools_manager/survey_capture.py`, `xml_to_wireframe.py`, `make_report.py` installed and verified.
  - Staging folder `deliverables/report_002/` created and fully populated.
  - Initial Kindle display settings verified and logged in `RESTORE_LOG.md`.
- **T1: Issue 003: Top/Bottom Bar Controls**:
  - All top/bottom buttons probed with real `uiautomator` bounds on hardware.
  - Birds-eye 9-dot thumbnail button fixed by resolving Z-order touch event consumption in `OpusReaderBottomBar.kt` (commit `0f7146b`). Verified responsive on device (`t1_tap_thumbnails_fixed.png`).
  - Aa display settings sheet, TOC, Search, Notebook, and Bookmark verified working on device.
  - Overflow 3-dots diagnosed: dispatches `ActiveReaderSheet.OVERFLOW` without composable side sheet implementation.
- **T2: Issue 001: True Edge-to-Edge Fullscreen Reading Mode**:
  - In `MainActivity.kt`: enabled `WindowCompat.setDecorFitsSystemWindows(window, false)` and `LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES`.
  - In `ReaderScreen.kt`: set transparent system bars in reading mode, wrapped chrome bars with window insets so overlay does not shift page canvas.
  - In `OpusNavHost.kt`: added status/navigation bar insets to top-level app screens.
  - Verified on physical hardware: top margin = 360 px, bottom margin = 361 px (symmetric); black bar at $y = 0..83$ eliminated. Verified on second book (`kindle_exam_v2.epub`). Commit `369ad4c`.
- **T3: Missing Proof (Import, Settings, Reflow)**:
  - In-app import driven through system DocumentsUI file picker: `t3_library_before_import.png`, `t3_system_file_picker.png`, `t3_library_after_import.png` (NEW badge), `t3_imported_book_reading.png`.
  - Settings sheet tabs captured: `t3_settings_sheet_font_tab.png`, `t3_settings_sheet_themes_tab.png`.
  - Reflow test: Normal (42px) $\rightarrow$ Small (34px); locator preserved (`spineIndex=2, charOffset=1178`); reflow timing 7133 ms, render timing 296 ms.
  - All 48 images in staging verified 100% unique (zero duplicate hashes) and non-blank.
- **T4: Official Kindle App Survey (Tier P1)**:
  - 19 states captured (K100-K105, K110-K112, K120-K122, K130-K134, K140-K141).
  - 19 SVG wireframes and element descriptions generated.
  - Design tokens (`tokens.md`), interactions ledger (`interactions.md`), gap analysis (`gap_analysis.md`) complete.
  - Kindle settings restored to initial state and verified in `RESTORE_LOG.md`.
- **T5: Report 002 Compilation**:
  - 69 unit tests passing (0 failures, 0 errors, 0 skipped).
  - Patches generated (`opus-reader.diff`, `render.engine.diff`, `git_state.txt`).
  - Report archive `deliverables/opus_marriage_work_worker_report_002.zip` built cleanly (11.6 MB, 133 files).

---

## 3. What is Broken or Open
- **Issue 002: Page-Flip Card Carousel**:
  - Kindle card carousel uses continuous horizontal drag physics with side peek cards ($722 \times 1497\text{ px}$ center card, 179 px peek slices with 40% scrim) and a "Back to Page X" pill. Our carousel is static, cannot be scrolled sideways, and has excessive vertical spacing.
- **Issue 003b: Missing Overflow Side Sheet Composable**:
  - 3-dot overflow button dispatches `ActiveReaderSheet.OVERFLOW`, but composable side sheet drawer is not yet implemented.
- **Line-Wrap Drift**:
  - 85 pages rendered in Opus Reader vs 82 pages in Python oracle on `kindle_exam_v3.epub` due to minor font metric / hyphenation differences.
- **Offline Dictionary Lookup (`K140b`)**:
  - Unverified due to lack of offline dictionary database and unauthenticated test session.
- **Coach Marks (`K143`)**:
  - Not present / already dismissed in current Kindle installation.

---

## 4. Next Steps
1. Deliver `deliverables/opus_marriage_work_worker_report_002.zip` to Manager AI (Claude).
2. Await Manager AI review and instructions for next batch (Issue 002 Page Flip Carousel implementation and Issue 003b Overflow drawer).
3. Implement continuous horizontal card scrolling in `PageFlipCarousel` matching Kindle `K130` tokens and geometry.
