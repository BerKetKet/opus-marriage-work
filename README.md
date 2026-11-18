# Kindle Render Rust Port & Opus Reader Android Marriage

This repository contains the complete verification artifacts, architecture decisions, and code deliverables for the Rust port of `kindle_render` and its marriage with the Opus Reader Android application.

---

## Quick Navigation

- **[FINAL_REPORT.md](FINAL_REPORT.md)**: Full verification report, performance benchmarks on Samsung Galaxy M30 (`SM-M305F`), and gate results.
- **[VERIFICATION_LEDGER.md](VERIFICATION_LEDGER.md)**: Empirical verification ledger with verbatim printed command outputs (all gates marked `PASS`, `FAIL`, or `NOT RUN: <reason>`).
- **[NOTES.md](NOTES.md)**: Current state, what is verified, what is unverified, and next steps.
- **[DECISIONS.md](DECISIONS.md)**: Architectural decisions D1–D12 with rationale and empirical evidence.
- **[REVIEW.md](REVIEW.md)**: Code review and architectural risk assessment.
- **[MERGE_MANIFEST.md](MERGE_MANIFEST.md)**: Manifest of patch deliverables and merge application instructions.
- **[WORKLOG.md](WORKLOG.md)**: Chronological step-by-step log across all stages (A0–A8).

---

## Deliverables

All ready-to-merge patches and pre-built binaries are in [`deliverables/`](deliverables/):
1. [`deliverables/render.engine.patch`](deliverables/render.engine.patch): Unified diff patch for the `render.engine` repository (Rust engine, CLI tools, FreeType/HarfBuzz integration, container harness).
2. [`deliverables/opus-reader.patch`](deliverables/opus-reader.patch): Unified diff patch for the `opus-reader` Android app (JNI bridge, native engine integration, geometry presets, on-device test suites).
3. [`deliverables/jniLibs/arm64-v8a/libkindle_render_jni.so`](deliverables/jniLibs/arm64-v8a/libkindle_render_jni.so): Self-contained `arm64-v8a` shared library bundling static FreeType 2.12.1 and static HarfBuzz 6.0.0 (dynamic links strictly `libdl, libm, libc`).

---

## Verification Summary Table

| Gate / Component | Result | Measured Evidence |
|---|---|---|
| **G4 (Python Imports)** | **PASS** | `passed=True errors=0` |
| **HarfBuzz Lock** | **PASS** | FreeType & HarfBuzz locked to 6.0.0 |
| **P0 (Oracle Determinism)** | **PASS** | 314/314 corpus pages 100% deterministic |
| **P0b (Word Offsets & Reflow)** | **PASS** | 40,644 word locator slices 100% invariant; 16/16 reflow spine texts byte-identical |
| **P1 (Canonical IR Round-Trip)** | **PASS** | **314/314 (100.0%) PASS** (bit-for-bit JSON & layout SHA-256 match) |
| **P2 (Standalone Rasterizer)** | **PASS** | **314/314 (100.0%) PASS** (pixel-for-pixel bit-identical RGB SHA-256 across all 5 corpora) |
| **P3 (Text Layer & Page Model)** | **PASS** | **314/314 (100.0%) PASS** (byte-for-byte identical TSV models across all 5 corpora) |
| **P4 / P5 (EPUB End-to-End)** | **MEASURED** | Page counts 100% identical; Pixels: **253/314 (80.6%) bit-for-bit identical** |
| **P6 (Static Analysis & Fuzzing)** | **PASS** | Clippy 0 warnings/errors; 8/8 robustness guards PASS; 500 mutation iterations PASS |
| **K1 (Kotlin JVM Tests & Build)** | **PASS** | 47/47 JVM tests PASS; `app-debug.apk` built (21 MB) |
| **N1 (Android Native Library)** | **PASS** | `libkindle_render_jni.so` (4.1 MB, zero external dependencies) |
| **D1 (On-Device Functional Parity)** | **PASS** | 5/5 connected tests PASS on Galaxy M30 (`SM-M305F`); page 0 RGBA SHA-256 bit-identical to Python oracle (`fb86f3b3...`) |
| **D1 (On-Device Latencies)** | **PASS** | `open = 941.69 ms`, `model = 0.03 ms`, `render_p50 = 7.91 ms`, `render_p95 = 145.82 ms` |
| **D2 (On-Device Fallback)** | **PASS** | Missing `.so` fallback verified: app booted without crashes, selected `FakeReaderEngine` |

---

## Sanitization & Proprietary Asset Notice

Per project safety rules (Rule S4) and secrets policy:
- Proprietary font binaries (`*.ttf`, `*.otf`), hyphenation dictionaries (`*.bin`, `*.dic`), and large bundles (`*.zip`) are excluded from this repository.
- Physical device serial numbers are redacted as `[REDACTED_DEVICE_SERIAL]`.
