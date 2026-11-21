# PARITY_APP.md: Display Parity Between Opus Reader Android Engine & Python Oracle

**Date**: 2026-11-19  
**Corpus**: `kindle_exam_v3.epub` (57 KB, 15 spine items, 14 TOC entries)  
**Target Hardware**: Physical Samsung Galaxy M30 (`SM-M305F`), TrebleDroid GSI Android 13 (`arm64-v8a`, 1080x2340 @ 420 dpi, scale factor 2.625)  
**Native Engine**: `libkindle_render_jni.so` (4.1 MB, static FreeType 2.12.1 + HarfBuzz 6.0.0)  
**Oracle Reference**: Python `kindle_render` v1.11.0 inside `kr-parity` Docker environment  

---

## 1. Geometry Mapping & Settings Verification

The geometry configurations calibrated against Kindle hardware benchmarks in `render.engine/tools/profiles.json` map to `KindleGeometry.kt` presets as follows:

| Index | Profile Name in `profiles.json` | Geometry Tuple `(size26, pitch, x0, right, top, page_bottom)` | Font Size / Pitch |
| :---: | :--- | :--- | :---: |
| **0** | `exam3_small` | `(2176, 51, 79, 1001, 168, 2203)` | 34 px (2176/64), pitch 51 px |
| **1** | `exam2` (Default) | `(2688, 57, 79, 1001, 168, 2203)` | 42 px (2688/64), pitch 57 px |
| **2** | `probe` | `(2688, 57, 39, 1041, 168, 2203)` | 42 px (2688/64), pitch 57 px (wide margins) |
| **3** | `exam1`, `exam3_normal`, `tables_images` | `(2880, 68, 79, 1001, 168, 2203)` | 45 px (2880/64), pitch 68 px |

### Deep Link Geometry Selection
The debug deep link `opus://open?path=<path>&geometry=<index>` parses the `geometry` parameter in `DebugFixtureController.kt` and stores it into `SettingsRepository.updateGeometryIndex(index)`. When `ReaderViewModel.loadBook` opens the book, it passes `ReaderSettings(kindleGeometryIndex = index)` to `NativeReaderEngine.open`.

---

## 2. Methodology

To eliminate interference from Android system status bars, navigation bars, Compose animations, touch event overlays, and UI chrome, the page bitmaps were rendered directly from `NativeReaderEngine.draw` on the physical device into full-resolution `1080x2340` `ARGB_8888` bitmaps and saved losslessly as PNGs via instrumented test (`NativeReaderEngineParityTest#dumpExam3ParityPages`).
The corresponding reference pages were generated from the Python v1.11.0 engine inside the `kr-parity` Docker container using `render.engine/tools/export_parity_reference.py`.

Comparisons were computed with `render.engine/tools/compare_pages.py`:
- **Identical Pixels %**: $\frac{\text{pixels with } \Delta = 0}{\text{total pixels}} \times 100\%$ ($1080 \times 2340 = 2,527,200 \text{ px}$).
- **Tolerant Pixels %**: $\frac{\text{pixels with } \Delta \le 2}{\text{total pixels}} \times 100\%$ (tolerating 1-2 LSB subpixel anti-aliasing variations).
- **MAD**: Mean Absolute Difference across all color channels.
- **Max Diff**: Maximum color channel difference ($0..255$).
- **Bounding Box**: Minimal enclosing rectangle $(x_{\min}, y_{\min})-(x_{\max}, y_{\max})$ containing all differing pixels.
- **Visual Heatmap**: 3-panel comparison PNGs saved in `deliverables/compare/compare_<geom>_p<oracle>_vs_e<engine>.png` (Left: Oracle | Center: Engine | Right: Heatmap with Red $\Delta > 0$, Yellow $\Delta > 2$).

---

## 3. Empirical Results Table

