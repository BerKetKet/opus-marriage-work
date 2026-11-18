# Engine Contract Specification (`ENGINE_CONTRACT.md`)

**Version:** `1.0`  
**Scope:** Boundary contract between `kindle_render` (Python oracle / Rust `kr-core` + `kr-jni`) and `opus-reader` (`:engine` Kotlin module).

---

## 1. Canonical Plain Text & Locator Semantics (Decision D1)

### 1.1 Provenance of IR & Text Layer Indices (`ir.py`, `text_layer.py`, `layout.py`, `page.py`)
In `kindle_render` v1.11.0:
- **`block_idx`** (`GlyphCommand.block_idx`, `TextBlockMeta.block_idx`): 0-based document-wide monotonic integer (`Pager._block_counter` in `page.py:86, 353, 540, 639, 987`) incremented once per layout block (`add_text_block`, `add_pre`, `add_table`, `add_image`). When a block spans a page break, both pages carry a `TextBlockMeta` with the same `block_idx`.
- **`line_idx`** (`GlyphCommand.line_idx`): 0-based document-wide monotonic integer (`Pager._line_counter` in `page.py:87, 505, 610, 703, 906`) incremented once per rendered line.
- **`logical_word_idx`** (`GlyphCommand.logical_word_idx`):
  - For `"paragraph"`, `"heading"`, and `"list_item"` blocks: 0-based per-block token counter (`word_counter` in `layout.py:build_items`, `layout.py:127`). When a word is split across lines by Liang hyphenation, soft hyphen (`U+00AD`), slash (`/`), zero-width space (`U+200B`), or ellipsis (`…`), all resulting `Box` fragments share the same `logical_word_idx`.
  - For list markers (`_draw_list_marker`, `page.py:303`): `logical_word_idx = -1` and `is_list_marker = True`.
  - For `"pre"` and `"table"` blocks (`page.py:617, 706, 923`): 0-based per-line word counter (`0, 1, ...` on each line).
- **`word_idx`** (`GlyphCommand.word_idx`): 0-based visual word counter on a single line (`vis_word_idx` in `layout.py:layout_line`, `layout.py:725`, or `-1` for list markers).
- **`logical_char_idx`** (`GlyphCommand.logical_char_idx`): 0-based cluster index within a shaped token (`c_idx` / `l_idx` in `layout.py:_shape_token_with_fallbacks`, or `-1` for drop-cap glyphs in `page.py:397`).

### 1.2 Canonical Plain Text Definition per Spine Item
Each book comprises $N_{\text{spines}} \ge 1$ spine items indexed $s \in \{0, \dots, N_{\text{spines}} - 1\}$ in OPF spine order (including `"cover"` at $s = 0$ when a cover image block is present, matching the order of distinct `chapter` identifiers in `PositionedDocument`).

For each spine $s$, its canonical plain text $T_s$ is constructed deterministically from the structured text layer (`build_document_text_layer`) as follows:
1. **Block Ordering**: Blocks belonging to spine $s$ are visited in increasing `block_idx` order.
2. **Line & Word Ordering**: Within each block, lines are visited in increasing `line_idx` order. Within each line, visual word entries $w \in \text{line.words}$ are visited in `reading_order` (`0, 1, ...`), where any non-empty list marker word (`is_list_marker == true`, e.g., `"1."`, `"•"`, `"■"`) comes first on line 0 of a list item, followed by content words ordered by `logical_word_idx`.
3. **Word Text & Synthetic Hyphens**:
   - Each visual word's text is the concatenation of its non-synthetic cluster strings:
     $$\text{word.text} = \bigoplus_{c \in \text{word.clusters},\; \neg c.\text{is\_synthetic\_hyphen}} c.\text{text}$$
   - Synthetic hyphen glyphs (`is_synthetic_hyphen == true`) are excluded from `word.text` and belong to **no** character range in $T_s$.
   - Any word entry with empty `word.text == ""` emits no characters into $T_s$ and produces no `WordBox`.
