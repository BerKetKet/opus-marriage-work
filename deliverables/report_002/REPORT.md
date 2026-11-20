# Opus Marriage Work: Worker Report 002

**Author**: Antigravity (Worker AI)  
**Recipient**: Claude (Manager & Quality Control AI)  
**Date**: 2026-11-20  
**Device**: Samsung Galaxy M30 (`SM-M305F`), Android 13 TrebleDroid GSI (`arm64-v8a`, $1080 \times 2340$ @ 420 dpi, density 2.625)  
**Deliverable Archive**: `deliverables/opus_marriage_work_worker_report_002.zip`  
**Git Commits**:
- `opus-reader`: `369ad4c566691502772005bd5a56e13bfa1f3adb`
- `render.engine`: `990eded88ffffea57677cbd6cd5ffc9b5aad1d1f` (clean)
- Top Workspace: `3b9dc9c898543af3554c1d42a69fb40530907a06` (pre-staging commit)

---

## 1. Executive Summary

| Task | Description | Verdict | Evidence |
|---|---|---|---|
| **T0** | Workflow setup & initial Kindle display recording | **PASS** | `tools_manager/` scripts operational; `deliverables/report_002/` staged; `specs/kindle_survey/RESTORE_LOG.md` |
| **T1** | Issue 003: Top/bottom buttons diagnostics & fix | **PASS** | Z-order fix in `OpusReaderBottomBar.kt` (commit `0f7146b`); `t1_tap_thumbnails_fixed.png`, `t1_tap_aa.png` |
| **T2** | Issue 001: True edge-to-edge fullscreen reading mode | **PASS** | `MainActivity.kt` cutout & `ReaderScreen.kt` insets (commit `369ad4c`); `t2_page1_edge_to_edge.png`, `t2_second_book_page1.png` |
| **T3** | Retake missing proof (import, settings, reflow) | **PASS** | System file picker import sequence; 7.1s reflow timing; `t3_library_after_import.png`, `t3_reflow_after_small.png` |
| **T4** | Official Kindle app survey (Tier P1) | **PASS** | 19 captured states; SVGs & element tables in `wireframes/`; `tokens.md`, `interactions.md`, `gap_analysis.md` |
| **T5** | Report 002 compilation & packaging | **PASS** | 69 unit tests passing (0 failures); clean patches; validated via `make_report.py` |

### Key Facts
1. **Edge-to-Edge Margins are Vertically Symmetrical**: By setting `WindowCompat.setDecorFitsSystemWindows(window, false)` and `LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES`, the $y = 0..83\text{ px}$ letterbox is eliminated. Physical measurement on `kindle_exam_v3.epub` page 1 shows top margin = $360\text{ px}$ and bottom margin = $361\text{ px}$, identical to reference layout geometry.
2. **Bottom Bar Thumbnail Button Clickability Resolved**: The 9-dot thumbnail button was dead because the Scrubber slider box was placed later in Compose layout order and consumed touch events across $x = 0..137\text{ px}$. Reordering the button surface on top restored immediate responsiveness.
3. **In-App Import and Reflow Proven on Hardware**: Real in-app import through Android DocumentsUI file picker was driven on the physical device. Font size change (Normal 42px $\rightarrow$ Small 34px) reflowed 85 pages in $7133\text{ ms}$, rendered in $296.37\text{ ms}$, and preserved the exact character locator (`spineIndex=2, charOffset=1178`).
4. **Comprehensive Kindle Tier P1 Survey Landed**: Captured 19 states of the official Kindle app with UI Automator XML hierarchies, SVG wireframes, design tokens (colors, padding, radii), interaction timings, and a full gap analysis against Opus Reader.

