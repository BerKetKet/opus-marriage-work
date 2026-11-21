# Known Issues & Defect Tracker (`TODO_ISSUES.md`)

**Date**: 2026-11-21  
**Device**: Samsung Galaxy M30 (`SM-M305F`), TrebleDroid GSI Android 13 (`arm64-v8a`, 1080x2340 @ 420 dpi)  
**Reporting Workflow**: Antigravity Worker AI $\leftrightarrow$ Claude Manager & Quality Control AI  

---

## Issue 001: Non-Immersive Fullscreen in Reading Mode (System Bars Visible / Content Pushed Down)

- **Status**: **PARTLY** (cover page proven; middle-page proof pending T1)
- **Resolution**:
  - Implemented `WindowCompat.setDecorFitsSystemWindows(window, false)` and `WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES` in `MainActivity.kt`.
  - Configured transparent status and navigation bars during reading mode in `ReaderScreen.kt`.
  - Applied `statusBarsPadding()` and `navigationBarsPadding()` to chrome overlay and top-level navigation screens (`HomeScreen`, `LibraryScreen`, `MoreScreen`).
  - **Empirical Verification on Physical Device**:
    - Black bar at $y = 0..83\text{ px}$ completely eliminated.
    - Page 1 cover margin measured at: top 360 px, bottom 361 px (perfect vertical symmetry).
    - Verified on both `kindle_exam_v3.epub` (`t2_page1_edge_to_edge.png`) and `kindle_exam_v2.epub` (`t2_second_book_page1.png`).
- **Paired Screenshots**:
  - Our App Cover: `t2_page1_edge_to_edge.png`
  - Real Kindle Cover: `issue_002_kindle_cover_fullscreen_ref.png`
  - Real Kindle Reading Page with Layout Bounds: `issue_001_kindle_page_margins_bounds.png`
- **User Description**:
  > "i have enabled layout bounds to be shown in dev settings... that is a page in the real app. and notice the status bar is hidden and the top of the screen is considered part of the reading page which is why the bottom and top marigins are symmetrical. unlike ours which even while hiding the status bar , shifts lower and displays a black bar where the status bar would have been. this is issue 1"
- **Defect Summary**:
  - In Kindle, reading mode is true edge-to-edge fullscreen extending to the very top edge ($y = 0$). The top of the screen is part of the reading page viewport, yielding vertically symmetrical top and bottom margins.
  - In Opus Reader, even when the system bars were set to hidden, the viewport was shifted downward and left an unrendered black bar in place of the status bar, breaking margin symmetry and pushing the cover page and text downward.

---

## Issue 002: Page Flip Carousel Differences (Cannot Scroll, Page Sizing & Excessive Vertical Spacing)

- **Status**: **OPEN** (Prioritized for instructions 003)
- **Survey Reference**: `K130` (`wireframes/K130.svg`, `wireframes/K130.md`, `tokens.md`)
- **Key Findings from Survey**:
  - Kindle card dimensions: Central card 722 x 1497 px (275 x 570 dp, aspect ~0.482).
  - Left & Right peek cards: 179 px visible slice, 40% scrim.
  - "Back to X" floating pill affordance at `[40, 1867][213, 1963]` restoring previous position.
  - Continuous horizontal drag and snapping physics.
- **Paired Screenshots**:
  - Real Kindle Reference: `issue_002_kindle_page_flip_carousel.png`
  - Our App (Chrome Active / Page Flip): `issue_002_our_app_chrome_page_bounds.png`
- **User Description**:
  > "look now, kindle when touching the middle of a book reading panel, displays the "pages" side by side which you can smoothly scroll sideways"
  > "look now at ours. you cant scroll and the page sizes ... and that ever present layout issue ..."
- **Defect Summary**:
  - **Cannot Scroll**: In Kindle, the horizontal page carousel can be dragged and smoothly scrolled sideways to browse pages. In Opus Reader, the side-by-side preview is completely static and cannot be scrolled or paged horizontally.
  - **Page Card Sizing**: In our app, the central card and adjacent thumbnail cards have incorrect sizing and aspect ratio constraints compared to the book's native geometry, making the text look disproportionate.
  - **Layout & Vertical Inset Waste**: In our app, there is massive dead vertical space between the top bar, the floating chapter title ("E01 The Ferryman's Almanac"), the carousel cards, the location label, and the bottom scrubber bar. Combined with the status bar inset issue, the layout feels uncalibrated and disjointed.

---

## Issue 003: Unresponsive Top Action Buttons & Visual Divergence from Kindle UI

