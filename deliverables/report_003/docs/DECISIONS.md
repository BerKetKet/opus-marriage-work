# Decisions Log (`DECISIONS.md`) - Report 003 New Decisions

Decisions recorded during Report 003 execution under Manager Instructions 002.

---

## D12. Retraction of Report 002 Black Screen Regression Claim (Task T1)
- **Settled**: Retract the conclusion from Report 002 that the bitmap LRU cache caused a black screen on middle pages.
- **Reason & Evidence**: Empirical testing of 7 distinct middle pages across White (mean ~233-245) and Black themes (stddev ~41-58) proved the bitmap cache functions correctly without recycled exceptions or eviction failures. The black screenshot was captured during initial EPUB load (~7.1s transition duration) combined with the `#000000` page background of the Black theme.

## D13. Profile Alignment for 42 px Normal Geometry (Task T4)
- **Settled**: Added `exam3_p42` to `render.engine/tools/profiles.json` to configure `size26=2688 / pitch=57` for `kindle_exam_v3.epub`.
- **Reason & Evidence**: In Opus Reader UI, "Normal 42 px" corresponds to `size26=2688 / pitch=57`. `profiles.json` previously lacked a 42 px profile for EPUB v3 (its `exam3_normal` profile was configured with `size26=2880 / pitch=68`, which corresponds to UI preset 3 "Large 45 px"). Generating the 42 px reference established identical 67-page counts across Phone, Rust, and Python.

## D14. Identification of Missing English Hyphenation Asset on Android (Task T4)
- **Settled**: Identified that the 85 vs 82 page count discrepancy on `exam3_normal` is caused by missing English hyphenation in Android assets combined with `kr-core` hardcoding local disk path lookups for `hyph_en_YJ.bin`.
- **Reason & Evidence**: Asset facts dumped by `connectedDebugAndroidTest` confirmed `hyph_en` was not loaded on the phone. Furthermore, `kr-core/src/api.rs` stores bytes in `mem_hyphen_bins` but never reads them, while `layout.rs` hardcodes disk path `kindle_render/hyph_en_YJ.bin`. Running container Rust with `--no-hyphen` expands page count to 85, exactly matching the phone.

## D15. Isolation of Non-Visual `glyph_name` Layout Hash Divergence (Task T4)
- **Settled**: Confirmed that the layout hash difference between Rust and Python on pages with identical pixel rendering is caused solely by `commands[i].glyph_name` formatting.
- **Reason & Evidence**: Running `ir_diff.py` across 30 pages (first 10 pages of `exam3_small`, `exam3_normal`, and `tables_images`) showed 28/28 mismatching pages differed solely at `commands[i].glyph_name` (`glyph00217` in Rust vs `C` in Python).
