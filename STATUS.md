# Session Status (`STATUS.md`)

## 1. Capability Tiers Detected in Sandbox
- **Rust Tier**: **Tier E1** (No `rustc` / `cargo` installed in sandbox VM; outbound internet disabled). Applied Fallback E1 (`tools/check_rust_imports.py`, `tools/port_audit.py`, `tools/const_audit.py`, `tools/test_epub_robustness.py`).
- **Python Oracle Tier**: **Tier P-a** (Full Python `3.11.2`, `libfreetype.so.6.18.3`, `libharfbuzz.so.0.60000.0` `6.0.0`, fingerprint `0a54d71bb5a5988b99f67f4281f2ff9d339c91c8324fc6496a50d77ebf952e3d`).
- **Kotlin / Android Tier**: **Fallback K-c** (`python3 tools/guard.py .` $\to$ `GUARD OK` + `tools/kotlin_compile_review.py` static AST/import/contract audit across 19 Kotlin files and 9 behavioral simulation suites).

## 2. Stage Completion Matrix (`S0..S10`)

| Stage | Description | Status | Verification Evidence |
|---|---|---|---|
| **S0** | Recon, Environment Probe & Local Python Oracle (`P0`) | **COMPLETED** | `RECON.md`, `P0` double-render `314/314` pages deterministic (`100%`) |
| **S1** | Contract (`ENGINE_CONTRACT.md`) & Reference Exporter (`P0b`) | **COMPLETED** | `export_reference.py`: `321` pages, `40,644` words, `0` violations (**PASS**) |
| **S2** | App-Side Kotlin Plumbing (`NativeReaderEngine`, `ReplayNativeBridge`, D1..D6) | **COMPLETED** | `guard.py` $\to$ `GUARD OK`; `kotlin_compile_review.py` $\to$ `19` files, `0` errors (**PASS**) |
| **S3** | Rust Workspace Skeleton (`kr-core`, `kr-cli`, `kr-jni`) & Dependency Graph | **COMPLETED** | `check_rust_imports.py` $\to$ `14` files, `0` errors (**PASS**) |
| **S4** | IR (`ir.rs`) & Canonical JSON / SHA-256 (`P1` code + CLI) | **COMPLETED** | `ir.rs` (`22/22` symbols ported); `P1` binary execution: `NOT RUN: no rustc in sandbox` |
| **S5** | Rasterizer (`raster.rs` + `ft_ffi`) (`P2` code + CLI) | **COMPLETED** | `raster.rs` (`25/25` symbols ported); `P2` binary execution: `NOT RUN: no rustc in sandbox` |
| **S6** | Text Layer (`text_layer.rs`) & Wire Format v1 (`page_model.rs`) (`P3` code + CLI) | **COMPLETED** | `text_layer.rs` (`7/7` symbols) + `page_model.rs`; `P3` binary execution: `NOT RUN: no rustc in sandbox` |
| **S7** | Layout, Shaping & Hyphenation (`layout.rs`, `page.rs`, `fonts.rs`, `hyphen.rs`) (`P4`) | **COMPLETED** | `layout.rs` (`16/16`), `page.rs` (`25/25`), `fonts.rs` (`27/27`), `hyphen.rs` (`8/8`) ported |
| **S8** | EPUB + CSS + HTML + Tables + Lists + Images (`epub.rs`) & Robustness (`P5`, `P6`) | **COMPLETED** | `epub.rs` (`13/13` symbols ported); `test_epub_robustness.py` `6/6` static guards (**PASS**) |
| **S9** | JNI Bridge (`kr-jni/src/lib.rs`) & Android Build Docs (`P7`) | **COMPLETED** | `14/14` JNI entry points with `catch_unwind`; `BUILD_ANDROID.md`, `BUILD_ON_HOST.md` |
| **S10** | Adversarial Self-Review (`REVIEW.md`), Manifest & Final Packaging | **COMPLETED** | `opus_rust_marriage_output.zip` verified `< 20 MB`, zero proprietary fonts/hyphen tables |

## 3. Missing Input Items Handled via Fallbacks
- `master_probe_v1.epub` (`probe` corpus in `tools/profiles.json`): Not included in `engine_bundle.zip` or `engine_bundle_full.zip`. Recorded as `NOT RUN: master_probe_v1.epub not supplied in uploaded bundles`.
- `NotoSansCJK-Regular.otf` and `NotoColorEmoji.ttf`: Deliberately omitted from `engine_bundle.zip` per Section 2. `Config::resolve_font_path` and `Family::special_face` degrade gracefully to `Bookerly-Regular.ttf` without panicking. Pages using those fonts (`exam1` p.50–51, `exam2` p.42) are recorded in `missing_font_pages` and reported separately.
