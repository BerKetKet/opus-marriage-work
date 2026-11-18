# Python Engine Quirks & Suspected Bugs (`PY_QUIRKS.md`)

Per Rule R1 ("Python is the specification. Port line by line... Calibration constants, odd branches, and suspected Python bugs are ported exactly as they are. Log suspected bugs in `PY_QUIRKS.md` and leave them in"), the following quirks and suspected bugs were identified in `kindle_render` v1.11.0 and **preserved faithfully** in the Rust port:

1. **System Font Fallback Picks Up Incompatible Debian CBDT `NotoColorEmoji.ttf` (`config.py:183`, `raster.py:310`)**:
   - `Config.resolve_font_path` searches `/usr/share/fonts/truetype/noto` after `kindle_render/fonts/`. When the repo's COLR/CPAL vector `NotoColorEmoji.ttf` is omitted, `resolve_font_path("NotoColorEmoji.ttf")` finds Debian's CBDT bitmap font at `/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf`, which has no scalable outlines and causes `FT_Set_Char_Size` to fail with FreeType error `23` (`FT_Err_Invalid_Pixel_Size`).
   - *Porting handling*: In Rust (`fonts.rs` / `raster.rs`), if a font lacks scalable outlines or `FT_Set_Char_Size` returns non-zero, it degrades gracefully to `.notdef` / fallback face per Section 6.6 instead of panicking or aborting.

2. **Dead Computation in `layout.py:make_lines` Heading Branch (`layout.py:678-689`)**:
   - In `make_lines`:
     ```python
     is_all_caps_hd = all(...)
     has_colon_long_end = (...)
     is_large_hd = any(...)
     w_last_hd = 0.65
     ```
     `is_all_caps_hd`, `has_colon_long_end`, and `is_large_hd` are computed on every heading block, and then `w_last_hd = 0.65` unconditionally overwrites the weight!
   - *Porting handling*: Ported `w_last_hd = 0.65` literally in `layout.rs`.

3. **Document-Wide `Pager._line_counter` in `GlyphCommand.line_idx` (`page.py:87, 505`)**:
   - `Pager._line_counter` increments monotonically across the entire document (`0 .. total_lines - 1`) and is stored in every `GlyphCommand.line_idx`, which is included in `PositionedPage.canonical_json()` and `layout_sha256()`. Consequently, a 1-line wrap difference in chapter `e12_scripts` (page 51 of `exam1` when CJK font is missing) shifts `line_idx` by `-1` on pages 52..70, changing their `layout_sha256()` even though their rendered pixels are 100% identical.
   - *Porting handling*: Preserved exact document-wide `_line_counter` increment order in `page.rs`.

4. **`epub.py:442` Inline `walk` Recursion Drops `outer_list` Parameter**:
   - At `epub.py:442` (the `else:` branch of `if nm in BLOCK_TAGS:` inside `walk`), the recursive call to `walk(...)` for inline elements (`<span>`, `<b>`, `<i>`, `<a>`) omits `outer_list=outer_list`, resetting `outer_list` to `None` inside inline tags.
   - *Porting handling*: Preserved exact parameter passing in `epub.rs`.

5. **`page.py:137` Uses `self.cfg.pitch` Directly Instead of `self.cfg.pitch_px()` for `<mark>` Height**:
   - In `Pager.draw_line` (`page.py:137`):
     `y1_bg = min(H, y0_bg + int(math.floor(self.cfg.pitch / 1.2)) + 1)`
     uses `self.cfg.pitch` directly (which can be `0` when default pitch ratio is used, whereas `self.cfg.pitch_px()` returns `51` or `57`).
   - *Porting handling*: Ported `self.cfg.pitch` literally in `page.rs:draw_line`.

6. **`fonts.py:194` `cpsp_xadv` and `cpsp_xplace` Overwritten by Last Subtable**:
   - In `Face._load_tables` (`fonts.py:193-195`), `self.cpsp_xadv` and `self.cpsp_xplace` are overwritten rather than accumulated across `cpsp` subtables.
   - *Porting handling*: Ported literally in `fonts.rs`.

7. **`page.py:806` Uses Outer Loop Variable `is_h` in `col_l_pad` Calculation**:
   - In `Pager.add_table` (`page.py:806`):
     ```python
     elif not has_chrome:
         lp = (17.0 if is_h else 1.0) if ci == 0 else 24.5
     ```
     Here `is_h` is leaked from the earlier loop `for ri, ci, txt, is_h, align, cs, rs in grid_cells:` (`page.py:720`) — i.e., it reflects the `is_h` of the *last cell in `grid_cells`*, not column `ci`!
   - *Porting handling*: In Python, loop variables leak into function scope; in Rust `page.rs`, we explicitly bind `last_grid_cell_is_h` from the last element of `grid_cells` so the branch evaluates identically to Python!
