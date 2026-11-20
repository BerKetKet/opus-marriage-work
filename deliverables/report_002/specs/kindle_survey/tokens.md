# Measured Design Tokens (`tokens.md`)
**Reference**: Official Amazon Kindle for Android (`com.amazon.kindle`)  
**Hardware Target**: Samsung Galaxy M30 (`SM-M305F`), 1080 x 2340 px, Display Density 2.625 (1 dp = 2.625 px)

---

## 1. Window & Screen Geometry

| Metric | Measured Px | Measured Dp | Notes |
|---|---|---|---|
| Display Width | 1080 px | 411.4 dp | Physical resolution |
| Display Height | 2340 px | 891.4 dp | Physical resolution |
| Status Bar (Cutout Area) | 83 px | 31.6 dp | y = 0..83 px |
| Navigation Bar | 63 px | 24.0 dp | y = 2277..2340 px |
| Reading Canvas (Chrome Hidden) | 1080 x 2340 px | 411.4 x 891.4 dp | Full-bleed from y=0 to y=2340 behind notch |

---

## 2. Reading Margins (Measured from Screen)

| Margin | Measured Px | Measured Dp | Notes |
|---|---|---|---|
| Top Margin (Cover page) | 360 px | 137.1 dp | Perfectly symmetric with bottom margin |
| Bottom Margin (Cover page) | 361 px | 137.5 dp | Centered vertically on 2340px canvas |
| Top Margin (Text page) | 176 px | 67.0 dp | Distance from y=0 to first baseline |
| Bottom Margin (Text page) | 241 px | 91.8 dp | Distance from last baseline to y=2340 |
| Left Margin | 78 px | 29.7 dp | Narrow margin setting |
| Right Margin | 77 px | 29.3 dp | Symmetrical with left margin |

---

## 3. Chrome Top Bar

| Property | Measured Value | Notes |
|---|---|---|
| Top Bar Height | 168 px (~64.0 dp) | y = 83..251 px (sits below status bar) |
| Top Bar Background | `#232323` | RGB [35, 35, 35] |
| Status Bar Background (Chrome Active) | `#232323` | Transparent status bar drawn over top bar background |
| Icon Touch Target | 74 x 71 px | Centered vertically at y=166 px |
| Back Button Bounds | `[32, 131][106, 202]` | Navigates back to Library/Home |
| Table of Contents Bounds | `[170, 131][244, 202]` | Opens TOC side sheet |
| Aa Display Settings Bounds | `[422, 131][496, 202]` | Opens Aa Display Settings sheet |
| Search Icon Bounds | `[560, 131][634, 202]` | Opens full-page Search |
| Bookmark Toggle Bounds | `[698, 131][772, 202]` | Toggles bookmark indicator |
| Notebook (Annotations) Bounds | `[836, 131][910, 202]` | Opens Notes & Highlights screen |
| Overflow (3-dots) Bounds | `[974, 131][1048, 202]` | Opens Overflow side sheet |

---

## 4. Chrome Bottom Bar & Navigation

| Property | Measured Value | Notes |
|---|---|---|
| Bottom Bar Container | `[0, 2107][1080, 2277]` | Height: 170 px (~64.8 dp) |
| Bottom Bar Background | `#232323` | Matching top bar |
| 9-Dot Thumbnail Grid Button | `[32, 2150][126, 2244]` | 94 x 94 px touch area |
| Scrubber Slider Layout | `[138, 2108][1080, 2276]` | Horizontal scrubber track |
| Scrubber Track Inactive Color | `#424242` | RGB [66, 66, 66] |
| Scrubber Track Active Color | `#90CAF9` / `#FFFFFF` | Accent highlight |
| Scrubber Thumb Diameter | 42 px (~16 dp) | Circular draggable thumb |
| Reading Progress Text Bounds | `[313, 2033][766, 2086]` | Centered above scrubber: "Page X of Y • Z%" |
| Reading Progress Font Color | `#E0E0E0` | Secondary light text |

---

## 5. Page-Flip Carousel (Card Mode)

| Property | Measured Value | Notes |
|---|---|---|
| Central Card Bounds | `[179, 456][901, 1953]` | Width: 722 px (275 dp), Height: 1497 px (570 dp) |
| Central Card Aspect Ratio | ~0.482 | Matches portrait reading page proportions |
| Card Corner Radius | 21 px (~8.0 dp) | Rounded corners |
| Left Peek Card Bounds | `[0, 456][179, 1953]` | Visible slice width: 179 px (68 dp) |
| Right Peek Card Bounds | `[901, 456][1080, 1953]` | Visible slice width: 179 px (68 dp) |
| Peek Card Dimming / Scrim | 40% Black overlay | Gives visual depth hierarchy |
| "Back to X" Return Affordance | `[40, 1867][213, 1963]` | Pill button in bottom-left above location bar |
| "Back to X" Background | `#2C2C2C` | Pill with `#FFFFFF` text |

---

## 6. 9-Dot Thumbnail Grid View

| Property | Measured Value | Notes |
|---|---|---|
| Grid Columns | 3 columns | Symmetrical 3-column vertical grid |
| Thumbnail Cell Width | 256 px (~97.5 dp) | `[70, y][326, y+419]`, etc. |
| Thumbnail Cell Height | 419 px (~159.6 dp) | Scaled canvas preview |
| Horizontal Column Gap | 87 px (~33.1 dp) | Spacing between grid columns |
| Page Label Pill Height | 61 px (~23.2 dp) | `[70, 419][326, 480]` |
| Active Page Highlight | Cyan/Gold border (3px) | "Page 3. Current Location." |

---

## 7. Overflow Side Sheet Menu

| Property | Measured Value | Notes |
|---|---|---|
| Side Sheet Container | `[424, 0][1080, 2277]` | Width: 656 px (250 dp) |
| Scrim Touch-Outside Width | `[0, 0][424, 2277]` | Width: 424 px (taps dismiss sheet) |
| Side Sheet Background | `#1E1E1E` | Material dark surface |
| Close Button Bounds | `[954, 83][1080, 209]` | Top-right cross icon |
| Menu Item Row Height | 137 px (~52.2 dp) | e.g. `[424, 209][1080, 346]` |
| Items Listed | About this book, Go to page, Annotations, Shop in Kindle store | Standard Kindle overflow list |

---

## 8. Text Selection & Annotation Toolbar

| Property | Measured Value | Notes |
|---|---|---|
| Selection Toolbar Bounds | `[73, 661][890, 838]` | Height: 177 px (~67.4 dp) |
| Action Buttons Order | Annotate, Note, Copy, Pin, Report | Left to right |
| Bottom Card Bounds | `[74, 1778][1006, 2340]` | Dictionary / Wikipedia lookup card |
| Highlight Color: Yellow | `#FFF176` | Default highlight |
| Highlight Color: Blue | `#68B6EF` | Blue highlight |
| Highlight Color: Pink | `#F48FB1` | Pink highlight |
| Highlight Color: Orange | `#FFA726` | Orange highlight |

---

## 9. Themes & Color Palette (Aa Sheet)

| Theme Name | Background Color (Hex) | Text Color (Hex) | Sampled Coordinates |
|---|---|---|---|
| White | `#FFFFFF` | `#111111` | [540, 500] in White mode |
| Sepia | `#F8F1E3` | `#5F4B32` | Sampled from Sepia theme preview |
| Green (Mint) | `#DCE8DC` | `#2A3A2A` | Sampled from Green theme preview |
| Black (Dark) | `#121212` | `#E0E0E0` | Sampled from Black theme preview |
