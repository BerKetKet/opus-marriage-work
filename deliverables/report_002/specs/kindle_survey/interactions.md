# Interaction Ledger (`interactions.md`)
**Reference**: Official Amazon Kindle for Android (`com.amazon.kindle`)  
**Hardware Target**: Samsung Galaxy M30 (`SM-M305F`)

| State ID | Element (Label, Bounds px) | Gesture | Result / Next State | Motion / Animation / Timing |
|---|---|---|---|---|
| K100 | Left Margin Zone (`[0, 0][216, 2340]`) | Tap | Turns to previous page (K102) | Instantaneous / ~80ms slide |
| K100 | Center Zone (`[216, 0][864, 2340]`) | Tap | Toggles chrome overlay shown (K101) | Slide-down top / slide-up bottom ~180ms |
| K100 | Right Margin Zone (`[864, 0][1080, 2340]`) | Tap | Turns to next page (K103) | Instantaneous / ~80ms slide |
| K100 | Reading Surface (`[0, 0][1080, 2340]`) | Horizontal Swipe Left (`900->200`) | Turns to next page (K103) | Finger tracking with momentum ~200ms |
| K100 | Reading Surface (`[0, 0][1080, 2340]`) | Horizontal Swipe Right (`200->900`) | Turns to previous page (K102) | Finger tracking with momentum ~200ms |
| K100 | Reading Progress Indicator (`[0, 2260][300, 2340]`) | Tap | Cycles footer mode: Page -> Location -> Time left in chapter -> Time left in book -> None | Text morph / fade cross-fade ~100ms |
| K100 | Word Text Body (`[300, 500]`) | Long-press (1200ms) | Selects word, reveals selection handles, toolbar and lookup card (K140) | Popup fade-in ~150ms |
| K101 | Back Button (`[32, 131][106, 202]`) | Tap | Exits reader to Library / Home | Shared element / slide exit ~250ms |
| K101 | Table of Contents (`[170, 131][244, 202]`) | Tap | Opens TOC navigation screen (K132) | Slide-in from left ~200ms |
| K101 | Display Settings Aa (`[422, 131][496, 202]`) | Tap | Opens Aa Display Settings bottom sheet (K120) | Slide-up bottom sheet ~250ms |
| K101 | In-Book Search (`[560, 131][634, 202]`) | Tap | Opens full-screen search input with keyboard (K134) | Fade-in with keyboard reveal ~200ms |
| K101 | Bookmark Button (`[698, 131][772, 202]`) | Tap | Toggles ribbon bookmark on current page (K111) | Bookmark ribbon drop animation ~150ms |
| K101 | Notebook / Notes (`[836, 131][910, 202]`) | Tap | Opens Annotations list screen (K133) | Slide-in from right ~200ms |
| K101 | Overflow Menu 3-dots (`[974, 131][1048, 202]`) | Tap | Opens Overflow side sheet menu (K112) | Slide-in from right ~220ms |
| K101 | 9-Dot Thumbnail Grid (`[32, 2150][126, 2244]`) | Tap | Opens 3-column thumbnail bird's-eye view (K131) | Zoom-out transform ~200ms |
| K101 | Scrubber Slider Track (`[138, 2108][1080, 2276]`) | Horizontal Drag | Enters Page-Flip card carousel mode (K130) | Fluid page card shrink and side peeks ~180ms |
| K112 | About This Book (`[424, 209][1080, 346]`) | Tap | Opens metadata modal dialog | Dialog pop-in ~150ms |
| K112 | Go To Page (`[424, 346][1080, 483]`) | Tap | Opens numeric page input dialog | Dialog pop-in ~150ms |
| K112 | Annotations (`[424, 483][1080, 712]`) | Tap | Navigates to Notebook annotations list (K133) | Slide-in ~200ms |
| K112 | Close Menu (`[954, 83][1080, 209]`) | Tap | Closes overflow side sheet, restores chrome | Slide-out to right ~180ms |
| K112 | Scrim Outside (`[0, 0][424, 2277]`) | Tap | Dismisses overflow menu | Slide-out to right ~180ms |
| K120 | Font Tab (`[0, 1118][270, 1265]`) | Tap | Displays Font family, size, spacing controls | Tab cross-fade ~100ms |
| K120 | Layout Tab (`[270, 1118][540, 1265]`) | Tap | Displays Page color themes (White, Sepia, Green, Black), margins (K121) | Tab cross-fade ~100ms |
| K120 | Themes Tab (`[540, 1118][810, 1265]`) | Tap | Displays preset themes (Compact, Standard, Large, Custom) (K122) | Tab cross-fade ~100ms |
| K120 | More Tab (`[810, 1118][1080, 1265]`) | Tap | Displays Assistive reader, reading ruler, progress cycle options | Tab cross-fade ~100ms |
| K120 | Backdrop / Tap Outside (`[0, 0][1080, 1118]`) | Tap | Dismisses Aa bottom sheet, keeps reader page updated live | Slide-down bottom sheet ~200ms |
| K130 | Central Card (`[179, 456][901, 1953]`) | Tap | Selects page and zooms into full reading view | Zoom-in expansion ~220ms |
| K130 | Left / Right Peek Cards | Drag | Smoothly scrolls cards horizontally with snap | Spring physics snapping ~150ms |
| K130 | Back to Return Affordance (`[40, 1867][213, 1963]`) | Tap | Returns to initial locator before scrubber was moved | Jump animation ~180ms |
| K131 | Thumbnail Cell (`[413, 772][668, 1326]`) | Tap | Jumps to tapped page in reading view | Zoom-in transition ~200ms |
| K132 | TOC Chapter Row (`[21, 565][969, 613]`) | Tap | Jumps reader directly to selected chapter locator | Slide-out TOC and page render ~200ms |
| K140 | Annotate Button (`[73, 661][272, 838]`) | Tap | Expands color palette picker (Yellow, Blue, Pink, Orange) (K141) | Dropdown expand ~120ms |
| K140 | Note Button (`[293, 661][420, 838]`) | Tap | Opens note text editor modal | Keyboard slide-up ~200ms |
| K140 | Copy Button (`[441, 661][568, 838]`) | Tap | Copies selected text to system clipboard, dismisses selection | Toast "Copied" ~100ms |
| K140 | Dismiss Selection (`[0, 0][1080, 2340]`) | Tap outside | Clears text highlight and dismisses lookup card | Fade-out ~120ms |