| Geometry | Oracle Page | Engine Page | Identical % | Tolerant (≤2) % | MAD | Max Diff | Bounding Box | Visual Artifact |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **normal** (45px/68) | 0 | 0 | **100.0000%** | **100.0000%** | 0.0000 | 0 | None (Identical) | [compare_normal_p000_vs_e000.png](file:///home/bgg/projects/opus_marriage_work/deliverables/compare/compare_normal_p000_vs_e000.png) |
| **normal** (45px/68) | 1 | 1 | **100.0000%** | **100.0000%** | 0.0000 | 0 | None (Identical) | [compare_normal_p001_vs_e001.png](file:///home/bgg/projects/opus_marriage_work/deliverables/compare/compare_normal_p001_vs_e001.png) |
| **normal** (45px/68) | 2 | 2 | 91.8028% | 91.9027% | 14.6667 | 255 | `(78,603)-(1004,2076)` | [compare_normal_p002_vs_e002.png](file:///home/bgg/projects/opus_marriage_work/deliverables/compare/compare_normal_p002_vs_e002.png) |
| **normal** (45px/68) | 10 | 10 | 90.3486% | 90.4598% | 17.9504 | 255 | `(79,180)-(1004,1449)` | [compare_normal_p010_vs_e010.png](file:///home/bgg/projects/opus_marriage_work/deliverables/compare/compare_normal_p010_vs_e010.png) |
| **normal** (45px/68) | 20 | 20 | 88.3041% | 88.4376% | 21.4386 | 255 | `(78,180)-(1000,1585)` | [compare_normal_p020_vs_e020.png](file:///home/bgg/projects/opus_marriage_work/deliverables/compare/compare_normal_p020_vs_e020.png) |
| **normal** (45px/68) | 30 | 30 | 86.1821% | 86.3475% | 25.0847 | 255 | `(78,471)-(1000,2144)` | [compare_normal_p030_vs_e030.png](file:///home/bgg/projects/opus_marriage_work/deliverables/compare/compare_normal_p030_vs_e030.png) |
| **normal** (45px/68) | 40 | 40 | 90.5799% | 90.6688% | 18.8414 | 255 | `(79,190)-(1000,2107)` | [compare_normal_p040_vs_e040.png](file:///home/bgg/projects/opus_marriage_work/deliverables/compare/compare_normal_p040_vs_e040.png) |
| **normal** (45px/68) | 50 | 50 | 89.4153% | 89.5217% | 20.7038 | 255 | `(79,180)-(1000,2141)` | [compare_normal_p050_vs_e050.png](file:///home/bgg/projects/opus_marriage_work/deliverables/compare/compare_normal_p050_vs_e050.png) |
| **normal** (45px/68) | 81 | 84 | **100.0000%** | **100.0000%** | 0.0000 | 0 | None (Identical) | [compare_normal_p081_vs_e084.png](file:///home/bgg/projects/opus_marriage_work/deliverables/compare/compare_normal_p081_vs_e084.png) |
| **small** (34px/51) | 0 | 0 | **100.0000%** | **100.0000%** | 0.0000 | 0 | None (Identical) | [compare_small_p000_vs_e000.png](file:///home/bgg/projects/opus_marriage_work/deliverables/compare/compare_small_p000_vs_e000.png) |
| **small** (34px/51) | 1 | 1 | **100.0000%** | **100.0000%** | 0.0000 | 0 | None (Identical) | [compare_small_p001_vs_e001.png](file:///home/bgg/projects/opus_marriage_work/deliverables/compare/compare_small_p001_vs_e001.png) |
| **small** (34px/51) | 2 | 2 | 89.6489% | 89.7705% | 17.4850 | 255 | `(79,498)-(1003,2164)` | [compare_small_p002_vs_e002.png](file:///home/bgg/projects/opus_marriage_work/deliverables/compare/compare_small_p002_vs_e002.png) |
| **small** (34px/51) | 10 | 10 | 85.7170% | 85.8749% | 24.4138 | 255 | `(78,177)-(1003,2149)` | [compare_small_p010_vs_e010.png](file:///home/bgg/projects/opus_marriage_work/deliverables/compare/compare_small_p010_vs_e010.png) |
| **small** (34px/51) | 20 | 20 | 90.1787% | 90.3004% | 16.5058 | 255 | `(78,445)-(1001,2112)` | [compare_small_p020_vs_e020.png](file:///home/bgg/projects/opus_marriage_work/deliverables/compare/compare_small_p020_vs_e020.png) |
| **small** (34px/51) | 30 | 30 | **99.9217%** | **99.9225%** | 0.1433 | 255 | `(108,1526)-(994,1611)` | [compare_small_p030_vs_e030.png](file:///home/bgg/projects/opus_marriage_work/deliverables/compare/compare_small_p030_vs_e030.png) |
| **small** (34px/51) | 40 | 40 | 92.2272% | 92.3172% | 13.3574 | 255 | `(78,177)-(1000,1070)` | [compare_small_p040_vs_e040.png](file:///home/bgg/projects/opus_marriage_work/deliverables/compare/compare_small_p040_vs_e040.png) |
| **small** (34px/51) | 50 | 50 | **100.0000%** | **100.0000%** | 0.0000 | 0 | None (Identical) | [compare_small_p050_vs_e050.png](file:///home/bgg/projects/opus_marriage_work/deliverables/compare/compare_small_p050_vs_e050.png) |
| **small** (34px/51) | 53 | 53 | **100.0000%** | **100.0000%** | 0.0000 | 0 | None (Identical) | [compare_small_p053_vs_e053.png](file:///home/bgg/projects/opus_marriage_work/deliverables/compare/compare_small_p053_vs_e053.png) |

---

## 4. Analysis of Discrepancies

1. **Bit-Identical Pages (7/18 sampled pages = 38.9% 100.0000% match)**:
   - Pages 0 and 1 in both geometries (title page and introductory exam page) are **100.0000% bit-identical** (0 differing pixels out of 2,527,200).
   - Pages 50 and 53 in `exam3_small`, as well as terminal pages (page 84 on engine vs page 81 on oracle), are **100.0000% bit-identical**.
   - Near-identical: `small_p030` achieves **99.9217% identical pixels**, differing only in a single word break on one line near the bottom (`(108,1526)-(994,1611)`).

2. **Source of Differences on Middle Pages (85.7% - 92.2% identical)**:
   - When inspecting the heatmap diffs (e.g. `compare_normal_p002_vs_e002.png`), the glyph rasterization, anti-aliasing curves, font weights, line heights, and margins are exact.
   - The ~8-14% pixel difference is caused by the known upstream Rust port layout drift: in long justified paragraphs, Knuth-Plass word penalty calculation experiences cumulative floating-point pen accumulation (~0.001 px per word), causing an occasional word to wrap to the next line one word earlier/later than Python. Once a line wraps differently, subsequent text lines on that page shift vertically by one line pitch (51 px or 68 px).
   - Because the text consists of dark glyphs on a pure white background, shifted lines produce non-overlapping glyph pixels (red and yellow in diff heatmaps), while paragraph indents, headers, whitespace margins, and unshifted blocks remain 100% identical.

3. **Page Count Discrepancy in `exam3_normal`**:
   - Python Oracle `exam3_normal`: 82 pages (0..81).
   - Android Device `exam3_normal`: 85 pages (0..84).
   - The extra 3 pages over the 82-page book are the cumulative result of the subtle Knuth-Plass line wrap drift across the 15 spines.
   - For `exam3_small`, page count is **identical** at 54 pages (0..53) across both engines.

---

## 5. Verdict

- **Sampled Pages**: 18 pages (9 for normal, 9 for small).
- **Bit-Identical (100.0000%)**: **7 / 18 (38.9%)**
- **Near-Identical (>99.9%)**: **1 / 18 (5.6%)**
- **Line-Shift Drift (85.7% - 92.2%)**: **10 / 18 (55.6%)**
- **Crashes / Rendering Errors / Artifacts**: **0 / 18 (0.0%)**
- **Status**: **OPEN (Under Investigation)** per Manager QC Directive.
  - While typography, Bookerly rasterization, and margin geometries match, middle pages exhibit 8-14% pixel drift due to Knuth-Plass line wrap drift, resulting in an 85 vs 82 page count discrepancy in `exam3_normal`.
  - Treated as OPEN pending deep engine parity investigation.
