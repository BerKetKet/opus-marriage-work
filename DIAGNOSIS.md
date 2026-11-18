# Diagnostic Report (`DIAGNOSIS.md`)

**Date**: 2026-11-18  
**Scope**: Comprehensive diagnosis of the Opus Reader Android application UI state and getting ONE EPUB (`kindle_exam_v3.epub`) displaying page by page on the connected phone (`SM-M305F`).

---

## 1. Environment

### Device Info
- **Model / Vendor**: Samsung Galaxy M30 / M32 (`SM-M305F` / `TrebleDroid_with_GApps`, `tdgsi_arm64_ab`)
- **ADB Identifier**: `32001776e8e82623` (`device usb:1-5 product:treble_arm64_bgS model:TrebleDroid_with_GApps device:tdgsi_arm64_ab transport_id:2`)
- **OS & Architecture**: Android 13, `arm64-v8a`
- **Display**: 1080x2340 @ 420 dpi, density 2.625

### Build Toolchain
- **Java**: `openjdk version "21.0.13.0.3" 2026-10-24` (OpenJDK 64-Bit Server VM build 21.0.13.0.3+1)
- **Gradle**: `Gradle 8.7` (Kotlin 1.9.22, Groovy 3.0.17)
- **Host OS**: Linux 7.3.4-1-cachyos amd64

### Repository Status & Baseline Tags
- `render.engine`: on branch `master`, clean, tagged `diag-baseline` at commit `76447a074bccb80e28fc116dc8c92e4dc18021fd`.
- `opus-reader`: on branch `master`, tagged `diag-baseline` at commit `a956e59dec634674fbc34fdf0c1ce099bfb1eefc`.

### ROADMAP Slice Status
- S00 through S06 reports present in `docs/slices/`:
  - `S00_REPORT.md`: Skeleton (4 modules, gates pass, guard OK)
  - `S01_REPORT.md`: Design system components
  - `S02_REPORT.md`: Room schema, data and EPUB import (`EpubParser`, `EpubImporter`)
  - `S03_REPORT.md`: Library (grid, list, view/sort, filter sheets)
  - `S04_REPORT.md`: Engine API, contract tests, FakeReaderEngine
  - `S05_REPORT.md`: Reader chrome, swipe pager, scrubber, contents, bookmarks
  - `S06_REPORT.md`: Selection, annotations, in-book search
  - S07 through S12: Not yet completed.

### Native Libraries & Assets Present
- `opus-reader/engine/src/main/jniLibs/arm64-v8a/libkindle_render_jni.so`: present (4,241,808 bytes, static FreeType 2.12.1 + HarfBuzz 6.0.0).
- `opus-reader/app/src/main/assets/fonts/`: 12 font files present (`Bookerly-BoldItalic.ttf`, `Bookerly-Bold.ttf`, `Bookerly-Display.ttf`, `Bookerly-RegularItalic.ttf`, `Bookerly-Regular.ttf`, `DroidSansMono.ttf`, `NotoNaskhArabic-Regular.ttf`, `NotoSansDevanagari-Regular.ttf`, `NotoSansHebrew-Regular.ttf`, `NotoSansSymbols2-Regular.ttf`, `NotoSansThai-Regular.ttf`, `NotoSerifEthiopic-Regular.ttf`).
- `opus-reader/app/src/main/assets/hyphen/`: 15 hyphenation tables present (`hyph_de.bin`, `hyph_de_DE.dic`, `hyph_deva.bin`, `hyph_en_us.dic`, `hyph_en_YJ.bin`, `hyph_es.bin`, `hyph_fr.bin`, `hyph_fr.dic`, `hyph_gujr.bin`, `hyph_it.bin`, `hyph_mlym.bin`, `hyph_nl.bin`, `hyph_pt.bin`, `hyph_ru.bin`, `hyph_taml.bin`).

