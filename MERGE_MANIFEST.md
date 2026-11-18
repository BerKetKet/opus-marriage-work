# Merge Manifest (`MERGE_MANIFEST.md`)

Date: 2026-11-18  
Deliverables directory: `deliverables/`

---

## 1. Deliverables Summary

1. `deliverables/render.engine.patch` (107 KB)
   - Git patch generated against baseline `547d019`.
   - Contains all Rust implementation improvements (`kr-core`, `kr-cli`, `kr-jni`), build scripts (`build_native_deps.sh`, `kr-jni/build.rs`), parity gates (`gate_p1_roundtrip.py`, `gate_p2_raster.py`, `gate_p3_pagemodel.py`), fuzzer (`fuzz_epub.py`), container script (`run_in_container.sh`), and local golden hashes (`tools/golden_local/`).
   - Zero modifications to `kindle_render/*.py` (Python oracle untouched).
   - Zero proprietary fonts or hyphenation binaries included.

2. `deliverables/opus-reader.patch` (8.5 KB)
   - Git patch generated against baseline `fa4045d`.
   - Contains unit test fix in `NativeReaderEngineTest.kt` (removing unmocked `RectF.toString()` from assertion interpolation).
   - Configures `androidTest` assets to include font assets from `app/src/main/assets`.
   - Adds on-device performance benchmark in `NativeReaderEngineParityTest.kt`.
   - Excludes `.so` from git tracking in `.gitignore`.

3. `deliverables/jniLibs/arm64-v8a/libkindle_render_jni.so` (4.1 MB)
   - Compiled Android shared library for `aarch64-linux-android` (`arm64-v8a`).
   - Statically links FreeType 2.12.1, HarfBuzz 6.0.0, and libc++ (`libc++_static.a` + `libc++abi.a`).
   - Dynamic dependencies (`readelf -d`): `libdl.so`, `libm.so`, `libc.so` only.

---

## 2. How to Apply in Real Repositories

### In `render.engine`:
```bash
cd /path/to/real/render.engine
git apply /path/to/deliverables/render.engine.patch
```

To build native dependencies and Rust binaries:
```bash
cd /path/to/real/render.engine
./rust/build_native_deps.sh
cargo build --release -p kr-cli --manifest-path rust/Cargo.toml
```

### In `opus-reader`:
```bash
cd /path/to/real/opus-reader
git apply /path/to/deliverables/opus-reader.patch
mkdir -p engine/src/main/jniLibs/arm64-v8a
cp /path/to/deliverables/jniLibs/arm64-v8a/libkindle_render_jni.so engine/src/main/jniLibs/arm64-v8a/
```

To build and run:
```bash
cd /path/to/real/opus-reader
./gradlew :engine:testDebugUnitTest :app:testDebugUnitTest :app:assembleDebug
./gradlew :engine:connectedDebugAndroidTest
./gradlew :app:installDebug
```