### Ranked Remaining Defects
1. **Issue 002: Page-Flip Card Carousel Physics & Layout**: Kindle uses continuous horizontal drag physics with side peek cards ($722 \times 1497\text{ px}$ center card, 179 px peek slices with 40% scrim) and a "Back to Page X" pill. Our carousel is static, cannot be scrolled sideways, and has excessive vertical spacing.
2. **Issue 003b: Missing Overflow Side Sheet Menu**: Tapping the 3-dot button in Opus Reader dispatches `ActiveReaderSheet.OVERFLOW`, but no composable side sheet exists. Kindle uses a 250 dp ($656\text{ px}$) right drawer with About, Go to page, Annotations, and Store.
3. **Paragraph Reflow Line-Wrap Drift**: In `kindle_exam_v3.epub`, Python engine renders 82 pages while Kotlin renderer produces 85 pages due to minor Knuth-Plass hyphenation and font metric variations across platforms.

---

## 2. Task Details & Empirical Evidence

### T0: Workflow Setup
- Tool scripts copied to `/home/bgg/projects/opus_marriage_work/tools_manager/`:
  - `survey_capture.py`: verified operational via `--help`.
  - `xml_to_wireframe.py`: verified operational via `--help`.
  - `make_report.py`: verified operational via `--help`.
- Staging directory created at `deliverables/report_002/`.
- Initial Kindle display settings recorded in `specs/kindle_survey/RESTORE_LOG.md`:
  - Font: Bookerly, Size step 3.
  - Layout: White theme, default margins, portrait lock.
  - Themes: Custom.
  - More: Reading Ruler Off, Assistive Off.

### T1: Issue 003 Diagnostics & Fix (Reader Top/Bottom Bars)
Every control was probed with UI Automator bounds on physical hardware (`kindle_exam_v3.epub`):

| Control | Measured Bounds (px) | Bounds (dp) | Tap Outcome | Code Path | Status |
|---|---|---|---|---|---|
| **Back Arrow** | `[0, 83][126, 209]` | `[0, 31.6][48, 79.6]` | Navigates back to Library | `OpusReaderTopBar.kt:45` | **PASS** (`t1_tap_back.png`) |
| **Contents (TOC)** | `[126, 83][252, 209]` | `[48, 31.6][96, 79.6]` | Opens TOC bottom sheet | `OpusReaderTopBar.kt:53` | **PASS** (`t1_tap_contents.png`) |
| **Search** | `[576, 83][702, 209]` | `[219.4, 31.6][267.4, 79.6]` | Opens Search bottom sheet | `OpusReaderTopBar.kt:61` | **PASS** (`t1_tap_search.png`) |
| **Notebook** | `[702, 83][828, 209]` | `[267.4, 31.6][315.4, 79.6]` | Opens Notebook bottom sheet | `OpusReaderTopBar.kt:69` | **PASS** (`t1_tap_notebook.png`) |
| **Bookmark** | `[828, 83][954, 209]` | `[315.4, 31.6][363.4, 79.6]` | Toggles bookmark state | `OpusReaderTopBar.kt:77` | **PASS** (`t1_tap_bookmark.png`) |
| **Aa Settings** | `[954, 83][1080, 209]` | `[363.4, 31.6][411.4, 79.6]` | Opens Display Settings sheet | `OpusReaderTopBar.kt:85` | **PASS** (`t1_tap_aa.png`) |
| **Overflow (3-dots)** | Top bar right edge | — | Dispatches `OVERFLOW` enum | `ReaderScreen.kt:312` | **MISSING** (No UI composable implemented) |
| **9-Dot Grid** | `[0, 2151][126, 2277]` | `[0, 819.4][48, 867.4]` | Opens Birds-Eye sheet | `OpusReaderBottomBar.kt:78` | **PASS** (Fixed in `0f7146b`, `t1_tap_thumbnails_fixed.png`) |

- **Root Cause & Fix for 9-Dot Button**: The scrubber slider container was laid out after the button and absorbed touch events over the button's bounding box. In `opus-reader/app/src/main/java/app/opusreader/feature/reader/ui/OpusReaderBottomBar.kt`, the thumbnail button `Box` was moved after the slider in layout order, giving it top Z-order.
- **Logcat Evidence**:
  `I ViewRootImpl: ViewPostIme key 0: action=ACTION_DOWN at (63, 2214)`
  `D ReaderViewModel: onAction: OpenThumbnailsSheet`