- **Status**: **PARTIALLY RESOLVED / DIAGNOSED** (Commit `0f7146b`, Task T1)
- **Diagnosis & Fix Details**:
  - **Birds-Eye Thumbnails Button**: Was dead due to Z-order touch event consumption by Scrubber Box covering `x = 0..137 px`. Fixed by reordering button above slider in `OpusReaderBottomBar.kt`. Verified working on device (`t1_tap_thumbnails_fixed.png`).
  - **Display Settings (Aa)**: Probed and confirmed working on device (`t1_tap_aa.png`, `t3_settings_sheet_font_tab.png`).
  - **TOC, Search, Notebook, Bookmark**: Probed with real `uiautomator` bounds and verified working (`t1_tap_contents.png`, `t1_tap_search.png`, `t1_tap_notebook.png`, `t1_tap_bookmark.png`).
  - **Overflow (3-dots)**: Tapping dispatches `ActiveReaderSheet.OVERFLOW`, but no composable side sheet menu exists in `ReaderScreen.kt`. Documented as missing design to be implemented based on Kindle `K112` survey.

---

## Issue 004: Text-Size Reflow Latency (~7.1s on Physical Device)

- **Status**: **LOGGED** (Do not fix in 002; optimization pending)
- **Measured Numbers**:
  - `kindle_exam_v3.epub` font size change from Normal (42px) to Small (34px) took **7,133 ms** to reflow all 85 pages.
  - Subsequent single-page render time: **296.37 ms**.
  - Logcat evidence: `D NativeReaderEngine: Reflowed book to geometry 0 in 7133 ms, locator=Locator(spineIndex=2, charOffset=1178) preserved; page 2 rendered in 296.37 ms`.
- **Screenshot Evidence**: `t3_reflow_before_normal.png`, `t3_reflow_after_small.png`.
- **Defect Summary**:
  - Changing font size triggers full-book reflow synchronously or blocks the reader UI thread for 7+ seconds on arm64 hardware, causing an unresponsiveness hiccup before the updated page renders.

---

## Issue 005: Thumbnails Grid Overlay Displays Only 2 Pages for an 85-Page Book

- **Status**: **DIAGNOSED / LOGGED** (Root cause identified; do not fix in 002)
- **Measured Numbers**:
  - Book `kindle_exam_v3.epub` has 85 pages on physical device.
  - Opening the Birds-Eye Thumbnails sheet renders only 2 page thumbnail cards.
- **Screenshot Evidence**: `t1_tap_thumbnails_fixed.png`.
- **Root Cause Analysis**:
  - In `opus-reader/app/src/main/java/app/opusreader/feature/reader/ReaderScreen.kt:675-679`, the invocation of `ReaderThumbnailsGrid` is hardcoded as:
    ```kotlin
    ReaderThumbnailsGrid(
        pages = listOfNotNull(
            engine.previous(uiState.currentPage ?: ...),
            uiState.currentPage,
            engine.next(uiState.currentPage ?: ...)
        ),
        ...
    )
    ```
  - When the user is on page 1 (cover), `engine.previous(...)` returns `null`, resulting in a list of exactly 2 pages (`currentPage` and `next`). On middle pages, it produces at most 3 pages.
  - This is not a lazy-loading failure or a display cap: the caller in `ReaderScreen.kt` literally passes a 3-element adjacent slice rather than a book-wide thumbnail sequence.

---

## Issue 006: Display Settings (Aa) Sheet Tab Parity (2 Tabs vs Kindle 4 Tabs)

- **Status**: **LOGGED** (Design gap; planned for instructions 003)
- **Measured Numbers**:
  - Opus Reader Aa sheet has 2 tabs: "Font" and "Themes" (height: 380 dp).
  - Official Kindle Aa sheet has 4 tabs: "Font", "Layout", "Themes", "More" (height: 400 dp / 1045 px, `[0, 1295][1080, 2340]`).
- **Screenshot Evidence**: `t3_settings_sheet_font_tab.png` vs Kindle `K120.png`, `K121.png`, `K122.png`.
- **Defect Summary**:
  - Missing Layout tab (margins, alignment, line spacing, reading ruler) and More tab (reading progress options, clock toggle).

---

## Issue 007: Reader Top Bar Height Divergence (160 px vs Kindle 168 px)

- **Status**: **LOGGED** (Visual token adjustment)
- **Measured Numbers**:
  - Opus Reader top bar height: 160 px (61 dp) excluding system status bar padding.
  - Kindle top bar height: 168 px (64 dp) at bounds `[0, 83][1080, 251]` (with toolbar parent `[0, 83][1080, 419]` including title subtitle container).
- **Screenshot Evidence**: `t1_opus_chrome_shown.png` vs Kindle `K110.png`.
- **Defect Summary**:
  - Minor 8 px vertical difference in top bar icon container height.
