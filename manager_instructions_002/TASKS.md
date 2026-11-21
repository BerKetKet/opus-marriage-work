# TASKS for report 003 (instructions 002)

Order: T0, T1, T2, T3, T4, T5. If budget runs short, drop in this order: T3 timings, T4 step 3, T3 gap rows that need new screens. Never drop T0, T1, T5.
Rules for every task: smallest change that fixes a demonstrated problem; obey `opus-reader/AGENTS.md` and `GUARD OK`; commit per task; no push; every screenshot unique and described; every before/after claim goes in `screenshots/PAIRS.tsv` (before<TAB>after<TAB>minimum changed pixels); blank is an error unless the description starts with `EXPECTED-BLANK:`.

## T0. Housekeeping and errata
1. Replace your `tools_manager/make_report.py` with `scripts/make_report.py` from this zip; add `pixel_diff.py` and `motion_measure.py`.
2. Rewrite `BLOCKERS.md`: delete the obsolete sandbox blockers (no Rust compiler, no Gradle); keep only blockers that still exist today, each with date, evidence and next step.
3. In `REPORT.md` add an "Errata to report 002" section stating what was retracted (items 1-4 of the verdict) and fix the wording "Kotlin renderer" to "native Rust engine (JNI)".
4. `TODO_ISSUES.md`: add these as new issues with measured numbers and a screenshot each (log only, do not fix in 002): 004 text-size reflow takes about 7.1 s for the test book; 005 Thumbnails sheet shows only 2 pages for an 85 page book (check whether it is lazy loading, a cap, or a bug, one hour max); 006 Aa sheet has 2 tabs, Kindle has 4 (Font, Layout, Themes, More); 007 top bar height 160 px vs Kindle 168 px. Set Issue 001 status to "PARTLY (cover page proven; middle-page proof pending T1)".

## T1. Why is the middle page black? (possible regression: highest priority)
Open `kindle_exam_v3.epub` at the default setting, chrome hidden, go to about page 40 (scrubber or taps), screenshot.
1. Reproduce on current HEAD. Take three middle pages (about 20, 40, 60) in the White theme and the same three in the Black theme, chrome hidden, each as its own screenshot. Also page 40 with chrome shown.
2. If any is black or text-less: find the cause with evidence. Test these hypotheses in order and record the result of each: (a) black text on a black page (theme colours not applied to the engine bitmap, check `PageTheme` flow into `nativeRender`); (b) bitmap recycled or evicted by the new LRU cache while it is still being drawn (check logcat for `recycled`, `Canvas: trying to use a recycled bitmap`, exceptions in draw); (c) the T2 inset/edge-to-edge change moved or clipped the bitmap (compare with the commit before `369ad4c` using a temporary worktree build); (d) the screenshot was taken during load or a page transition (take it 3 s after the last input and again 6 s later).
3. Fix the cause. If it is the cache, add a behaviour test that fails before the fix (a page is drawn after eviction pressure) and passes after.
4. Compare at least two of the working middle pages with the Python reference of the same page and geometry using `pixel_diff.py` (geometry setup is in `specs/ENGINE_INVESTIGATION.md`, section 1) and report identical percentage. This also tells you whether the app places the bitmap exactly like the engine.
Done when: six distinct non-blank middle-page screenshots (3 White, 3 Black) and the root cause stated with evidence, or "not reproducible" with the evidence of each hypothesis test.

## T2. Redo the import proof
1. Use a book that is NOT already in the library and has a visibly different title: `kindle_exam_v1.epub` (check the library list first; if present, remove nothing, pick `kindle_tables_images_exam.epub`).
2. Switch the library to LIST view (titles visible). Screenshots: list before, picker with the file visible, list after (new title visible), the book opened to its first real text page (not a cover placeholder), the same book reopened after force-stop at the saved position.
3. `PAIRS.tsv` must contain list-before to list-after with a minimum of 3000 changed pixels. Also run `pixel_diff.py` on them and paste its line in `REPORT.md`.
4. Explain `t3_imported_book_reading.png` (Android icon): what screen is it, and why did it appear? Also test importing the same file twice and importing a corrupt file (truncate a copy to 20 KB): screenshot what the user sees each time.
Done when: the new title is visible in the library list after import, the book reads, errors are handled with a visible message; or FAIL with logcat evidence.

## T3. Repair the gap analysis evidence
1. For rows K102, K103, K105, K140, K141, K142 in `specs/kindle_survey/gap_analysis.md`: take real Opus screenshots with the same book and locator: tap-turn before/after pair, swipe-turn before/after pair, the footer (is there a footer in reading mode with chrome hidden? screenshot), long-press selection with toolbar, highlight created with colour, dictionary/lookup (what appears). Each must pass `make_report.py` checks. If a behaviour is not present or does not work, the verdict is MISSING or FAIL, with the screenshot of what actually happens.
2. Reclassify every row where the evidence was the black screenshot. Do not keep WORKS without a valid image.
3. Timings: for chrome toggle, page turn by tap, Aa sheet open, thumbnails open, on BOTH Kindle and Opus: record with `adb shell screenrecord --time-limit 6`, measure with `motion_measure.py` (host has ffmpeg; if not, say so and label every number `est`). Replace the `~xxx ms` values in `interactions.md` and `tokens.md` with measured values and the number of recordings used, or mark them `est`. Keep at most 6 small mp4 files (under 2 MB each) in `specs/kindle_survey/motion/`.
4. Add the probing evidence for the Kindle tap zones (taps at x = 20, 100, 200, 230, 540, 850, 870, 1000, 1060; one line each: result). The 20/60/20 split in the table must come from this, not from assumption.
Done when: every gap row has a valid image or an honest FAIL/MISSING/NOT RUN, and no timing is unlabeled.

## T4. Engine investigation: why does the phone show a different page count than the PC?
Follow `specs/ENGINE_INVESTIGATION.md` step by step. Deliver `ENGINE_INVESTIGATION.md` with the tables defined there. Do not change the Python engine. You may fix the Rust engine or the app only if the root cause is proven and the fix is small; then re-run the Rust gates (P1, P2, P3 tools and `parity_check.py` in the container) and report counts before/after.
Done when: for each of the three presets (Small 34 px, Normal 42 px, Large 45 px) there is one table row with: pages on phone, pages from Rust in the container, pages from Python in the container, the first page where phone and container Rust differ (or "identical"), and the first page where container Rust and Python differ, plus a root-cause statement for each difference or "unexplained, evidence in X".

## T5. Report 003
Build `opus_marriage_work_worker_report_003.zip` with the v2 script as in `NEXT_REPORT_REQUIREMENTS.md`. Commit first. The script must exit 0; if it refuses, fix the evidence, not the script.
