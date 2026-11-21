# Interaction Ledger (`interactions.md`)
**Reference**: Official Amazon Kindle for Android (`com.amazon.kindle`)  
**Hardware Target**: Samsung Galaxy M30 (`SM-M305F`)

| State ID | Element (Label, Bounds px) | Gesture | Result / Next State | Motion / Animation / Timing |
|---|---|---|---|---|
| K100 | Left Margin Zone (`[0, 0][216, 2340]`) | Tap | Turns to previous page (K102) | Instantaneous / 133 ms (measured 4 frames) |
| K100 | Center Zone (`[216, 0][864, 2340]`) | Tap | Toggles chrome overlay shown (K101) | Slide-down top / slide-up bottom 167 ms (measured 6 frames) |
| K100 | Right Margin Zone (`[864, 0][1080, 2340]`) | Tap | Turns to next page (K103) | Instantaneous / 133 ms (measured 4 frames) |
| K100 | Reading Surface (`[0, 0][1080, 2340]`) | Horizontal Swipe Left (`900->200`) | Turns to next page (K103) | Finger tracking with momentum ~200ms (est) |
| K100 | Reading Surface (`[0, 0][1080, 2340]`) | Horizontal Swipe Right (`200->900`) | Turns to previous page (K102) | Finger tracking with momentum ~200ms (est) |
| K100 | Reading Progress Indicator (`[0, 2260][300, 2340]`) | Tap | Cycles footer mode: Page -> Location -> Time left in chapter -> Time left in book -> None | Text morph / fade cross-fade ~100ms (est) |
| K100 | Word Text Body (`[300, 500]`) | Long-press (1200ms) | Selects word, reveals selection handles, toolbar and lookup card (K140) | Popup fade-in ~150ms (est) |
| K101 | Back Button (`[32, 131][106, 202]`) | Tap | Exits reader to Library / Home | Shared element / slide exit ~250ms (est) |
| K101 | Table of Contents (`[170, 131][244, 202]`) | Tap | Opens TOC navigation screen (K132) | Slide-in from left ~200ms (est) |
| K101 | Display Settings Aa (`[422, 131][496, 202]`) | Tap | Opens Aa Display Settings bottom sheet (K120) | Instant / 0 ms (measured 1 frame) |
| K101 | In-Book Search (`[560, 131][634, 202]`) | Tap | Opens full-screen search input with keyboard (K134) | Fade-in with keyboard reveal ~200ms (est) |
| K101 | Bookmark Button (`[698, 131][772, 202]`) | Tap | Toggles ribbon bookmark on current page (K111) | Bookmark ribbon drop animation ~150ms (est) |
| K101 | Notebook / Notes (`[836, 131][910, 202]`) | Tap | Opens Annotations list screen (K133) | Slide-in from right ~200ms (est) |
| K101 | Overflow Menu 3-dots (`[974, 131][1048, 202]`) | Tap | Opens Overflow side sheet menu (K112) | Slide-in from right ~220ms (est) |
| K101 | 9-Dot Thumbnail Grid (`[32, 2150][126, 2244]`) | Tap | Opens 3-column thumbnail bird's-eye view (K131) | Zoom-out transform ~200ms (est) |
| K101 | Scrubber Slider Track (`[138, 2108][1080, 2276]`) | Horizontal Drag | Enters Page-Flip card carousel mode (K130) | Fluid page card shrink and side peeks ~180ms (est) |
| K112 | About This Book (`[424, 209][1080, 346]`) | Tap | Opens metadata modal dialog | Dialog pop-in ~150ms (est) |
| K112 | Go To Page (`[424, 346][1080, 483]`) | Tap | Opens numeric page input dialog | Dialog pop-in ~150ms (est) |
| K112 | Annotations (`[424, 483][1080, 712]`) | Tap | Navigates to Notebook annotations list (K133) | Slide-in ~200ms (est) |
| K112 | Close Menu (`[954, 83][1080, 209]`) | Tap | Closes overflow side sheet, restores chrome | Slide-out to right ~180ms (est) |
| K112 | Scrim Outside (`[0, 0][424, 2277]`) | Tap | Dismisses overflow menu | Slide-out to right ~180ms (est) |
| K120 | Font Tab (`[0, 1118][270, 1265]`) | Tap | Displays Font family, size, spacing controls | Tab cross-fade ~100ms (est) |
| K120 | Layout Tab (`[270, 1118][540, 1265]`) | Tap | Displays Page color themes (White, Sepia, Green, Black), margins (K121) | Tab cross-fade ~100ms (est) |
| K120 | Themes Tab (`[540, 1118][810, 1265]`) | Tap | Displays preset themes (Compact, Standard, Large, Custom) (K122) | Tab cross-fade ~100ms (est) |
| K120 | More Tab (`[810, 1118][1080, 1265]`) | Tap | Displays Assistive reader, reading ruler, progress cycle options | Tab cross-fade ~100ms (est) |
| K120 | Backdrop / Tap Outside (`[0, 0][1080, 1118]`) | Tap | Dismisses Aa bottom sheet, keeps reader page updated live | Slide-down bottom sheet ~200ms (est) |
| K130 | Central Card (`[179, 456][901, 1953]`) | Tap | Selects page and zooms into full reading view | Zoom-in expansion ~220ms (est) |
| K130 | Left / Right Peek Cards | Drag | Smoothly scrolls cards horizontally with snap | Spring physics snapping ~150ms (est) |
| K130 | Back to Return Affordance (`[40, 1867][213, 1963]`) | Tap | Returns to initial locator before scrubber was moved | Jump animation ~180ms (est) |
| K131 | Thumbnail Cell (`[413, 772][668, 1326]`) | Tap | Jumps to tapped page in reading view | Zoom-in transition ~200ms (est) |
| K132 | TOC Chapter Row (`[21, 565][969, 613]`) | Tap | Jumps reader directly to selected chapter locator | Slide-out TOC and page render ~200ms (est) |
| K140 | Annotate Button (`[73, 661][272, 838]`) | Tap | Expands color palette picker (Yellow, Blue, Pink, Orange) (K141) | Dropdown expand ~120ms (est) |
| K140 | Note Button (`[293, 661][420, 838]`) | Tap | Opens note text editor modal | Keyboard slide-up ~200ms (est) |
| K140 | Copy Button (`[441, 661][568, 838]`) | Tap | Copies selected text to system clipboard, dismisses selection | Toast "Copied" ~100ms (est) |
| K140 | Dismiss Selection (`[0, 0][1080, 2340]`) | Tap outside | Clears text highlight and dismisses lookup card | Fade-out ~120ms (est) |