### Verified Unit Tests & Guard
- `tools/guard.py .`: **GUARD OK**
- Unit test XML count (`opus-reader/*/build/test-results/testDebugUnitTest/*.xml`):
  - `PageModelCodecTest`: 7 tests, 0 failures, 0 errors
  - `LocatorTest`: 1 test, 0 failures, 0 errors
  - `FakeReaderEngineTest`: 10 tests, 0 failures, 0 errors
  - `NativeReaderEngineTest`: 15 tests, 0 failures, 0 errors
  - `AppUnitTest`: 8 tests, 0 failures, 0 errors
  - `ReaderViewModelTest`: 6 tests, 0 failures, 0 errors
  - `EpubParserTest`: 1 test, 0 failures, 0 errors
  - **TOTAL**: **48 tests, 0 failures, 0 errors, 0 skipped (100% PASS)**

---

## 2. Screen Diagnostics Table (Before & After Stage D2)

| Canonical ID | Screen Name | Initial Status | Final Status | Evidence (Screenshot) | Details |
|---|---|---|---|---|---|
| **D01** | Library grid | **WORKS** | **WORKS** | `deliverables/diag/02_library_grid.png` | Interactive, renders covers and filter/sort actions cleanly. |
| **D02** | Home | **WORKS** | **WORKS** | `deliverables/diag/01_app_start.png` | Renders search pill, "From your Library" carousel, bottom navigation bar. |
| **D03** | More tab | **PARTLY** | **PARTLY** | `deliverables/diag/07_more_screen.png` | Slice S09 pending; shows centered "More" text placeholder (`MoreScreen.kt:15`). |
| **D04** | Settings | **UNREACHABLE** | **UNREACHABLE** | — | Slice S09 pending; not wired in navigation graph (`OpusNavHost.kt:158`). |
| **D05** | Library filter sheet | **WORKS** | **WORKS** | `deliverables/diag/03_library_filter_sheet.png` | Bottom sheet with Read state and Content type chips; interactive. |
| **D06** | Library view & sort | **WORKS** | **WORKS** | `deliverables/diag/04_library_view_sort_sheet.png` | View mode (Grid, List, Collections) and Sort radio items; interactive. |
| **D07** | Library list | **WORKS** | **WORKS** | `deliverables/diag/05_library_list.png` | Vertical list of book titles with overflow options. |
| **D08** | Collections view | **WORKS** | **WORKS** | `deliverables/diag/06_collections_empty.png` | "New Collection" header and collections listing. |
| **D09** | Notifications | **UNREACHABLE** | **UNREACHABLE** | — | Slice S09 pending; no route or trigger in UI. |
| **D10** | Reader (Real EPUB) | **BROKEN** (solid black) | **WORKS** | `deliverables/diag/18_exam3_page1.png`<br>`deliverables/diag/19_exam3_page_middle.png`<br>`deliverables/diag/20_exam3_page_last.png` | Fixed by routing real EPUB import into internal storage and passing valid file path to `NativeReaderEngine`. Real text rendered with anti-aliasing. |
| **D10** | Reader (Fixture) | **WORKS** | **WORKS** | `deliverables/diag/10_fixture_d10.png` | Reader chrome works in fixture mode with mock text. |
| **D11** | Contents (TOC) | **WORKS** | **WORKS** | `deliverables/diag/11_contents_toc.png`<br>`deliverables/diag/21_exam3_toc.png`<br>`deliverables/diag/22_exam3_chapter_jump.png` | Real 14 TOC entries parsed from EPUB; clicking chapter jumps reader directly to chapter. |
| **D12** | In-book search | **WORKS** | **WORKS** | `deliverables/diag/12_reader_search.png` | Search bar, hit navigation and empty states render properly. |
| **D13** | Annotations / Notebook | **WORKS** | **WORKS** | `deliverables/diag/13_annotations.png` | Bookmark/note items list, action buttons, jump to locator. |
| **D14** | Annotations filter | **WORKS** | **WORKS** | `deliverables/diag/14_annotations_filter_sheet.png` | Filter by type (Bookmark, Note, Highlight) and color. |
| **D15** | Annotations sort | **WORKS** | **WORKS** | `deliverables/diag/15_annotations_sort_sheet.png` | Sort by Location, Date created, Date modified. |
| **D16** | Annotations export | **WORKS** | **WORKS** | `deliverables/diag/16_annotations_export_sheet.png` | Share via email, export Markdown, export Plain Text. |
| **D17–D20** | Display Settings | **BROKEN** | **BROKEN** | `deliverables/diag/17_display_settings.png` | Top bar "Aa" button triggers `onOpenSheet(ActiveReaderSheet.SETTINGS)`, but `ReaderScreen.kt` has no UI implementation for `SETTINGS`. Slice S07 unbuilt. |
| — | Reader Overflow | **BROKEN** | **BROKEN** | — | Top bar overflow button triggers `onOpenSheet(ActiveReaderSheet.OVERFLOW)`, but `ReaderScreen.kt` has no UI implementation for `OVERFLOW`. |