4. **Separators Between Consecutive Non-Empty Words in Spine $s$**:
   - **Block Separator**: When transitioning from block $b_{\text{prev}}$ to a different block $b_{\text{cur}} \ne b_{\text{prev}}$ within the same spine $s$, exactly one newline character `"\n"` (`U+000A`, 1 UTF-16 code unit) is inserted into $T_s$.
   - **Intra-Block Hyphenated / Split Word Continuation**: When $b_{\text{cur}} == b_{\text{prev}}$ and word $w$ is the first non-empty word on a new line (`w_index_in_line == 0`):
     - In `"paragraph"`, `"heading"`, and `"list_item"` blocks: if $\neg w.\text{is\_list\_marker} \land w.\text{logical\_word\_idx} \ge 0 \land w.\text{logical\_word\_idx} == w_{\text{prev}}.\text{logical\_word\_idx}$, then **no separator** (`""`, 0 UTF-16 code units) is inserted between $w_{\text{prev}}$ and $w$. The two visual fragments receive contiguous UTF-16 ranges $[a, b)$ and $[b, c)$ in $T_s$, and the slice $T_s[a:c]$ equals the unhyphenated full word.
     - In `"pre"` and `"table"` blocks: if the previous line had `ends_with_synthetic_hyphen == true` or $w_{\text{prev}}.\text{text}$ ends with `"-"`, `"/"`, or `"_"`, **no separator** (`""`, 0 UTF-16 code units) is inserted.
   - **Intra-Block Word Separator**: Between all other consecutive non-empty words in the same block (same line, normal line wrap, after a list marker before the first content word, or between adjacent `<pre>` / `<table>` words), a single ASCII space `" "` (`U+0020`, 1 UTF-16 code unit) is inserted into $T_s$.
5. **Images & Horizontal Rules**:
   - Cover images, block images, inline images, and `<hr/>` blocks emit no text into $T_s$.
   - A page containing only an image or rule (with zero words) has `words = emptyList()` and a **zero-length anchor** `start = Locator(s, offset)`, `end = Locator(s, offset)` at the current UTF-16 offset in spine $s$ (e.g., `Locator(0, 0)` on a cover page).
6. **UTF-16 Code-Unit Indexing**:
   - `Locator(spineIndex, charOffset)` uses a 0-based **UTF-16 code-unit offset** into $T_{\text{spineIndex}}$.
   - Basic Multilingual Plane (BMP) code points (`U+0000..U+FFFF`) have UTF-16 length `1`.
   - Supplementary astral code points (`U+10000..U+10FFFF`) encode as a surrogate pair and have UTF-16 length `2`.
   - Every `WordBox` on spine $s$ has `start = Locator(s, startOff)` and `end = Locator(s, endOff)` with $0 \le \text{startOff} < \text{endOff} \le |T_s|_{\text{UTF-16}}$, and slicing $T_s$ at $[\text{startOff}, \text{endOff})$ yields `WordBox.text` exactly.
   - For any page with $\ge 1$ word, `page.start = page.words.first().start` and `page.end = page.words.last().end`.
   - **Reflow Invariance**: Because synthetic hyphens are stripped and split word fragments are joined with `""`, $T_s$ is invariant across font size, pitch, and margin reflow (verified `16/16` chapters byte-for-byte identical between `exam3_normal` and `exam3_small`).

---

## 2. Page Coordinates, Bitmaps & Canvas Mapping (Decision D2)

1. **Native IR Coordinate Space**:
   - Every page is laid out and rasterized in a fixed `1080 x 2340` pixel space (`W_ir = 1080`, `H_ir = 2340`).
   - All `WordBox.rect` and `LinkBox.rect` coordinates (`left`, `top`, `right`, `bottom`) are in IR pixels satisfying $0 \le \text{left} < \text{right} \le 1080$ and $0 \le \text{top} < \text{bottom} \le 2340$.
2. **Bitmap Format & Theme Coloring**:
   - `nativeRender(handle, pageIndex, fgArgb, bgArgb, directByteBuffer)` writes a full `1080 x 2340` `ARGB_8888` image (`10,108,800` bytes = `1080 * 2340 * 4`, byte order `R, G, B, A` with `A = 0xFF` matching `android.graphics.Bitmap.Config.ARGB_8888` `copyPixelsFromBuffer`).
   - When `PageTheme(textColor, backgroundColor)` equals the engine's default `fg`/`bg` (`#000000` on `#FFFFFF`), ink is blended directly from `ir_page.fg`/`ir_page.bg`. When the app supplies a custom theme (such as dark mode `textColor = 0xFFE0E0E0`, `backgroundColor = 0xFF000000`), background pixels map to `backgroundColor` and monochrome foreground glyphs/rules map to `textColor` (preserving colored highlights/links/images).
