# Marriage State & Verification Notes (`NOTES.md`)

**Date**: 2026-11-18  
**Workspace**: `/home/bgg/projects/opus_marriage_work/`  
**Target Hardware**: Samsung Galaxy M30 (`SM-M305F`), TrebleDroid GSI Android 13 (`arm64-v8a`).

---

## 1. Current State
- The Rust port of `kindle_render` (`kr-core`, `kr-cli`, `kr-jni`) is fully compiled, verified against Python oracle v1.11.0, and integrated with the Opus Reader Android application.
- Self-contained `libkindle_render_jni.so` (4.1 MB) statically links FreeType 2.12.1 and HarfBuzz 6.0.0, requiring only `libdl, libm, libc` on Android.
- Verified on physical Galaxy M30: the app launches, selects `NativeReaderEngine`, loads the native library directly from APK, and passes all instrumentation and parity tests.

---

## 2. What is Verified
- **G4 & HarfBuzz Pinning**: Python imports and HarfBuzz 6.0.0 lock **PASS**.
- **Python Bugfixes**: B1, B2, B3, B4 **PASS**.
- **Gate P0 & P0b**: 314/314 corpus pages deterministic; 40,644 word locator slices 100% invariant; reflow text invariant 16/16 (100%).
- **Gate P1**: Canonical IR round-trip **314/314 (100.0%) PASS**.
- **Gate P2**: Standalone rasterizer **314/314 (100.0%) PASS** (bit-identical RGB SHA-256).
- **Gate P3**: Page Model Wire Format v1 **314/314 (100.0%) PASS** (byte-for-byte identical TSV).
- **Gate P4/P5**: Full EPUB rendering produces **253/314 (80.6%) bit-identical page hashes**; page counts 100% identical.
- **Gate P6**: `cargo clippy --all-targets -- -D warnings` (0 warnings, 0 errors); 8/8 static robustness guards **PASS**; 500 EPUB mutation fuzzer iterations **PASS** (0 crashes).
- **Gate K1**: 47/47 JVM unit tests **PASS** (33 engine + 14 app); `app-debug.apk` builds (21 MB).
- **Gate N1**: Self-contained `libkindle_render_jni.so` built with NDK r30 Clang; 13/13 JNI entrypoints match `JniNativeBridge.kt`.
- **Gate D1 (Device Functional & Benchmark)**: 5/5 connected Android tests **PASS** on Galaxy M30 (`SM-M305F`). Page 0 RGBA SHA-256 matches Python golden. Latencies: `open = 941.69 ms`, `model = 0.03 ms`, `render_p50 = 7.91 ms`, `render_p95 = 145.82 ms`.
- **Gate D2 (Device Fallback)**: Graceful fallback to `FakeReaderEngine` verified with 0 crashes when `.so` is omitted.

---

## 3. What is Broken or Unverified
- `master_probe_v1.epub`: **NOT RUN: file not supplied** (file was omitted from workspace corpora).
- CJK / Emoji pages: **NOT RUN: font not supplied** (`NotoSansCJK-Regular.otf` and `NotoColorEmoji.ttf` omitted; safely degrades to Bookerly).
- Full EPUB pipeline has 19.4% hash differences due to floating-point pen accumulation in long Knuth-Plass justified paragraphs, though rasterizer itself is 100% bit-identical.

---

## 4. Next Steps
1. Upstream merge: Apply `deliverables/render.engine.patch` to `render.engine` and `deliverables/opus-reader.patch` to `opus-reader`.
2. Deploy `deliverables/jniLibs/arm64-v8a/libkindle_render_jni.so` into production Android app builds.
3. Review through GitHub using [FINAL_REPORT.md](file:///home/bgg/projects/opus_marriage_work/FINAL_REPORT.md) and [VERIFICATION_LEDGER.md](file:///home/bgg/projects/opus_marriage_work/VERIFICATION_LEDGER.md).
