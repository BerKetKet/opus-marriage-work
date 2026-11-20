# Protocol: survey of the official Kindle app (reference for Opus Reader)

Purpose: ground truth for every screen, element and interaction, so the Opus Reader UI is built from measurements, not memory. The app is on the owner's phone (adb model SM-M305F, 1080x2340, density 2.625 so 1 dp = 2.625 px).

## Safety rules (hard)
1. Read-only survey. Do NOT purchase, borrow, download, delete, archive, sign out, share, rate, or change account, sync, notification or store settings. Do not open Account, Payment, Store checkout or any screen showing personal details; stop at the screen's entrance, capture that one screen only if it carries no personal data.
2. Display settings (theme, font, size, spacing, margins, brightness, orientation lock...) ARE changed during the survey. BEFORE the first change record every initial value with screenshots (`RESTORE_LOG.md`), and at the end restore them exactly and screenshot the restored state.
3. Use the book already used for the owner's exam captures (`KINDLE RENDER EXAM`, the v3 test book) if it is in the Kindle library; otherwise any book whose chapters have a table of contents. Do not capture other books' text beyond what a screen needs; the report zip is shared only with the manager.
4. Do not paste screenshots or text of the survey anywhere except into the report zip.

## Method
1. Wake the phone, disable auto-rotate, keep portrait. Keep the screen awake (`adb shell svc power stayon usb`).
2. For every state: bring the app to that state with real gestures (`adb shell input tap/swipe/keyevent`; `adb shell input swipe x1 y1 x2 y2 duration_ms` for drags; long-press = `swipe` with the same start and end and 800 ms). Find tap targets from a `uiautomator dump` of the current screen, not from guessing.
3. Capture with `survey_capture.py` (screenshot + XML + index). Use the ID scheme in the checklist. For key P1 states also capture a layout-bounds image (`--suffix _bounds`): turn on "Show layout bounds" in Developer options (the owner has used it before) and turn it off again afterwards.
4. For each tappable element: tap it once, record what happens (new state id, or "no visible change"), then return. Write one line per element in `interactions.md`: `id | element (label, bounds px) | gesture | result | animation/time`.
5. Motion: record transitions with `adb shell screenrecord --time-limit 6 /sdcard/x.mp4`, pull, and describe in words: direction, duration (count frames if `ffmpeg` is available: `ffmpeg -i x.mp4 -vf fps=30 f_%03d.png`), easing (fast-start, linear...). Keep the mp4 only if small (under 3 MB each, at most 5 files) and name them `motion_<what>.mp4`.
6. Measurements (`tokens.md`): from XML bounds and from the screenshots: sizes and positions in px and dp; colors sampled as hex from specific pixels (give the pixel coordinates) for background, text, bars, dividers, selection, highlight colors, scrubber track and thumb, accent; for EVERY theme in the Aa sheet; icon sizes and stroke weights; corner radii; spacing between elements; text sizes estimated from glyph heights (say it is an estimate and how it was measured); the UI typeface if recognisable. Include page margins in the reading view and the position of the page content relative to the screen edges.
7. Wireframes: run `xml_to_wireframe.py` for each captured XML; add a one-paragraph annotation per state in `wireframes/<id>.md` (below the table the script writes): purpose, entry, exits, notable behaviour.
8. If `uiautomator dump` fails or is blank for a screen, capture the screenshot with `--no-xml`, measure bounds from the image, and say so.
9. Behaviour that depends on state (first use hints, tooltips, coach marks) should be captured once as they appear; note that they are one-time.

## Gap analysis (`gap_analysis.md`)
One row per Kindle state: `Kindle id | Kindle screenshot | Opus equivalent screen | Opus screenshot (take it with the same book and locator) | WORKS / DIFFERS / MISSING | the three most important differences`. Use measured numbers for DIFFERS (for example "top bar height 168 px vs 144 px").

## Quality bar (the manager will check)
- No two captures may have identical content (the script warns); if a state really looks the same as another, say why in the index notes.
- Every claim in `interactions.md` must point to a capture id.
- Say "not present in this app version" when an item in the checklist does not exist; do not skip silently.
- Partial but correct beats complete but invented. Write results as you go.