### T2: Issue 001: True Edge-to-Edge Fullscreen Reading Mode
- **Changes Applied**:
  - `MainActivity.kt`: Configured `WindowCompat.setDecorFitsSystemWindows(window, false)` and `window.attributes.layoutInDisplayCutoutMode = WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES`.
  - `ReaderScreen.kt`: Enabled transparent status bar and transparent navigation bar when chrome is hidden. Wrapped `OpusReaderTopBar` and `OpusReaderBottomBar` in background containers respecting `statusBarsPadding()` and `navigationBarsPadding()` so the overlay never pushes the book canvas.
  - `OpusNavHost.kt`: Applied `statusBarsPadding()` and `navigationBarsPadding()` to top-level app destinations (`HomeScreen`, `LibraryScreen`, `MoreScreen`) and bottom navigation bar.
- **Physical Device Measurements (`kindle_exam_v3.epub`, 1080x2340)**:
  - Top margin from pixel 0 to top edge of cover illustration: **$360\text{ px}$**
  - Bottom margin from bottom edge of cover illustration to pixel 2340: **$361\text{ px}$**
  - Status bar notch area ($y = 0..83\text{ px}$): Zero black bar; book canvas renders directly behind cutout.
  - Chrome overlay: Top bar overlays at $y = 0..209\text{ px}$; bottom bar overlays at $y = 2050..2340\text{ px}$; page canvas position is stationary.
  - Second book verification: Tested on `kindle_exam_v2.epub` (`t2_second_book_page1.png`), measuring identical $360\text{ px}$ symmetric margins.
- **Guard Validation**: `python3 tools/guard.py .` $\rightarrow$ `GUARD OK`. Committed: `369ad4c`.

### T3: Retake Missing Proof (Import, Settings, Reflow)
- **In-App File Picker Import**:
  1. `t3_library_before_import.png`: Library showing existing books.
  2. `t3_system_file_picker.png`: Android system `DocumentsUI` selecting `/sdcard/Download/test_import_v2.epub`.
  3. `t3_library_after_import.png`: Library showing `test_import_v2` tile with "NEW" badge.
  4. `t3_imported_book_reading.png`: Reading view successfully rendering the imported book.
- **Settings Sheet Tabs**:
  - `t3_settings_sheet_font_tab.png`: Font family selection and font size controls.
  - `t3_settings_sheet_themes_tab.png`: Theme presets and layout options.
- **Reflow Verification**:
  - Pre-reflow (Normal 42px): `t3_reflow_before_normal.png` (`spineIndex=2, charOffset=1178`).
  - Post-reflow (Small 34px): `t3_reflow_after_small.png` (`spineIndex=2, charOffset=1178`).
  - **Logcat Timing**: `Reflowed book to geometry 0 in 7133 ms, locator=Locator(spineIndex=2, charOffset=1178) preserved; page 2 rendered in 296.37 ms`.
- **Image Hygiene**: Zero duplicate images, zero blank/near-blank screenshots.

### T4: Official Kindle App Survey (Tier P1)
All 19 states of the P1 Reader workflow were captured, indexed, and analyzed in `specs/kindle_survey/`:

