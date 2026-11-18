# Owner Guide: Running Opus Reader with the Native Engine

This guide explains how to build, install, and use Opus Reader on your Android device (`Samsung Galaxy M30 / M32`), and how to open and read EPUB books using the native Rust rendering engine (`NativeReaderEngine`).

All code changes in this session were AI-written.

---

## 1. What Works Right Now

- **Native Rust Engine**: The native shared library (`libkindle_render_jni.so`) compiles for `arm64-v8a` with FreeType 2.12.1 and HarfBuzz 6.0.0 statically linked. It loads on the device and passes its built-in self-test on every launch.
- **EPUB Parsing and Loading**: Real EPUB files are unpacked, their spine items are parsed, and the 14-chapter Table of Contents is extracted.
- **Typography & Glyph Rasterization**: The Rust engine rasterizes text glyphs directly to memory, producing sharp, anti-aliased Bookerly font rendering on the device screen.
- **Page Navigation**:
  - Tapping the right 20% of the screen turns forward to the next page.
  - Tapping the left 20% of the screen turns backward to the previous page.
  - Tapping the center toggles the top and bottom navigation bars (chrome).
- **Table of Contents**:
  - Tapping the Contents icon in the top bar displays the complete chapter list.
  - Tapping any chapter name jumps directly to that chapter's first page.
- **Performance**:
  - First-time page renders take ~175 ms to ~380 ms on this phone.
  - Pre-cached pages and backward navigation redraw in under 16 ms.

---

## 2. Prerequisites

Connect your Samsung device via USB with USB debugging enabled. Ensure `adb devices` shows the device authorized:

```bash
adb devices -l
```

---

## 3. Step-by-Step Instructions

### Step 1: Build the Debug Application

Run the Gradle build task from the `opus-reader` directory:

```bash
cd /home/bgg/projects/opus_marriage_work/opus-reader
./gradlew :app:assembleDebug
```

### Step 2: Install the App on Your Phone

Stream the compiled APK to your device:

```bash
adb install -r /home/bgg/projects/opus_marriage_work/opus-reader/app/build/outputs/apk/debug/app-debug.apk
```

### Step 3: Copy an EPUB Book to the App Storage

Place the test book into the app's external files directory where the app has read permission:

```bash
adb shell mkdir -p /sdcard/Android/data/app.opusreader/files
adb push /home/bgg/projects/opus_marriage_work/render.engine/corpora/kindle_exam_v3.epub /sdcard/Android/data/app.opusreader/files/kindle_exam_v3.epub
```

### Step 4: Open the EPUB in the Reader

Trigger the app to import and open the EPUB using the deep-link intent:

```bash
adb shell am start -W -a android.intent.action.VIEW -d "opus://open?path=/sdcard/Android/data/app.opusreader/files/kindle_exam_v3.epub" app.opusreader
```

The book will open to the cover / title page within 2-3 seconds.

---

## 4. How to Navigate Inside the Reader

- **Turn Page Forward**: Tap on the right side of the screen (or run `adb shell input tap 950 1200`).
- **Turn Page Backward**: Tap on the left side of the screen (or run `adb shell input tap 100 1200`).
- **Toggle Navigation Bars**: Tap in the middle of the screen (or run `adb shell input tap 540 1200`).
- **Open Table of Contents**: With navigation bars visible, tap the list icon in the top bar (x=250, y=160), or run:
```bash
adb shell input tap 250 160
```
- **Jump to a Chapter**: Tap any chapter name in the Table of Contents list.
- **Return to Library**: Tap the left arrow in the top bar (x=80, y=160).

---

## 5. What Does Not Work Yet (Remaining Work)

1. **Display Settings (Aa Button)**: Tapping the "Aa" button in the reader top bar currently has no visual effect because the settings sheet UI component (roadmap slice S07) has not been built yet.
2. **Reader Overflow Menu (Three Dots)**: Tapping the three dots in the reader top bar currently has no visual effect because the overflow menu composable has not been built yet.
3. **In-App File Picker**: There is no "Import" button inside the Library screen yet. Books currently must be launched via the `opus://open` intent or placed in the app directory.
4. **Memory Management**: Rendered page bitmaps are currently kept in a cache without eviction. Traversing 50+ pages increases native memory use to ~560 MB. An LRU eviction cache will keep this below 100 MB.