---

## Empirical Kindle Tap-Zone Probing Table
Empirical probing at y = 1200 on Samsung Galaxy M30 (`SM-M305F`, 1080x2340):

| x Probe (px) | Width % | Observed Action | Diff Pixels | Zone Classification |
|---|---|---|---|---|
| 20 | 1.8% | NO_ACTION (diff=0px) | 0 px | Bezel deadzone (0..100px) |
| 100 | 9.3% | NO_ACTION (diff=0px) | 0 px | Bezel deadzone (0..100px) |
| 200 | 18.5% | PREV_PAGE (diff=247477px) | 247,477 px | Left zone (0..216px, 20%) |
| 230 | 21.3% | TOGGLE_CHROME | 345,316 px | Center zone (216..864px, 60%) |
| 540 | 50.0% | TOGGLE_CHROME | 345,316 px | Center zone (216..864px, 60%) |
| 850 | 78.7% | TOGGLE_CHROME | 345,316 px | Center zone (216..864px, 60%) |
| 870 | 80.6% | NEXT_PAGE (diff=247477px) | 247,477 px | Right zone (>864px, 20%) |
| 1000 | 92.6% | NEXT_PAGE (diff=414131px) | 414,131 px | Right zone (>864px, 20%) |
| 1060 | 98.1% | NEXT_PAGE (diff=337818px) | 337,818 px | Right zone (>864px, 20%) |

The 20 / 60 / 20 zone split is empirically validated:
- Left zone: 0..216 px (20% of 1080px)
- Center zone: 216..864 px (60% of 1080px)
- Right zone: 864..1080 px (20% of 1080px)

---

## Measured Motion Timings (Host `motion_measure.py`)
Recorded with `adb shell screenrecord` at 60 fps; 6 recordings in `motion/` (all < 2 MB):

| Transition | Kindle Duration | Opus Reader Duration | Recordings Analyzed | Note |
|---|---|---|---|---|
| Chrome Toggle | 167 ms (6 frames) | 0 ms (1 frame) | `kindle_chrome_toggle.mp4` (290 KB), `opus_chrome_toggle.mp4` (318 KB) | Kindle slides top/bottom bars; Opus toggles Compose state instantly |
| Tap Page Turn | 133 ms (4 frames) | 0 ms (1 frame) | `kindle_tap_page_turn.mp4` (36 KB), `opus_tap_page_turn.mp4` (141 KB) | Kindle performs smooth page turn transition; Opus renders next page immediately |
| Aa Sheet Open | 0 ms (1 frame) | 0 ms (1 frame) | `kindle_aa_sheet_open.mp4` (180 KB), `opus_aa_sheet_open.mp4` (90 KB) | Both render sheet instantly upon event dispatch |
| Thumbnails Open | ~200 ms (est) | ~180 ms (est) | N/A (unrecorded) | Marked `est` per instructions |
