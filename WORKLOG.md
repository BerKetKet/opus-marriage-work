# WORKLOG (`WORKLOG.md`)

## A0. Orientation
- **Date/Time**: 2026-11-18 12:33
- **Rollback commits**:
  - `render.engine`: git initialized, baseline commit created (`547d019`).
  - `opus-reader`: git initialized, baseline commit created (`883bfca`).
- **Environment Probes**:
  - `docker`: `Docker version 29.9.3, build 5457199aa5`
  - `docker image kr-parity`: present (`58979c423d69`, 2.56GB)
  - `cargo`: `1.98.0`
  - `rustc`: `1.98.0`
  - `rustup targets`: `aarch64-linux-android`, `x86_64-unknown-linux-gnu`
  - `java`: `openjdk 21.0.13.0.3`
  - `ANDROID_HOME`: `/opt/android-sdk`
  - `ANDROID_NDK_HOME`: `/opt/android-ndk` (NDK r30)
  - `adb devices`: `[REDACTED_DEVICE_SERIAL] device` (connected Samsung Galaxy M32)
  - `sdkmanager`: `/opt/android-sdk/cmdline-tools/latest/bin/sdkmanager`
  - `cargo-ndk`: not installed
- **Status**: Completed A0. Moving to A1.

## A1. Container Loop and Baseline
- **Tool**: `tools/run_in_container.sh` with named volumes `kr-target`, `kr-cargo`, `kr-ref`.
- **Cargo Build**: `cargo build --manifest-path rust/Cargo.toml --release` inside `kr-parity` succeeded (48.84s, 0 errors).
- **Cargo Test**: `cargo test --manifest-path rust/Cargo.toml --release` inside `kr-parity`: 4 unit tests PASS (3 in `math_py`, 1 in `kr-jni`).
- **Gate P-base** (against legacy `tools/golden/*.json`):
  - `probe`: NOT RUN: epub master_probe_v1.epub not found
  - `exam1`: layout 1/70, pixels 60/70 (85.7%)
  - `exam2`: layout 1/65, pixels 32/65 (49.2%)
  - `exam3_normal`: layout 0/82, pixels 71/82 (86.6%)
  - `exam3_small`: layout 0/54, pixels 44/54 (81.5%)
  - `tables_images`: layout 0/44, pixels 24/44 (54.5%)
  - Total: layout 2/315 (0.6%), pixels 231/315 (73.3%).

## A2. Oracle Truth (Gate P0)
- **Dependency fix**: `lxml` installed in `kr-parity` Docker image (committed) to enable `BeautifulSoup(..., 'xml')` in `epub.py:203` (Decision D9).
- **Reference export**: `python3 tools/export_reference.py --scratch-dir /work/ref` exported 321 pages, 40,644 words, 0 violations (**PASS** on Gate P0b).
- **Gate P0** (Python v1.11.0 in `kr-parity` vs legacy `tools/golden/*.json`):
  - `exam1`: pixels 69/70 (p51 CJK/emoji fallback), layout 50/70
  - `exam2`: pixels 39/65, layout 39/65 (CJK font fallback)
  - `exam3_normal`: pixels 81/82 (p1 cover scaling drift v1.10.1 -> v1.10.2), layout 81/82
  - `exam3_small`: pixels 53/54 (p1 cover scaling drift v1.10.1 -> v1.10.2), layout 53/54
  - `tables_images`: pixels 44/44 (100%), layout 44/44 (100%)
  - Total: pixels 286/315 (90.8%), layout 267/315 (84.8%).
- **Local goldens**: Generated `tools/golden_local/<corpus>.json` for all 5 corpora.
- **Parity check vs golden_local**:
  - `exam1`: layout 1/70, pixels 61/70 (87.1%)
  - `exam2`: layout 1/64, pixels 51/64 (79.7%)
  - `exam3_normal`: layout 1/82, pixels 72/82 (87.8%)
  - `exam3_small`: layout 1/54, pixels 45/54 (83.3%)
  - `tables_images`: layout 0/44, pixels 24/44 (54.5%)
  - Total pixels: 253/314 (80.6%).

## A3. Parity Ladder (Gates P1, P2, P3)
- **Gate P1 (Canonical IR Round-Trip)**:
  - Command: `python3 tools/gate_p1_roundtrip.py --ref-dir /work/ref`
  - Result: **314/314 (100.0%) PASS** (byte-for-byte canonical JSON & layout SHA-256 match across all 5 corpora).
- **Gate P2 (Standalone Rasterizer)**:
  - Fixed TrueType post format 3.0 tilde split in `kr-core/src/raster.rs` using cmap Unicode glyph resolution.
  - Added reference image dumps in `tools/dump_reference_images.py`.
  - Command: `python3 tools/gate_p2_raster.py --ref-dir /work/ref --images-dir /work/ref/images`
  - Result: **314/314 (100.0%) PASS** (pixel-for-pixel bit-identical RGB SHA-256 across all 5 corpora).
