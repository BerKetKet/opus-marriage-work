# Next Session Prompt (`NEXT_SESSION_PROMPT.md`)

If you run a follow-up session in an environment with `rustc`/`cargo` and the Android NDK/SDK installed, paste the following prompt:

```text
We are resuming from opus_rust_marriage_output.zip where Stages S0..S10 (the full Rust port in render.engine/rust/ across kr-core, kr-cli, kr-jni and the full Kotlin integration in opus-reader/engine and opus-reader/app) have been written and statically audited in a Tier E1 / Fallback K-c sandbox.

Your task in this session (with rustc/cargo and Android SDK available):
1. Unpack opus_rust_marriage_output.zip and merge render.engine/ and opus-reader/ into the repo trees per MERGE_MANIFEST.md.
2. Run `cargo build --manifest-path rust/Cargo.toml --release` and `cargo test --manifest-path rust/Cargo.toml --release`, fixing any compiler diagnostics if they arise.
3. Run `python3 tools/rust_parity.py` to execute dynamic parity gates P1 (IR roundtrip), P2 (Rasterizer from Python IR), P3 (PageModel / text_layer), P4 (Layout/Shaping/Hyphenation), P5 (Full EPUB -> IR -> PageModel -> Pixels), and P6 (fuzz-epub on the 8 hostile EPUBs), and paste the printed outputs into VERIFICATION_LEDGER.md.
4. Cross-compile `libkindle_render_jni.so` for `aarch64-linux-android` (`arm64-v8a`) and host (`x86_64-unknown-linux-gnu`), copy into `opus-reader/engine/src/main/jniLibs/`, and run `./gradlew :engine:testDebugUnitTest :app:testDebugUnitTest :app:assembleDebug` (Gate P7).
```