| ID | Title | Key Interaction / Geometry | Wireframe |
|---|---|---|---|
| **K100** | Reading view, chrome hidden | Fullscreen edge-to-edge ($1080 \times 2340$); margins $118\text{ px}$ ($45\text{ dp}$); footer at $y = 2277$ | `wireframes/K100.svg` |
| **K101** | Reading view, chrome shown | Top bar $168\text{ px}$ ($64\text{ dp}$); bottom scrubber $200\text{ px}$ ($76\text{ dp}$) | `wireframes/K101.svg` |
| **K102** | Reader tap zones | Left tap ($x = 0..216$) turns back; Right tap ($x = 324..1080$) turns forward | `wireframes/K102.svg` |
| **K103** | Page turn by swipe | Horizontal swipe drag with fluid page reveal | `wireframes/K103.svg` |
| **K104** | Cover view | Centered cover artwork; symmetrical $360\text{ px}$ top/bottom margins | `wireframes/K104.svg` |
| **K105** | Reading progress footer cycle | Tapping footer cycles: Page in book $\rightarrow$ Loc in book $\rightarrow$ Time left in chapter $\rightarrow$ None | `wireframes/K105.svg` |
| **K110** | Top bar controls | Close, Contents, Search, Annotations, Aa, Export, Overflow | `wireframes/K110.svg` |
| **K111** | Bookmark indicator | Blue ribbon at `[966, 0][1080, 137]` | `wireframes/K111.svg` |
| **K112** | Overflow side sheet | Right slide-in drawer ($656\text{ px}$ / $250\text{ dp}$ width); About, Go to, Annotations, Store | `wireframes/K112.svg` |
| **K120** | Aa Font tab | Font Family selector, 14-step font size slider, bold weight slider | `wireframes/K120.svg` |
| **K121** | Aa Layout tab | Page color themes (White, Sepia, Black), margins (3 steps), line spacing (3 steps) | `wireframes/K121.svg` |
| **K122** | Aa Themes tab | Presets: Compact, Standard, Large, and Custom | `wireframes/K122.svg` |
| **K130** | Page-flip card carousel | Center card $722 \times 1497\text{ px}$; peek cards 179 px; "Back to X" pill | `wireframes/K130.svg` |
| **K131** | 9-dot thumbnail grid | $3 \times 3$ grid of page tiles with bookmark ribbons; bottom page scrubber | `wireframes/K131.svg` |
| **K132** | Table of Contents | Hierarchical chapter list with page locators and current progress marker | `wireframes/K132.svg` |
| **K133** | Notebook annotations list | Filter tabs: All, Bookmarks, Notes, Highlights; export affordance | `wireframes/K133.svg` |
| **K134** | In-book search | Search text field with match frequency count and contextual snippet list | `wireframes/K134.svg` |
| **K140** | Text selection toolbar | Selection handles, floating menu (Copy, Highlight, Note, Share, Search) | `wireframes/K140.svg` |
| **K141** | Highlight palette & note | 4 color swatches (Yellow, Blue, Pink, Orange) and inline note editor | `wireframes/K141.svg` |

- **Restoration Verification**: Kindle settings restored to initial state and verified in `specs/kindle_survey/RESTORE_LOG.md`.

### T5: Deliverables & Report Archive
- **Unit Tests Execution**:
  - Command: `./gradlew test --rerun-tasks`
  - Results: **69 tests executed, 0 failures, 0 errors, 0 skipped**.
  - Test XMLs copied to `deliverables/report_002/test_reports/`.
- **Patches**:
  - `patches/opus-reader.diff`: Git diff `5e757ff..HEAD` capturing T1 and T2 fixes.
  - `patches/render.engine.diff`: Clean (no modifications to python engine per protocol).
  - `patches/git_state.txt`: Full git status, remotes, and log history.
- **Documentation**:
  - `docs/TODO_ISSUES.md`: Issue 001 marked RESOLVED, Issue 003 PARTIALLY RESOLVED, Issue 002 OPEN.
  - `docs/DECISIONS.md`: Decisions D9 (Cutout ShortEdges), D10 (Bottom bar z-order), D11 (Parity status).
  - `docs/BLOCKERS.md`: No blocking items.
  - `docs/PARITY_APP.md`: Verdict maintained as OPEN per manager instruction.

---

## 3. What I Could Not Verify and Why

1. **Offline Dictionary Lookup Card (`K140b`)**: Long-pressing a word opened the text selection toolbar and dictionary card container, but the full dictionary definition card failed to display lexical definitions because no offline dictionary pack was downloaded and the physical test device had no authenticated Amazon account session.
2. **First-Run Coach Marks (`K143`)**: Kindle first-run introductory overlay coach marks (e.g., "Tap here to turn pages", "Tap top for menu") could not be captured because the installed Kindle application version on this device had previously completed its initial onboarding walkthrough.
