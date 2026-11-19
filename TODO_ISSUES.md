# Known Issues & Defect Tracker (`TODO_ISSUES.md`)

**Date**: 2026-11-19  
**Device**: Samsung Galaxy M30 (`SM-M305F`), TrebleDroid GSI Android 13 (`arm64-v8a`, 1080x2340 @ 420 dpi)  
**Reporting Workflow**: Antigravity Worker AI $\leftrightarrow$ Claude Manager & Quality Control AI  

---

## Issue 001: Non-Immersive Fullscreen in Reading Mode (System Bars Visible / Content Pushed Down)

- **Paired Screenshots**:
  - Our App Cover: [issue_001_cover_page.png](file:///home/bgg/projects/opus_marriage_work/deliverables/diag/issue_001_cover_page.png)
  - Real Kindle Cover: [issue_002_kindle_cover_fullscreen_ref.png](file:///home/bgg/projects/opus_marriage_work/deliverables/diag/issue_002_kindle_cover_fullscreen_ref.png)
  - Real Kindle Reading Page with Layout Bounds: [issue_001_kindle_page_margins_bounds.png](file:///home/bgg/projects/opus_marriage_work/deliverables/diag/issue_001_kindle_page_margins_bounds.png)
- **User Description**:
  > "i have enabled layout bounds to be shown in dev settings... that is a page in the real app. and notice the status bar is hidden and the top of the screen is considered part of the reading page which is why the bottom and top marigins are symmetrical. unlike ours which even while hiding the status bar , shifts lower and displays a black bar where the status bar would have been. this is issue 1"
- **Defect Summary**:
  - In Kindle, reading mode is true edge-to-edge fullscreen extending to the very top edge ($y = 0$). The top of the screen is part of the reading page viewport, yielding vertically symmetrical top and bottom margins.
  - In Opus Reader, even when the system bars are set to hidden, the viewport is shifted downward and leaves an unrendered black bar in place of the status bar, breaking margin symmetry and pushing the cover page and text downward.

---

## Issue 002: Page Flip Carousel Differences (Cannot Scroll, Page Sizing & Excessive Vertical Spacing)

- **Paired Screenshots**:
  - Real Kindle Reference: [issue_002_kindle_page_flip_carousel.png](file:///home/bgg/projects/opus_marriage_work/deliverables/diag/issue_002_kindle_page_flip_carousel.png)
  - Our App (Chrome Active / Page Flip): [issue_002_our_app_chrome_page_bounds.png](file:///home/bgg/projects/opus_marriage_work/deliverables/diag/issue_002_our_app_chrome_page_bounds.png)
- **User Description**:
  > "look now, kindle when touching the middle of a book reading panel, displays the "pages" side by side which you can smoothly scroll sideways"
  > "look now at ours. you cant scroll and the page sizes ... and that ever present layout issue ..."
- **Defect Summary**:
  - **Cannot Scroll**: In Kindle, the horizontal page carousel can be dragged and smoothly scrolled sideways to browse pages. In Opus Reader, the side-by-side preview is completely static and cannot be scrolled or paged horizontally.
  - **Page Card Sizing**: In our app, the central card and adjacent thumbnail cards have incorrect sizing and aspect ratio constraints compared to the book's native geometry, making the text look disproportionate.
  - **Layout & Vertical Inset Waste**: In our app, there is massive dead vertical space between the top bar, the floating chapter title ("E01 The Ferryman's Almanac"), the carousel cards, the location label, and the bottom scrubber bar. Combined with the status bar inset issue, the layout feels uncalibrated and disjointed.
---

## Issue 003: Unresponsive Top Action Buttons & Visual Divergence from Kindle UI

- **Referenced Screenshot**:
  - Our App (Chrome Active): [issue_002_our_app_chrome_page_bounds.png](file:///home/bgg/projects/opus_marriage_work/deliverables/diag/issue_002_our_app_chrome_page_bounds.png)
- **User Description**:
  > "in this same page you can see there are many buttons some of which look completely different to the original and the buttons on top that are supposed to bring up settings dont even respond. i dont even know if we have a light mode , the themes, layout options. this is why i say our app isnt nearly well designed enough"
- **Defect Summary**:
  - **Unresponsive Controls**: Top bar action buttons (notably the "Aa" display settings icon, search, and bookmark buttons) fail to respond or invoke their respective bottom sheets during regular reading sessions.
  - **Visual Divergence & Feature Gaps**: Button icons, weights, and placements diverge visibly from Kindle's canonical design. Controls for light/sepia/dark themes, margins, font sizing, and layout options are either hidden, non-functional, or not discoverable in the UI.

---

# Strategic Recommendations for Manager AI (Claude)

## Request for Comprehensive Reference App Survey & Wireframing

- **User Directive**:
  > "please inform the manager ai in your next report the importance of a survey and a wireframe of the original app .. i d like it to have you collect screenshots of the original app exploring every element to know what every interaction does"
- **Proposal for Next Task Batch**:
  1. **Systematic Kindle UI Audit**: Instruct the worker agent to drive an exhaustive exploratory survey of the official Kindle app on the connected device (`SM-M305F`).
  2. **Comprehensive Capture Suite**: Capture high-resolution screenshots with layout bounds enabled across all states:
     - Top bar actions & overflow menus.
     - "Aa" Display Settings sheets (themes, font families, font sizes, line spacing, margins, reading alignment).
     - Page Flip continuous card scrubber & 9-dot thumbnail grid view.
     - Table of Contents, Bookmark list, and Annotation / Notebook sheets.
     - In-book search and search results navigation.
  3. **Interaction & Behavior Spec**: Synthesize the captured data into a canonical reference wireframe and interaction specification so Opus Reader development has unambiguous ground truth for every UI component and interaction model.
