# Engine investigation plan: phone vs PC page counts and page contents

Question: the same Rust engine gives 82 pages for `kindle_exam_v3.epub` in the container (and Python gives 82 for the same configuration), but the phone reported 85 pages. Why? Is it a settings difference, a missing asset, a platform math difference, or the known Rust-vs-Python layout gap (about 20% of pages differ end to end)?

Principle: change ONE thing at a time, compare hashes, never explain from guesses. Hypotheses to test, in this order:
- H1 config: the app passes different settings than the container run (size, pitch, margins x0/right, justification, hyphenation, boldness, language).
- H2 assets: on the phone a font or hyphenation table is missing or different (path lookup in `AndroidEngineAssets`, wrong file, fallback to a different font), changing advances or hyphenation.
- H3 platform: same input, same config, but different numeric results (NDK/bionic math or compiler contraction vs glibc).
- H4 core: container Rust itself differs from Python (known: about 80% of pages identical end to end, layout hash anomaly): then the phone is not special and the work is in the Rust layout.

## 1. Define the three presets precisely
For each app preset (Small 34 px, Normal 42 px, Large 45 px) write the exact engine configuration the app sends over JNI (`KindleGeometry.kt`, `NativeReaderEngine.open` settings text): size26, pitch, x0, right, top, page_bottom, justify, hyphenate, boldness, language, any other field. Compare each with the matching entry of `render.engine/tools/profiles.json` (small = `exam3_small`, large = `exam3_normal`; Normal 42 px/57 matches `exam2`/`probe` settings but has NO existing reference for `kindle_exam_v3.epub`).
Create a new profile `exam3_p42` in `profiles.json` (EPUB v3, size26 2688, pitch 57, x0 79, right 1001, same other values as `exam2`), and generate Python references inside the container (`tools/export_reference.py`) so all three presets have a Python reference for the v3 book. Record any field that differs between app and profile: that is H1 evidence.

## 2. Dump what the phone really does (debug-only code, no behaviour change)
Add a debug-only mechanism (debug source set or a debug-gated function) that, for the book open on the phone:
1. writes the effective engine config (all fields) and the asset facts (for each font/hyphenation table the engine loaded: name, bytes, first 12 hex chars of sha256) to `/sdcard/Android/data/app.opusreader/files/engine_dump_<preset>.txt`;
2. writes one line per page: `page<TAB>layout_sha256<TAB>rgb_sha256<TAB>line_count` for ALL pages of the book at that preset (use the same hash definitions as `kr-cli render-book`).
Add the same config printout to `kr-cli render-book` (`--print-config`) so both sides print the same fields. Pull the three phone files with `adb pull`.

## 3. Compare (tables for `ENGINE_INVESTIGATION.md`)
Run in the container (Docker image `kr-parity`, `tools/run_in_container.sh`): Rust `render-book` for the three presets on the v3 book, and the Python references. Then produce, per preset:
| preset | pages phone | pages Rust container | pages Python | first page phone != Rust container | first page Rust container != Python | matching pages phone vs Rust container | matching Rust container vs Python |
Raw per-page files go in the report (TSV).
Interpretation:
- Phone == Rust container for every page: H1, H2, H3 are ruled out; the problem is H4 (shared). Say so.
- Phone != Rust container: find out which. Compare the config dumps (H1), then the asset sha256 values against the files in the container (H2), then, if both are identical, H3: write a small deterministic numeric test (inputs fixed in the code: `py_round` on many halves, floor-division with negatives, float32 sums, any `powf`/`exp`/`ln`/`sqrt` the engine uses) and run it BOTH on the phone (instrumented test or debug entry) and in the container; print the outputs and diff them. Record the first differing value.

## 4. Classify the shared mismatches (H4), time-boxed
For the first 10 mismatching pages (container Rust vs Python) across `exam3_small`, `exam3_normal` and `tables_images`: dump both IRs (`kr-cli layout --dump-ir` if present, otherwise add it; Python IR from `export_reference.py`), print the first differing command and field per page (`tools/ir_diff.py`), and aggregate counts by class: line break position, hyphenation point, justification/spacing value, glyph advance, image size/position, table geometry, page break, non-visual field only (indexes/metadata). The "layout hash differs although the pixels are identical" cases are a class of their own: name the differing field.
Stop after 5 attempts per class and write BLOCKERS entries. Fix only what is proven and small.

## 5. Output
`ENGINE_INVESTIGATION.md`: (a) preset configuration table (app vs profile, differences highlighted); (b) the comparison tables of section 3; (c) the class table of section 4; (d) one root-cause statement per difference with the evidence file name; (e) ranked list of proposed fixes with effort estimates. Raw files (TSV) alongside.
