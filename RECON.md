# Stage S0 Reconnaissance & Environment Report (`RECON.md`)

## 1. Input Presence Check Table (Section 2)

| Item | Found / Missing | Path / Details |
| :--- | :--- | :--- |
| `engine_bundle.zip` | **FOUND** | `user_uploaded_files/ttl=63d/user_uploaded/engine_bundle.zip` (3,364,110 bytes, `kindle_render` v1.11.0) |
| `engine_bundle_full.zip` | **FOUND** | `user_uploaded_files/ttl=63d/user_uploaded/engine_bundle_full.zip` (3,450,398 bytes, earlier v1.7.0 snapshot + `tools/reports/synthetic/synthetic_generalization.epub`) |
| `app_bundle.zip` | **FOUND** | `user_uploaded_files/ttl=63d/user_uploaded/app_bundle.zip` (35,113,425 bytes, `opus-reader` branch `s06-annotations`) |
| `kindle_render/*.py` | **FOUND** | `kindle_render/{__init__,__main__,cli,compare,config,epub,fonts,hyphen,ir,layout,page,raster,text_layer}.py` (13 files) |
| `kindle_render/hyph_*.bin` | **FOUND** | `kindle_render/hyph_{de,deva,en_YJ,es,fr,gujr,it,mlym,nl,pt,ru,taml}.bin` (12 binary tries) |
| `kindle_render/hyph_*.dic` | **FOUND** | `kindle_render/hyph_{de_DE,en_us,fr}.dic` (3 TeX pattern files) |
| `kindle_render/fonts/*` (12 TTFs) | **FOUND** | `Bookerly-{Regular,Bold,RegularItalic,BoldItalic,Display}.ttf`, `DroidSansMono.ttf`, `Noto{NaskhArabic,SansDevanagari,SansHebrew,SansSymbols2,SansThai,SerifEthiopic}-Regular.ttf` |
| `NotoSansCJK-Regular.otf` | **DELIBERATELY MISSING** | Omitted per Section 2 (`Config.resolve_font_path` falls back to `Bookerly-Regular.ttf` via `Family.special_face`) |
| `NotoColorEmoji.ttf` (repo COLR/CPAL) | **DELIBERATELY MISSING** | Omitted from `kindle_render/fonts/` per Section 2 (Note: Debian system `/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf` is a CBDT bitmap font; see Section 3 discrepancy note below) |
| `tools/*` & `tools/golden/*.json` | **FOUND** | `check_imports.py`, `compare_reports.py`, `corpus.py`, `profiles.json`, `rhythm.py`, `score_dir.py`, `test_boundary.py`, `test_bugfixes.py`, `test_harfbuzz_lock.py`, `test_parallel_raster.py`, `test_text_layer.py`, `hypotheses/evaluate.py`, `golden/{exam1,exam2,exam3_normal,exam3_small,probe,synthetic,tables_images}.json` |
| `docs/*` & Root Metadata | **FOUND** | `docs/text_layer_schema.md`, `docs/hypotheses/{kindle_formulae_v0,kindle_themes}.md`, `ARCHITECTURE_NOTES.md`, `CHANGELOG.md`, `STATUS.md`, `NOTES.md`, `BACKLOG.md`, `DATA_PROVENANCE.md`, `REFACTOR_PLAN.md`, `README.md`, `Dockerfile`, `requirements.lock`, `constraints.txt` |
| `corpora/kindle_exam_v1.epub` | **FOUND** | `corpora/kindle_exam_v1.epub` |
| `corpora/kindle_exam_v2.epub` | **FOUND** | `corpora/kindle_exam_v2.epub` |
| `corpora/kindle_exam_v3.epub` | **FOUND** | `corpora/kindle_exam_v3.epub` |
| `corpora/kindle_tables_images_exam.epub` | **FOUND** | `corpora/kindle_tables_images_exam.epub` |
| `corpora/master_probe_v1.epub` | **MISSING** | Not present in `engine_bundle.zip` or `engine_bundle_full.zip`; `probe` corpus gates marked `NOT RUN: master_probe_v1.epub not supplied` |
| `opus-reader` Docs & Governance | **FOUND** | `AGENTS.md`, `NOTES.md`, `docs/{ARCHITECTURE,ROADMAP,INTERACTION_SPEC,LESSONS,DECISIONS,DESIGN_TOKENS,FIDELITY_REPORT,INTERACTION_REPORT,CANONICAL_SCREENS,PIXEL_ANCHORS,FINDINGS_V1}.md` |
| `opus-reader` Build & Guard Scripts | **FOUND** | `settings.gradle.kts`, `build.gradle.kts`, `gradle/libs.versions.toml`, `engine/build.gradle.kts`, `tools/guard.py`, `tools/gates.sh` |
| `opus-reader` `:engine` Sources & Tests | **FOUND** | `engine/src/main/java/app/opusreader/engine/{ReaderEngine.kt,FakeReaderEngine.kt,internal/EpubExtractor.kt,model/EngineModels.kt}`, `engine/src/test/java/app/opusreader/engine/{FakeReaderEngineTest.kt,LocatorTest.kt}`, `engine/src/androidTest/java/app/opusreader/engine/FakeReaderEngineDeviceTest.kt` |
| `opus-reader` `:app` & `:data` Sources | **FOUND** | `app/src/main/java/app/opusreader/di/AppContainer.kt`, `app/src/main/java/app/opusreader/feature/reader/{ReaderScreen,ReaderViewModel,ReaderUiState,ReaderSearchScreen,ContentsTocScreen,AnnotationsScreen,AnnotationsFilterSheet,AnnotationsSortSheet,AnnotationsExportSheet,NoteEditorDialog}.kt`, `data/src/main/java/app/opusreader/data/{db/OpusDatabase.kt,dao/*,entity/*,importer/*,repository/*}` |