- **Gate P3 (Text Layer & Page Model)**:
  - Added directory loading and TSV dump to `kr-cli page-model`.
  - Command: `python3 tools/gate_p3_pagemodel.py --ref-dir /work/ref`
  - Result: **314/314 (100.0%) PASS** (byte-for-byte identical Wire Format v1 page models across all 5 corpora).

## A4. Robustness & Fuzzing (Gate P6)
- **Clippy Static Analysis**:
  - Command: `cargo clippy --all-targets -- -D warnings`
  - Result: 0 warnings, 0 errors (**PASS**).
- **Static Robustness Guards**:
  - Command: `python3 tools/test_epub_robustness.py`
  - Result: 8/8 cases handled without crash (**PASS**).
- **EPUB Mutation Fuzzing**:
  - Tool: `render.engine/tools/fuzz_epub.py` running 500 mutation iterations against `kr-cli fuzz-epub`.
  - Command: `python3 tools/fuzz_epub.py`
  - Result: `iterations=500 ok=1 handled_errors=499 crashes=0 status=PASS`.

## A5. Kotlin JVM Verification (Gate K1)
- **Test Fix**:
  - Fixed unmocked `android.graphics.RectF.toString()` evaluation in assertion string interpolation in `NativeReaderEngineTest.kt:83`.
- **Command**:
  - `cd opus-reader && ./gradlew :engine:testDebugUnitTest :app:testDebugUnitTest :app:assembleDebug`
- **Result**:
  - 47/47 tests passed (33 engine + 14 app, 0 failures, 0 errors).
  - APK built successfully: `app/build/outputs/apk/debug/app-debug.apk` (21 MB).

## A6. Android Native Compilation (Gate N1)
- **Tooling**:
  - Installed `cargo-ndk` v4.1.2.
  - Scripted `render.engine/rust/build_native_deps.sh` to compile static `libfreetype.a` (2.12.1) and `libharfbuzz.a` (6.0.0) with NDK r30 Clang for `arm64-v8a`.
  - Configured `render.engine/rust/kr-jni/build.rs` to statically link FreeType, HarfBuzz, and NDK `libc++_static.a` + `libc++abi.a`.
- **Compilation**:
  - `cargo ndk -t arm64-v8a -P 26 -o opus-reader/engine/src/main/jniLibs build --release -p kr-jni`
- **Verification**:
  - `readelf -d` confirms `DT_NEEDED` contains only `libdl.so, libm.so, libc.so` (zero external dependencies).
  - `nm -D` confirms all 13 JNI entrypoints match `JniNativeBridge.kt`.
  - Size: 4.1 MB (`libkindle_render_jni.so`).

## A7. On-Device Verification (Gates D1 & D2)
- **Target Device**: Physical Samsung Galaxy M32 (`[REDACTED_DEVICE_SERIAL]`), Android 13, arm64-v8a.
- **Gate D1 (On-Device Parity & Benchmarks)**:
  - Bundled font assets in `androidTest` sourceSets in `engine/build.gradle.kts`.
  - Added on-device benchmark test to `NativeReaderEngineParityTest.kt`.
  - Command: `./gradlew :engine:connectedDebugAndroidTest`
  - Result: 5/5 tests passed on device.
  - `renderPage0_matchesPythonEngineGoldenSha256OnDevice` PASSED: bit-identical RGBA hash `fb86f3b3046789ef695d72c7e7dff5dc942de2d1f7e2bf78511384422006a49c`.
  - Device latencies measured via logcat:
    - `open = 915.78 ms`
    - `model = 0.03 ms`
    - `render_p50 = 7.36 ms`
    - `render_p95 = 142.25 ms`
- **Gate D2 (On-Device Fallback)**:
  - Removed `libkindle_render_jni.so` from APK, installed on device, launched `app.opusreader`.
  - Verified app booted cleanly without crashes (pid 25137), `selectReaderEngine` selected `FakeReaderEngine`.
  - Restored `.so` and verified normal native operation.

## A8. Final Artifacts & Deliverables
- **Patches**:
  - `deliverables/render.engine.patch` (107 KB, `git diff baseline`).
  - `deliverables/opus-reader.patch` (8.5 KB, `git diff baseline`).
- **Binary**:
  - `deliverables/jniLibs/arm64-v8a/libkindle_render_jni.so` (4.1 MB).
- **Documentation**:
  - `VERIFICATION_LEDGER.md` (all gates with verbatim printed outputs).
  - `REVIEW.md` (code review and architectural risk analysis).
  - `DECISIONS.md` (decisions D1-D11 logged with empirical rationale).
  - `MERGE_MANIFEST.md` (manifest of changes and application steps).
  - `FINAL_REPORT.md` (comprehensive final report).

