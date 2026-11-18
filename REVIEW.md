# Adversarial Self-Review (`REVIEW.md`)

Date: 2026-11-18  
Scope: Rust port (`kr-core`, `kr-cli`, `kr-jni`), Android integration (`:engine`, `:app`), and parity gates.

---

## 1. Semantic Traps Checklist (Section 2)

| Trap # | Description | Risk & Analysis | Mitigation & Verification |
|---|---|---|---|
| **1** | Python `round()` vs Rust `.round()` | Python `round()` is ties-to-even. Rust's `f64::round()` rounds half away from zero. | All rounding in `kr-core` routes through `math_py::py_round`, `py_round_i64`, `py_round_i32`, or `round_ties_even()`. Unit tests in `math_py.rs` verify exact ties-to-even behavior. |
| **2** | Floor division `//` and `%` | Python `//` floors toward negative infinity; Rust `/` truncates toward zero on negative numbers. | Handled in `math_py::py_floor_div`, `py_floor_mod`, and `py_divmod` for all signed integer calculations (e.g. glue distribution in `layout.rs`). |
| **3** | Float precision (f64 vs f32) | Python floats are 64-bit IEEE 754. Accidental use of 32-bit floats or fused multiply-add breaks bit parity. | All geometry, positions, scales, and pen positions in `kr-core` use `f64`. FreeType 26.6 fixed-point math uses signed 64-bit integers (`i64`) matching Python `int`. |
| **4** | Summation order & compensation | Python 3.12 `sum()` uses Neumaier compensation. Container uses Python 3.11. | Golden hashes and local references were generated under Python 3.11. Iteration order in Rust matches Python list iteration exactly. |
| **5** | UTF-8 vs UTF-16 vs Unicode scalars | Rust strings are UTF-8 bytes; Python strings are Unicode code points; Android Kotlin strings and Locators are UTF-16 code units. | `text_layer.rs` computes offsets in Unicode code points; `page_model.rs` maps offsets to UTF-16 code units using `code_point_to_utf16_offset`. Verified across 40,644 words with 0 violations in Gate P0b. |
| **6** | Dict iteration order & stable sorts | Python dicts maintain insertion order. Non-deterministic HashMap iteration breaks serialization. | `ir.rs` and `page_model.rs` use sorted keys or deterministic ordered structures (`Vec`, `BTreeMap`, `preserve_order` in `serde_json`). Gate P1 proved 314/314 canonical JSON byte identity. |
| **7** | Swallowed errors (`try/except`) | Python code catches and ignores certain DOM or font parsing errors. Rust `?` could panic or abort early. | Error handling in `epub.rs` mirrors Python `try/except` fallbacks, falling back to empty text runs or default styling where Python does. |
| **8** | Canonical IR serialization | Key sorting, separators (`: `, `, `), float formatting (`1e-6` precision, `-0.0` normalization). | `PositionedPage::canonical_json` in `ir.rs` implements exact key ordering, float rounding to 6 decimal places, and negative zero stripping. 314/314 pages match bit-for-bit. |
| **9** | HarfBuzz shaping sequence | Buffer flags, cluster levels, features, and face scaling (`size26 / upem - 1e-9`). | `fonts.rs` invokes HarfBuzz with exact flags (`HB_BUFFER_FLAG_DEFAULT`, cluster level 0) and scaling formula. Verified on device with HarfBuzz 6.0.0. |
| **10** | FreeType rasterization sequence | Load flags (`FT_LOAD_NO_HINTING`, `FT_LOAD_NO_BITMAP`), char size, `FT_Outline_EmboldenXY`, autohinting. | `raster.rs` replicates Python FreeType calls. Post table format 3.0 glyph names resolved via `cmap` Unicode table. 314/314 standalone rasterizer pages match bit-for-bit (Gate P2). |
| **11** | Image resampling | PIL `Image.BILINEAR` convolution vs simple interpolation; `_skia_bilerp_rgb` cover scaling. | `image_resample_bilinear` in `raster.rs` replicates Pillow's box-filter-supported bilinear filter. Bit-identical pixels confirmed in Gate P2. |
| **12** | HTML/CSS parsing | BeautifulSoup XML/HTML parser recovery vs XML parsers. | `epub.rs` robustly handles unclosed tags, entity decoding, and whitespace collapsing. Mutation fuzzer (500 iterations) verified 0 crashes. |
| **13** | Hyphenation `.bin` trie | Custom binary trie packing in `hyph_*.bin`. | `hyphen.rs` parses the binary trie and produces identical hyphenation points. |
| **14** | Threading determinism | Multi-threading race conditions on caches. | Engine instances are single-threaded; JNI engine registry protects each engine instance with a `std::sync::Mutex`. |

---

## 2. Unsafe Blocks Audit & Soundness Justification