3. **Canvas Scaling in `ReaderScreen.kt` and `Engine.draw`**:
   - In `ReaderScreen.kt` Mode A (immersive reading on the `1080x2340` 420 dpi test phone), `Canvas` has pixel size `1080 x 2340` (uniform scale factor $S = 1.0$). `NativeReaderEngine.draw(page, canvas, theme)` draws the `1080 x 2340` `Bitmap` with `srcRect = Rect(0, 0, 1080, 2340)` and `dstRect = RectF(0f, 0f, 1080f, 2340f)`.
   - In `ReaderScreen.kt` Mode B (peek/central cards) and `ReaderThumbnailsGrid`, `ReaderScreen.kt` applies `canvas.nativeCanvas.scale(size.width / 1080f, size.width / 1080f)` before calling `engine.draw(page, canvas.nativeCanvas, theme)`. Because `dstRect = RectF(0f, 0f, 1080f, 2340f)` is drawn in the canvas's local coordinate system, Android's canvas matrix automatically scales the `1080x2340` bitmap to the card/thumbnail size.
   - If an external caller passes an unscaled software `Canvas` whose width $W_c \ne 1080$ and whose transform matrix is identity, `NativeReaderEngine.draw` applies uniform scale $S = W_c / 1080.0\text{f}$ (`dstRect = RectF(0f, 0f, 1080f * S, 2340f * S)`).

---

## 3. Cumulative Progress & Scrubber Resolution (Decisions D3 & D4)

1. **Cumulative UTF-16 Offsets**:
   - Let $L_s = |T_s|_{\text{UTF-16}}$ be the UTF-16 code-unit length of spine $s$ (reported in the `S\t<spineIndex>\t<utf16CharLength>\t<chapterId>` line of the book model).
   - Define cumulative spine start offsets $C_0 = 0$ and $C_s = \sum_{k=0}^{s-1} L_k$, with total book length $L_{\text{total}} = \sum_{k=0}^{N_{\text{spines}}-1} L_k$.
2. **`progress(page: Page): Progress`**:
   - $\text{current} = \min(L_{\text{total}}, C_{\text{page.start.spineIndex}} + \text{page.start.charOffset})$.
   - $\text{total} = L_{\text{total}}$.
   - $\text{percent} = \begin{cases} (\text{current}.\text{toFloat}() / \text{total}.\text{toFloat}()) \times 100\text{f} & \text{if } \text{total} > 0 \\ 0\text{f} & \text{otherwise} \end{cases}$.
3. **`pageAtProgress(current: Int): Page`**:
   - Added to `ReaderEngine` with default implementation `fun pageAtProgress(current: Int): Page = pageAt(Locator(0, current))`.
   - Overridden in `NativeReaderEngine` and `FakeReaderEngine`: clamps `clamped = current.coerceIn(0, total)`, locates the highest spine $s$ with $C_s \le \text{clamped}$ (where $L_s > 0$ or $s = 0$), computes local spine offset $\text{localOff} = \text{clamped} - C_s$, and returns `pageAt(Locator(s, localOff))`.
   - `ReaderViewModel.onScrubberCommit(location: Int)` calls `engine.pageAtProgress(clamped)` instead of `engine.pageAt(Locator(0, clamped))`.

---

## 4. Wire Format v1 Grammar (Section 6.4 & Decision D5)

All text crossing JNI is UTF-8 encoded, with `\n`-terminated records and `\t`-separated fields.