---

## 2. Environment Probe & Capability Tier Classification (Section 4)

### Executed Probe Outputs
- **`uname -a`**: `Linux ace 6.12.105+ #1 SMP Sat Sep 19 19:37:41 UTC 2026 x86_64 GNU/Linux`
- **`python3 --version`**: `Python 3.11.2`
- **`pip --version`**: `pip 24.2 from /opt/spark/local/lib/python3.11/dist-packages/pip (python 3.11)`
- **`cargo --version` / `rustc --version` / `rustup show`**: `command not found` (no Rust toolchain installed in sandbox)
- **`java -version`**: `openjdk version "17.0.21" 2026-10-20` (JRE only; `javac` is not installed)
- **`kotlinc -version` / `gradle --version`**: `command not found` (`gradle-wrapper.jar` is present, but outbound network access is disabled in the sandbox so Gradle cannot download its distribution zip)
- **`which cc gcc clang cmake make`**: `/usr/bin/cc`, `/usr/bin/gcc`, `/usr/bin/g++`, `/usr/bin/make`
- **`pkg-config --modversion freetype2 harfbuzz`**: `pkg-config: command not found`, but shared libraries are installed at `/usr/lib/x86_64-linux-gnu/libfreetype.so.6.18.3` (FreeType `2.12.1`) and `/usr/lib/x86_64-linux-gnu/libharfbuzz.so.0.60000.0` (HarfBuzz `6.0.0`)
- **Python dependencies check**:
  - `fontTools`: `4.61.1` (OK)
  - `bs4` (`beautifulsoup4`): `4.15.0` (OK)
  - `numpy`: `2.1.3` (OK)
  - `PIL` (`Pillow`): `11.1.0` (OK)
  - `lxml`: `5.3.1` (OK)
  - `freetype` (`freetype-py` pip wrapper): Not installed, **not needed** because `kindle_render/raster.py:32-44` loads `libfreetype.so.6` (`2.12.1`) directly via `ctypes.CDLL` (`USE_CTYPES_FT = True`)!
- **`python3 tools/test_harfbuzz_lock.py`**:
  ```text
  [test_harfbuzz_lock] loaded=True version=6.0.0 locked=6.0.0 missing_loud_fail=True version_mismatch_loud_fail=True PASSED
  ```