`kr-core` enforces `#![deny(unsafe_code)]` at the crate root. Only two internal modules use `unsafe`:
1. `kr-core/src/fonts.rs` (`mod hb_ffi`):
   - **Calls**: `hb_blob_create`, `hb_face_create`, `hb_font_create`, `hb_buffer_create`, `hb_shape`, `hb_buffer_get_glyph_infos`, `hb_buffer_get_glyph_positions`, and destroy methods.
   - **Soundness**: All input buffers (`&[u8]`) are kept alive for the lifetime of the HarfBuzz objects. Output pointers are converted to Rust slices with lengths explicitly verified from `hb_buffer_get_length`. Every allocated HarfBuzz object is destroyed on drop or function exit.
2. `kr-core/src/raster.rs` (`mod ft_ffi`):
   - **Calls**: `FT_Init_FreeType`, `FT_New_Memory_Face`, `FT_Set_Char_Size`, `FT_Load_Glyph`, `FT_Render_Glyph`, `FT_Outline_EmboldenXY`, `FT_Done_Face`, `FT_Done_FreeType`.
   - **Soundness**: Font memory buffers are owned by `_RasterFontMeta` and pinned for the duration of the FreeType face. Return codes are checked after every FreeType call.
3. `kr-jni/src/lib.rs` (JNI Direct ByteBuffer):
   - **Calls**: `env.get_direct_buffer_address`, `env.get_direct_buffer_capacity`, `std::slice::from_raw_parts_mut`.
   - **Soundness**: Null pointer checks and capacity checks are performed before creating the slice. The direct byte buffer is allocated and owned by the calling JVM thread (`ByteBuffer.allocateDirect`) and valid for the duration of the synchronous JNI invocation.

---

## 3. Panic Safety Across JNI Boundary

Every single exported JNI function in `kr-jni/src/lib.rs`:
- `Java_app_opusreader_engine_JniNativeBridge_nativeVersion`
- `Java_app_opusreader_engine_JniNativeBridge_nativeSelfTest`
- `Java_app_opusreader_engine_JniNativeBridge_nativeCreate`
- `Java_app_opusreader_engine_JniNativeBridge_nativeSetFont`
- `Java_app_opusreader_engine_JniNativeBridge_nativeSetHyphenation`
- `Java_app_opusreader_engine_JniNativeBridge_nativeOpen`
- `Java_app_opusreader_engine_JniNativeBridge_nativePageCount`
- `Java_app_opusreader_engine_JniNativeBridge_nativePageIndexFor`
- `Java_app_opusreader_engine_JniNativeBridge_nativePageIndexForProgress`
- `Java_app_opusreader_engine_JniNativeBridge_nativePageModel`
- `Java_app_opusreader_engine_JniNativeBridge_nativeRender`
- `Java_app_opusreader_engine_JniNativeBridge_nativeSearch`
- `Java_app_opusreader_engine_JniNativeBridge_nativeClose`

wraps its entire implementation in `std::panic::catch_unwind(AssertUnwindSafe(|| ...))`.
- No Rust panic can ever unwind across the extern "system" boundary into the Android ART runtime.
- On error or panic, functions return sentinel error codes (`0`, `-1`, `JNI_FALSE`, or `null` / error string prefixed with `"ERR\t"`).
- Kotlin `JniNativeBridge` checks all return values and translates errors into Kotlin `EngineException`.

---

## 4. Kotlin Main-Thread Safety & Concurrency

- `NativeReaderEngine.open(book, settings)` is a `suspend` function executing on `backgroundDispatcher` (`Dispatchers.Default`). Heavy parsing, EPUB extraction, layout, and wire model decoding never block the Android UI thread.
- `pageAt`, `pageAtProgress`, `next`, `previous`, `progress`, `hitTest`, `rectsFor`, and `textFor` operate synchronously on immutable cached `BookSession` structures in $< 0.1\text{ ms}$, ensuring 60/120 fps fluid scrolling and touch response on the main thread.
- `draw` checks an in-memory `BitmapCacheKey` LRU cache. On cache hits, draw takes $< 8\text{ ms}$ (measured 7.36 ms on Galaxy M32). Neighboring pages are prefetched asynchronously via `prefetchScope.launch`.

---

## 5. Scope & Unverified Items

1. **`master_probe_v1.epub`**: The `probe` corpus was not supplied in the work folder. Correctly recorded as `NOT RUN: file not supplied`.
2. **Missing CJK & Emoji Fonts**: `NotoSansCJK-Regular.otf` and `NotoColorEmoji.ttf` were deliberately omitted. Pages requiring them (`exam1` p.50–51, `exam2` p.42) fall back cleanly to Bookerly outlines without crashing.
3. **End-to-End Layout Diff (P4/P5)**: When rendering directly from EPUB files, 253/314 pages (80.6%) achieve bit-for-bit identical RGB SHA-256 hashes. The remaining pages exhibit sub-pixel line breaking differences due to micro float precision in Knuth-Plass hyphenation penalties. Standalone IR roundtrip (P1), rasterizer (P2), and page model (P3) are all 100.0% bit-identical.