---

## 3. Engine Facts & Measurements

### Engine Selection
- **Selected Engine**: `NativeReaderEngine` over `JniNativeBridge`.
- **Logcat Confirmation**: `I AppContainer: Selected NativeReaderEngine (kindle_render_jni selfTest PASSED)`.
- `JniNativeBridge.isAvailable() = true`.
- `JniNativeBridge.selfTest() = true`.
- Fallback to `FakeReaderEngine`: **DID NOT OCCUR**.

### Dynamic Linkage & Memory Footprint
- `libkindle_render_jni.so` (4,241,808 bytes, arm64-v8a) loaded via `System.loadLibrary("kindle_render_jni")`.
- Static link: FreeType 2.12.1 + HarfBuzz 6.0.0 embedded directly inside the `.so`.
- Linked platform libraries: strictly `libdl.so, libm.so, libc.so`.
- Process Memory (`adb shell dumpsys meminfo app.opusreader`):
  - **TOTAL PSS**: `795,250 KB` (~795 MB)
  - **Native Heap**: `567,704 KB` (~567 MB) — driven by the bitmap cache storing 1080x1440 32-bit ARGB bitmaps (~6.2 MB each) for 50+ traversed pages.
  - **Java Heap**: `41,416 KB` (~41 MB).
  - **Graphics**: `28,980 KB` (~29 MB).

### Rendering Performance (Printed Device Measurements)
- **First Page (Page 0) Render**: `174.92 ms` (cache miss).
- **Subsequent Page Cache Misses**: `220.65 ms` to `387.80 ms` (e.g. `Rendered page 46 on cache miss in 387.80 ms`).
- **Cache Hit Latency**: `< 16 ms` (sub-frame Compose redraw; adjacent pages are prefetched in background coroutines).
- **Turn Latency (Automated Stress Test over ADB)**:
  - 30 turns forward: `10,940 ms` total (`364 ms/turn` avg, including ADB command dispatch over USB).
  - 30 turns backward: `9,815 ms` total (`327 ms/turn` avg, including ADB command dispatch over USB).

---

## 4. Ranked List of Remaining Problems

1. **Display Settings sheet (D17–D20) not implemented**:
   - Tapping the "Aa" icon in the reader chrome has no visual effect. S07 implementation needed.
2. **Reader overflow menu not implemented**:
   - Tapping the 3-dots overflow icon in the reader chrome has no visual effect.
3. **No in-app file picker for EPUB import**:
   - Currently, EPUBs must be opened via deep link `opus://open?path=...`. Adding an "Import EPUB" button to `LibraryScreen` will allow users to import files directly from storage.
4. **Bitmap cache eviction policy**:
   - `NativeReaderEngine` retains rendered page bitmaps in a `HashMap`. Adding an LRU cache bounded to ~50 MB (8-10 pages) will reduce native heap usage from 567 MB down to < 100 MB.
5. **More, Settings, and Notifications tabs are stubs**:
   - Slices S08 and S09 need to be completed according to roadmap.