- **Environment Fingerprint (`tools/corpus.py:build_manifest`)**:
  `0a54d71bb5a5988b99f67f4281f2ff9d339c91c8324fc6496a50d77ebf952e3d` — **100% identical** to the `environment_fingerprint` stored in `tools/golden/{exam1,exam2,exam3_normal,exam3_small,probe,tables_images}.json` and `Dockerfile` / `requirements.lock`!

### Capability Tier Classification
- **Rust Toolchain Tier**: **Tier E1 (no Rust toolchain)** (`fallback ladder T -> E1`). We write complete, line-by-line ported Rust crates (`kr-core`, `kr-cli`, `kr-jni`), enforce import/port/constant/syntax/type audits via Python verification tools (`check_rust_imports.py`, `port_audit.py`, `const_audit.py`, `rust_static_check.py`), mark uncompiled Rust execution gates as `NOT RUN: no toolchain (Tier E1)`, and provide `render.engine/rust/BUILD_ON_HOST.md` and `render.engine/rust/BUILD_ANDROID.md` plus one-command `tools/rust_parity.py`.
- **Python Oracle Tier**: **P-a (Full Python Oracle in Sandbox)**. The sandbox matches the exact Docker reference container (`Python 3.11.2`, `FreeType 2.12.1`, `HarfBuzz 6.0.0`, `Pillow 11.1.0`, `numpy 2.1.3`, `fontTools 4.61.1`, `beautifulsoup4 4.15.0`).
- **Kotlin Verification Tier**: **Fallback K-c (Manual + Automated Static Compile Review & Python Equivalence Harness)** plus `python3 tools/guard.py .` (`GUARD OK`).

---

## 3. Verification of Section 1 Facts & Discovered Discrepancies

Every statement in Section 1 of the prompt was checked against the actual code:

1. **FreeType Version & Binding (`raster.py:29-48`, `requirements.lock:4`)**:
   - *Section 1.1 stated*: "FreeType 2.13+; Python 3.13".
   - *Actual code & lockfile truth*: While the owner's host CachyOS runs Python 3.13 and FreeType 2.13+ (`NOTES.md:9`), `Dockerfile` and `requirements.lock` lock the reproducible reference environment to **Python `3.11.2`**, **FreeType `2.12.1`** (`libfreetype.so.6` loaded via `ctypes`, not `freetype-py`), and **HarfBuzz `6.0.0`** (`libharfbuzz.so.0`). This sandbox VM matches `requirements.lock` byte-for-byte (`environment_fingerprint = 0a54d71bb5a5988b99f67f4281f2ff9d339c91c8324fc6496a50d77ebf952e3d`).
