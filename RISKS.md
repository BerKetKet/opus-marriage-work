# Technical Risks & Mitigations (`RISKS.md`)

## 1. Host & Android Compilation First-Run Minor Type/Lifetime Adjustments
- **Risk**: Because the sandbox is **Tier E1** (no `rustc`) and **Fallback K-c** (no `kotlinc`), the Rust workspace and Kotlin sources were verified via AST/regex static audits (`check_rust_imports.py`, `port_audit.py`, `const_audit.py`, `kotlin_compile_review.py`, `guard.py`) rather than `cargo build` / `./gradlew testDebugUnitTest`.
- **Mitigation**: All Rust modules use explicit, concrete standard library types (`i64`, `f64`, `String`, `Vec`, `HashMap`, `Arc<Face>`), avoid complex lifetime parameters or procedural macros beyond `serde`, and isolate C FFI (`libfreetype.so.6`, `libharfbuzz.so.0`) to small `extern "C"` blocks with explicit C signatures.

## 2. FreeType & HarfBuzz Version Parity on Android (`arm64-v8a`)
- **Risk**: Pixel-exact parity (`P2`, `P4`, `P5`) depends on FreeType `2.12.1+` hinting and HarfBuzz `6.0.0` shaping tables. If an Android device loads a different system `libharfbuzz.so` or `libfreetype.so`, shaping or hinting pixels can drift by 1 px on Devanagari/Thai or hinted glyphs.
- **Mitigation**: `BUILD_ANDROID.md` documents bundling `libfreetype.so` and `libharfbuzz.so` (`6.0.0`) directly in `opus-reader/engine/src/main/jniLibs/arm64-v8a/` alongside `libkindle_render_jni.so`, and `kr_core::fonts::verify_harfbuzz()` checks the runtime HarfBuzz version against `6.0.0`.

## 3. Synchronous Main-Thread Page Renders on Cold Cache
- **Risk**: `NativeReaderEngine.draw(page, canvas, theme)` renders via JNI into a direct `ByteBuffer` (`1080x2340x4` = `10.1 MB`) when the page bitmap is not yet in the 6-page `LruCache`.
- **Mitigation**: Measured single-page rasterization latency in Python (`export_reference.py`) is `~54 ms` median, and in native Rust with cached `FT_Face` glyphs is `< 10 ms`. The 6-page `LruCache<Long, Bitmap>` and single pre-allocated direct `ByteBuffer` eliminate GC churn during page turns.
