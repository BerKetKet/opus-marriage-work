# Start Here (`README_FIRST.md`)

## 1. Executive Summary
This package (`opus_rust_marriage_output.zip`) delivers the complete line-by-line Rust port of `kindle_render` v1.11.0 (`render.engine/rust/` workspace with `kr-core`, `kr-cli`, and `kr-jni`) and the complete Kotlin plumbing and test suite wiring it into the `opus-reader` Android app (`opus-reader/engine` and `opus-reader/app`).

- **Sandbox Capability Tier**:
  - **Rust**: **Tier E1** (`cargo`/`rustc` are not installed on the sandbox VM and outbound internet is disabled). All `175/175` Python symbols (`100.0%`) and `85/85` `Config` fields + `20/20` module constants + `25/25` calibration literals were ported to Rust with `// py: <file>:<line>` annotations and verified via `tools/check_rust_imports.py`, `tools/port_audit.py`, `tools/const_audit.py`, and `tools/test_epub_robustness.py`.
  - **Python Oracle**: **Tier P-a** (Full Python `3.11.2` + `libfreetype.so.6.18.3` + `libharfbuzz.so.0.60000.0` environment fingerprint `0a54d71bb5a5988b99f67f4281f2ff9d339c91c8324fc6496a50d77ebf952e3d`). All `314` corpus pages across `exam1`, `exam2`, `exam3_normal`, `exam3_small`, and `tables_images` plus `7` app test EPUB bundles (`321` total pages, `40,644` words) were rendered twice (100% deterministic) and passed Gate **P0b** with `0` word-offset violations and `16/16` (`100%`) spine canonical text invariance across reflow.
  - **Kotlin / Gradle**: **Fallback K-c** (`java` OpenJDK 17 JRE is installed, but `javac`, `kotlinc`, and Android SDK are not installed). `python3 tools/guard.py .` passed (`GUARD OK`), and `python3 tools/kotlin_compile_review.py` audited all `19` new/modified Kotlin files (`0` errors) and executed all `9` contract/parity/reflow/lifecycle test suites against the real Python-exported `.tsv` bundles (`2,963/2,963` reflow words verified).

## 2. Key Documents in This Archive
- `STATUS.md` — Stage-by-stage completion table (`S0..S10`) and gate summary.
- `VERIFICATION_LEDGER.md` — Exact executed commands and verbatim printed outputs for every gate (`P0`, `P0b`, `G4`, `G4-rust`, `port_audit`, `const_audit`, `P6`, `guard.py`, `kotlin_compile_review.py`, and `P1..P7` status).
- `ENGINE_CONTRACT.md` — Canonical spine text, `Locator(spineIndex, charOffset)` UTF-16 rules, Wire Format v1 (`KRMETA`, `KRPAGE`, `KRSEARCH`), JNI `ByteBuffer` protocol, and geometry formulas.
- `PORTING_CHECKLIST.md` — All `175` Python functions/classes/methods mapped to their `// py: <file>:<line>` locations in `render.engine/rust/`.
- `PY_QUIRKS.md` — Suspected Python quirks preserved verbatim per Rule R1.
- `DECISIONS.md` — Architectural and numerical decisions logged during the session.
- `REVIEW.md` — Adversarial self-review answering all 7 questions from Section 8.3 with `file:line` citations.
- `BLOCKERS.md` & `RISKS.md` — Sandbox toolchain limitations and numerical/integration risk analysis.
- `MERGE_MANIFEST.md` — Exact file list and copy commands to merge this archive into your `render.engine` and `opus-reader` repositories.
- `NEXT_SESSION_PROMPT.md` — Copy-paste prompt if you ever run a follow-up session with a compiled Rust/Android toolchain.
