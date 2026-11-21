# Active Environment & Verification Blockers (`BLOCKERS.md`)

**Date**: 2026-11-21  
**Device**: Samsung Galaxy M30 (`SM-M305F`), TrebleDroid GSI Android 13 (`arm64-v8a`)  
**Workspace**: `/home/bgg/projects/opus_marriage_work/`

---

## 1. Blocker B1: Missing `master_probe_v1.epub`
- **Date**: 2026-11-18 (persisting)
- **Symptom**: `master_probe_v1.epub` referenced by the `probe` profile in `render.engine/tools/profiles.json` was omitted from workspace test corpora.
- **Evidence**: `ls -la render.engine/tests/corpora/master_probe_v1.epub` fails (`No such file or directory`).
- **Next Step**: Retain profile as `NOT RUN: file not supplied`. Profile `exam3_p42` created for `kindle_exam_v3.epub` investigation.

## 2. Blocker B2: Deliberately Omitted CJK and Color Emoji Fonts
- **Date**: 2026-11-18 (persisting)
- **Symptom**: `NotoSansCJK-Regular.otf` and `NotoColorEmoji.ttf` are omitted to keep repo size minimal.
- **Evidence**: `render.engine/kindle_render/assets/fonts/NotoSansCJK-Regular.otf` not present. Engine safely falls back to Bookerly for font resolution.
- **Next Step**: Pages with CJK/Emoji glyphs continue to fall back gracefully to Bookerly-Regular.ttf.

## 3. Active Toolchain & Execution Status
- **Host Toolchain**: Fully functional (Rust 1.84+, OpenJDK 17, Android SDK 34, NDK r30, Gradle 8.2, ffmpeg/ffprobe installed on CachyOS).
- **Target Device**: Samsung Galaxy M30 (`SM-M305F`) connected via adb, awake, and responsive.
- **Time-box Thresholds**: Zero active technical blocks preventing compilation, instrumentation, or device execution.
