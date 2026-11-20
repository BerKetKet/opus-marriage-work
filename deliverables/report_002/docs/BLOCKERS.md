# Environment Blockers & Applied Fallbacks (`BLOCKERS.md`)

## 1. Blocker B1: No Rust Compiler (`rustc` / `cargo`) in Sandbox VM (Tier E1)
- **Symptom**: `which cargo rustc rustup` returned exit code `1` during Stage S0, and outbound network access is disabled inside the sandbox container.
- **Fallback Ladder Applied (Section 9.1 — Tier E1)**:
  1. Wrote the complete, idiomatic Cargo workspace (`render.engine/rust/Cargo.toml`, `kr-core`, `kr-cli`, `kr-jni`) with all `175/175` Python symbols ported and annotated with `// py: <file>:<line>`.
  2. Built and executed automated static verification tools:
     - `tools/check_rust_imports.py` (`G4-rust`): verified `14/14` Rust files obey module dependency rules and isolate `unsafe` strictly inside `hb_ffi` and `ft_ffi`.
     - `tools/port_audit.py`: verified `175/175` (`100.0%`) Python functions, classes, and methods have matching `// py: <file>:<line>` implementations in Rust.
     - `tools/const_audit.py`: verified `85/85` `Config` fields, `20/20` module constants, and `25/25` calibration literals match between Python and Rust.
     - `tools/test_epub_robustness.py`: generated all `8` hostile/malformed EPUB test cases and verified all `6/6` static safety guards.
  3. Marked dynamic binary execution gates `P1..P7` as `NOT RUN: no rustc in sandbox` in `VERIFICATION_LEDGER.md` (Rule R2).

## 2. Blocker B2: No `kotlinc` / `javac` / Android SDK in Sandbox VM (Fallback K-c)
- **Symptom**: `/usr/bin/java` (`OpenJDK 17.0.21` JRE) is installed, but `javac`, `kotlinc`, and the Android SDK are not installed in the container, and Gradle wrapper cannot download dependencies without internet.
- **Fallback Ladder Applied (Section 9.3 — Fallback K-c)**:
  1. Ran `python3 tools/guard.py .` in `opus-reader` $\to$ `GUARD OK`.
  2. Built and ran `python3 tools/kotlin_compile_review.py work/app`, which statically audited all `19` new/modified Kotlin files (balanced braces/parens, package declarations, imports, `:engine` isolation from `:data`, additive-only `ReaderEngine` / `ReaderSettings` / `BookInfo` signatures) and executed `9` behavioral simulation suites against the real Python-exported `.tsv` replay bundles (`7` bundles, `2,963/2,963` reflow words verified).

## 3. Blocker B3: Missing `master_probe_v1.epub` and Deliberately Omitted CJK / Emoji Fonts
- **Symptom**: `master_probe_v1.epub` (`probe` profile in `tools/profiles.json`) was not present in the uploaded zip bundles, and `NotoSansCJK-Regular.otf` / `NotoColorEmoji.ttf` were deliberately omitted per Section 2.
- **Fallback Applied**:
  - Recorded `probe` as `NOT RUN: master_probe_v1.epub not supplied in uploaded bundles`.
  - Patched `resolve_font_path` so missing `NotoSansCJK-Regular.otf` and `NotoColorEmoji.ttf` degrade gracefully to `Bookerly-Regular.ttf` without picking up Debian's incompatible CBDT bitmap font, and recorded `exam1` pages `50, 51` and `exam2` page `42` as `NOT RUN: font not supplied`.

## 4. Session 002 Status: No Active Blockers
- **Status**: Zero active blockers.
- **Environment**: Host toolchain, Android SDK, Gradle, adb, and connected physical Samsung Galaxy M30 (`SM-M305F`) were all fully functional. Tasks T0–T5 completed without hitting any time-box thresholds or unresolved blocks.