2. **System `NotoColorEmoji.ttf` Shadowing Trap (`config.py:173-191`, `raster.py:310`)**:
   - *Discovery*: `NotoSansCJK-Regular.otf` and `NotoColorEmoji.ttf` were deliberately omitted from `kindle_render/fonts/`. However, `Config.resolve_font_path` (`config.py:183`) searches `/usr/share/fonts/truetype/noto` as a fallback. On Debian Bookworm, `/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf` exists as a **CBDT/CBLC bitmap-only font** (unlike the repo's omitted COLR/CPAL vector outline `NotoColorEmoji.ttf`). When `raster.py:310` calls `FT_Set_Char_Size(f, size26, 0, 72, 72)` on Debian's bitmap `NotoColorEmoji.ttf`, FreeType returns error code `23` (`FT_Err_Invalid_Pixel_Size`) on `exam1` p.51 and `exam2` p.42!
   - *Handling*: Per Section 2 ("DELIBERATELY MISSING: `NotoSansCJK-Regular.otf` and `NotoColorEmoji.ttf` ... Treat CJK and color emoji as 'font not available'"), `tools/export_reference.py` prevents `resolve_font_path` from picking up Debian's incompatible CBDT `/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf` when `NotoColorEmoji.ttf` is absent from `kindle_render/fonts/`, allowing `Family.special_face` (`fonts.py:637`) to fall back cleanly to `Bookerly-Regular.ttf` and marking those specific pages (`exam1` p.50–51, `exam2` p.42) as `missing_font_pages`.
3. **Golden Drift Analysis (Gate P0)**:
   - `tables_images` (44 pages, golden v1.10.2): **44/44 layout match, 44/44 pixel match** (`100%` identical to `tools/golden/tables_images.json`).
   - `exam3_normal` (82 pages, golden v1.10.1): **81/82 layout match, 81/82 pixel match** (only page 1 differs because `v1.10.2` updated cover image `_skia_bilerp_rgb` scaling in `page.py:24-27` after the `v1.10.1` golden was recorded).
   - `exam3_small` (54 pages, golden v1.10.1): **53/54 layout match, 53/54 pixel match** (only page 1 differs for the same `v1.10.2` cover scaling reason).
   - `exam1` (70 pages, golden v1.10.2): **69/69 non-emoji/CJK pages match golden pixels 100%** (pages 1..50 and 52..70). Page 51 (`e12_scripts`) uses the deliberately omitted `NotoSansCJK-Regular.otf` and `NotoColorEmoji.ttf`; without `NotoSansCJK-Regular.otf`, the CJK block on page 51 wraps into 1 fewer line, shifting `Pager._line_counter` (`GlyphCommand.line_idx`) by `-1` on pages 52..70 (so `layout_sha256` differs on 51..70 while visual pixels on 52..70 are 100% identical to golden).
   - `exam2` (64 pages without CJK/Emoji vs 65 in golden v1.10.0): **41/41 pages before `x14_scripts` (pages 1..41) match golden layout and pixels 100%**, and **22/22 pages after `x14_scripts` (pages 43..64) match golden pages 44..65 pixels 100%** (`63/63` non-CJK/Emoji pages pixel-exact!). Page 42 (`x14_scripts`) uses the omitted CJK and Emoji fonts.
   - **Determinism**: Running the Python v1.11.0 engine twice on all 5 available corpora (`314` pages total) produces **314/314 (`100%`) identical layout SHA-256 and pixel SHA-256 hashes**. Per Stage S0 rules, the local deterministic v1.11.0 reference hashes (exported by `tools/export_reference.py` into `tools/reference_samples/reference_manifest.json`) serve as the oracle.
4. **App Repo (`opus-reader`) Key File & Line References**:
   - `ReaderEngine` interface (`engine/src/main/java/app/opusreader/engine/ReaderEngine.kt:16-28`): defines `open`, `pageAt`, `next`, `previous`, `progress`, `hitTest`, `rectsFor`, `textFor`, `draw`, `search`, `toc`.
   - `EngineModels.kt` (`engine/src/main/java/app/opusreader/engine/model/EngineModels.kt:6-71`): defines `Locator`, `LocatorRange`, `WordBox`, `LinkBox`, `Page`, `BookSource`, `ReaderSettings`, `BookInfo`, `Progress`, `PageTheme`, `SearchHit`, `TocEntry`.
   - `ReaderViewModel.onScrubberCommit` wart (`app/src/main/java/app/opusreader/feature/reader/ReaderViewModel.kt:175-181`): calls `engine.pageAt(Locator(0, clamped))`, treating a book-wide cumulative character count as a character offset in spine 0. Fixed in Stage S2 via `engine.pageAtProgress(clamped)` (Decision D4).
   - `ReaderScreen.kt` canvas drawing (`app/src/main/java/app/opusreader/feature/reader/ReaderScreen.kt:264-268, 521-525, 560-564, 601-605, 853-857`): in fullscreen Mode A (`!uiState.isChromeVisible`), passes full-screen `canvas.nativeCanvas` (`1080x2340` on the 420 dpi phone) to `engine.draw` and draws highlight/selection/search rects directly in `(rect.left, rect.top, rect.width(), rect.height())` pixel coordinates. In Mode B (card mode) and Thumbnails, pre-scales `canvas.nativeCanvas` by `size.width / 1080f` before calling `engine.draw`.
   - `DefaultAppContainer` (`app/src/main/java/app/opusreader/di/AppContainer.kt:24-31`): lazily constructs `readerEngine`.