## D0. Orientation & Baseline Check
- Probes confirmed: Galaxy M30 (`SM-M305F`) on adb, Java 21, Gradle 8.7, clean git working trees.
- Tagged `diag-baseline` in `render.engine` (`76447a0`) and `opus-reader` (`a956e59`).
- Checked assets and libraries: `libkindle_render_jni.so` (4.1 MB) present; 12 fonts and 15 hyphenation tables present.

## D1. Diagnostics Collection
- Built and installed fresh APK: `BUILD SUCCESSFUL`, `Performing Streamed Install`, `Success`.
- Ran unit tests and guard: 47/47 JVM unit tests pass; `tools/guard.py .` -> `GUARD OK`.
- Systematically navigated through all reachable screens: D01 (Library Grid), D02 (Home), D03 (More), D05 (Filter Sheet), D06 (View & Sort), D07 (Library List), D08 (Collections), D10 (Reader Chrome), D11 (Contents/TOC), D12 (In-book Search), D13 (Annotations), D14 (Annotations Filter), D15 (Annotations Sort), D16 (Annotations Export). Captured screenshots in `deliverables/diag/` and logs in `logs/`.
- Root cause identified: No intent filter or file picker exists to import real EPUB files; seeded books in database use mock paths (`/books/...`), which cause `engine.open` to fail, rendering a blank canvas. Display settings (D17–D20) and Overflow menu have no UI handlers in `ReaderScreen.kt`. Documented in `DIAGNOSIS.md`.


## D0. Diagnostic Orientation
- **Date/Time**: 2026-11-18 22:35
- **Device Probed**: Samsung Galaxy M30 / M32 (`SM-M305F`, Android 13, `arm64-v8a`, 1080x2340 @ 420 dpi, density 2.625).
- **Baseline Git Tags**:
  - `render.engine`: Tagged `diag-baseline` at commit `76447a0`.
  - `opus-reader`: Tagged `diag-baseline` at commit `a956e59`.
- **Assets & Libraries**: `libkindle_render_jni.so` (4.1 MB) present; 12 fonts in `assets/fonts/`; 15 hyphenation tables in `assets/hyphen/`.

## D1. Diagnostic Collection Across Reachable Screens
- **Tested Screens**: Captured screenshots and logs for D01-D16 in `deliverables/diag/` and `logs/`.
- **Key Discovery**:
  - Tapping books from Library rendered a solid black screen because seeded books had simulated file paths (`/books/...`), causing `engine.open` to fail.
  - Display settings ("Aa") and reader overflow menu composables are unbuilt (S07 and S08/S09).
  - `AndroidEngineAssets.kt` searched `"hyph/"` instead of `"hyphen/"`.

## D2. Real EPUB Ingestion & Display on Phone
- **Test Book**: `kindle_exam_v3.epub` (57 KB, 15 spines, 14 TOC entries).
- **Fixes Applied**:
  - Added `opus://open` intent-filter to `AndroidManifest.xml`.
  - Implemented real EPUB stream copy and import in `DebugFixtureController.kt` and `MainActivity.kt`.
  - Fixed `AndroidEngineAssets.kt` candidate paths to include `"hyphen/$lang.bin"`.
  - Fixed `ReaderViewModel.kt` to reset `activeSheet = null` and `isChromeVisible = false` on `loadBook`.
  - Wrapped `android.util.Log` calls in `try/catch` in `ReaderViewModel.kt` to prevent unmocked JUnit crashes.
- **Verification on Device**:
  - EPUB imported cleanly into `/data/user/0/app.opusreader/files/epubs/kindle-exam-v3.epub`.
  - App selected `NativeReaderEngine` (`kindle_render_jni selfTest PASSED`).
  - Page 1 rendered cleanly: `18_exam3_page1.png` ("KINDLE RENDER EXAM").
  - Middle page rendered cleanly: `19_exam3_page_middle.png` (anti-aliased Bookerly prose).
  - Last page rendered cleanly: `20_exam3_page_last.png` (terminal spine item `x4_lines_bolditalic`).
  - Forward and backward page turns verified (30 forward: avg 364 ms/turn; 30 backward: avg 327 ms/turn).
  - TOC opened and displayed 14 chapters: `21_exam3_toc.png`.
  - Chapter jump to "E03 Long Words and Names" verified: `22_exam3_chapter_jump.png`.
  - Memory: Total PSS 795 MB (Native Heap 567 MB, Java Heap 41 MB).

## D3. Final Verification & Documentation
- **Guard**: `python3 tools/guard.py .` -> **GUARD OK**.
- **Unit Tests**: 48/48 tests PASS across `:app`, `:data`, `:design`, `:engine`.
- **Documentation**: Generated `DIAGNOSIS.md`, `deliverables/diag/INDEX.md`, `OWNER_GUIDE.md`.