### 4.1 String Escaping Rules
In any text field (`<escapedTitle>`, `<escapedAuthor>`, `<escapedChapterId>`, `<escapedText>`, `<escapedTarget>`, `<escapedSnippet>`):
- `\` (`U+005C`) $\leftrightarrow$ `\\`
- `\t` (`U+0009`) $\leftrightarrow$ `\t`
- `\n` (`U+000A`) $\leftrightarrow$ `\n`
- `\r` (`U+000D`) $\leftrightarrow$ `\r`
All other UTF-8 characters (including astral emoji, RTL Arabic/Hebrew, Indic, Ethiopic) are transmitted literally as UTF-8.

### 4.2 Book Model Wire Format (returned by `nativeOpen`)
```text
B\t<escapedTitle>\t<escapedAuthor>\t<spineCount>\t<pageCount>\t<isCalibrated:0|1>\t<missingFontCount>
S\t<spineIndex>\t<utf16CharLength>\t<escapedChapterId>
T\t<level>\t<spineIndex>\t<charOffset>\t<escapedTitle>
```
- Exactly one `B` line first.
- `spineCount` `S` lines in order `0 .. spineCount - 1`.
- Zero or more `T` lines in reading order.

### 4.3 Page Model Wire Format (returned by `nativePageModel`)
```text
P\t<pageIndex>\t<startSpine>\t<startOff>\t<endSpine>\t<endOff>\t<widthPx>\t<heightPx>
W\t<startSpine>\t<startOff>\t<endSpine>\t<endOff>\t<left>\t<top>\t<right>\t<bottom>\t<escapedText>
L\t<escapedTarget>\t<left>\t<top>\t<right>\t<bottom>
```
- Exactly one `P` header line first.
- Zero or more `W` lines in reading order. Coordinates `<left>`, `<top>`, `<right>`, `<bottom>` are formatted in fixed-point decimal with 3 fractional digits (`%.3f`, `.` decimal separator, e.g. `79.000`).
- Zero or more `L` lines for hyperlinks on the page (`%.3f` coordinates).

### 4.4 Search Hits Wire Format (returned by `nativeSearch`)
```text
H\t<spineIndex>\t<charOffset>\t<utf16MatchLen>\t<escapedSnippet>
```
- Zero or more `H` lines in book order.

---

## 5. Threading, Caching & Lifecycle (Decision D4)

1. **`open(book, settings)`**:
   - Executes on `Dispatchers.Default`.
   - Calls `nativeOpen`, fetches and decodes all compact `Page` models (`0 .. pageCount - 1`), populates an immutable snapshot (`BookSession`) containing `pages: List<Page>`, `pageIndexByStart: Map<Locator, Int>`, `pagesBySpine: Map<Int, List<Page>>`, and `spineOffsets: IntArray`, and clears the bitmap LRU cache.
2. **Synchronous Queries (`pageAt`, `pageAtProgress`, `next`, `previous`, `progress`, `hitTest`, `rectsFor`, `textFor`, `toc`)**:
   - Read from the current volatile `BookSession` snapshot in memory without JNI round-trips on the main thread.
   - `next(page)` and `previous(page)` perform an $O(1)$ lookup via identity/start-locator map.
   - `textFor(page, range)` slices the canonical text reconstructed from the page's words (joining words in the same block with `" "` or `""` for contiguous split fragments, and blocks with `"\n"`).
3. **Bitmap LRU Cache & Prefetch (`draw`)**:
   - `NativeReaderEngine` maintains a thread-safe `LruCache` of capacity `4` `Bitmap` instances (`1080 x 2340`, `ARGB_8888`, ~10.1 MB each) keyed by `(sessionId, pageIndex, textColor, backgroundColor)`.
   - On `draw(page, canvas, theme)`:
     - If cached, draws immediately and triggers background prefetch of `pageIndex + 1` and `pageIndex - 1` on `Dispatchers.Default`.
     - If a cache miss occurs, renders synchronously into a reusable direct `ByteBuffer` via `nativeRender`, copies into a `Bitmap`, stores it in the LRU cache, logs the render latency in milliseconds, draws to `canvas`, and schedules neighbor prefetch.
4. **Native Handle Management**:
   - Native engine instances live in a thread-safe Rust handle table (`Mutex<HashMap<i64, Arc<Mutex<EngineInstance>>>>`).
   - `NativeReaderEngine.close()` (and re-opening) releases native handles cleanly.

---

## 6. Settings Mapping & Calibrated Geometries (Decision D6)

### 6.1 Calibrated Kindle Geometries (`tools/profiles.json`)
Only the following 4 geometry tuples `(size26, pitchPx, x0, right, top, pageBottom)` at `screen_w = 1080, screen_h = 2340`, `fontName = "Bookerly"`, `boldnessLevel = 0`, `justify = true`, `hyphenate = true` are **calibrated** (`isCalibrated = true`):

| `kindleGeometryIndex` | Corpus Profile(s) | `sizePx` (`size26`) | `fontSizeSp` (`@2.625x`) | `pitchPx` | `x0` .. `right` | `top` .. `pageBottom` |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| `0` | `exam3_small` | `34.0 px` (`2176`) | `12.95 sp` | `51 px` | `79 .. 1001` | `168 .. 2203` |
| `1` | `exam2` | `42.0 px` (`2688`) | `16.00 sp` | `57 px` | `79 .. 1001` | `168 .. 2203` |
| `2` | `probe` | `42.0 px` (`2688`) | `16.00 sp` | `57 px` | `39 .. 1041` | `168 .. 2203` |
| `3` | `exam1`, `exam3_normal`, `tables_images` | `45.0 px` (`2880`) | `17.14 sp` | `68 px` | `79 .. 1001` | `168 .. 2203` |

### 6.2 Mapping Rule (`KindleGeometry.fromSettings`)
1. If `settings.kindleGeometryIndex != null`:
   - Uses the indexed calibrated entry from the table above (`0..3`, clamped).
2. If `settings.kindleGeometryIndex == null`:
   - Computes target `rawSizePx = settings.fontSizeSp * 2.625f` and `rawPitchPx = rawSizePx * settings.lineSpacingMultiplier`.
   - `KindleGeometry.nearestCalibrated(settings)` selects the calibrated entry minimizing $|\text{sizePx} - \text{rawSizePx}| + 0.5 \times |\text{pitchPx} - \text{rawPitchPx}| + 0.25 \times |\text{x0} - (\text{settings.marginHorizontalPx} ?: 79)|$.
   - Note that the app's default `ReaderSettings(fontSizeSp = 16f, lineSpacingMultiplier = 1.3f, fontName = "Bookerly")` maps to `rawSizePx = 42.0`, `rawPitchPx = 54.6`, whose nearest calibrated geometry is **Index 1** (`size26 = 2688`, `pitchPx = 57`, `x0 = 79`, `right = 1001`).
   - If the caller explicitly supplies an uncalibrated font size or custom parameters via `KindleGeometry.fromSettings(settings, snapToCalibrated = false)`, `size26 = round(rawSizePx * 64)`, `pitch = round(rawPitchPx)`, and `isCalibrated` is set to `false` (`"uncalibrated: layout is extrapolated"`).

---

## 7. Asset Delivery, Missing Fonts & Error Model (Decisions D7 & Section 6.6)

1. **`EngineAssets` Interface (`:engine`)**:
   - `fun fontBytes(fileName: String): ByteArray?`
   - `fun hyphenationBytes(lang: String): ByteArray?`
   - Implemented in `:app` (`AndroidEngineAssets`), reading `:design` raw font resources (`R.font.bookerly_regular`, `R.font.bookerly_bold`, `R.font.bookerly_display`, etc.) and asset files if bundled.
2. **Missing Font Degradation (Section 6.6)**:
   - When a fallback font (`NotoSansCJK-Regular.otf`, `NotoColorEmoji.ttf`, etc.) is not supplied, the engine falls back to `Bookerly-Regular.ttf` (`.notdef` or space advance), increments `missingFontCount` in the `B\t...` book header, and never panics.
3. **FFI Error Model & Self-Test (R3 & D7)**:
   - Every JNI entry point in `kr-jni` wraps its body in `std::panic::catch_unwind`.
   - Any Rust `Err(EngineError)` or caught panic returns an error sentinel or throws `app.opusreader.engine.EngineException` on the JVM side — never aborting the process.
   - `AppContainer` invokes `JniNativeBridge.isAvailable()` and `JniNativeBridge.selfTest()` (which renders a built-in test string in Rust and verifies its deterministic hash). If either returns `false`, `AppContainer` logs the reason and falls back to `FakeReaderEngine`.
