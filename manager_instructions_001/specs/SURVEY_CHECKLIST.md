# Survey checklist (IDs are suggestions; keep them stable)

Tier P1 = reader (mandatory). P2 = library. P3 = the rest. Tick each as captured; write "N/A: not present" where the app has no such item.

## P1: Reader (K1xx)
Reading view
- [ ] K100 page, chrome hidden: full screen (system bars hidden), measured margins left/right/top/bottom in px, bounds on
- [ ] K101 chrome shown: top bar and bottom bar (positions, heights, all icons with their labels/content descriptions)
- [ ] K102 tap zones: left edge, right edge, centre (what each tap does, zone widths measured by probing taps at several x positions)
- [ ] K103 page turn by tap and by swipe (motion recording; direction; duration; what is under the page while turning)
- [ ] K104 first page (cover) and last page behaviour, end-of-book screen if any (do not use store actions)
- [ ] K105 status/clock/battery overlay or footer text in reading view, and the reading-progress label: tap it, record every cycle state (page x of y / location / time left in chapter / time left in book / percent)
Top bar
- [ ] K110 each top-bar control: back, contents/notebook, search, Aa, bookmark, overflow, any others: result of tapping each
- [ ] K111 bookmark add and remove: indicator, animation, long-press behaviour
- [ ] K112 overflow menu: every item listed (do not execute destructive/store/share items; open only safe ones)
Aa display sheet
- [ ] K120 Aa sheet, every tab or section reached (Theme/Font/Layout/More or whatever exists): full capture of each
- [ ] K121 themes: every theme preview captured with the reader behind it applied (all theme names, background and text colors as hex)
- [ ] K122 brightness and any slider: track, thumb sizes, value feedback
- [ ] K123 font family list, size control (steps, min/max, how it reflows), bold, line spacing steps, margins options, alignment, orientation lock, any "more options"
- [ ] K124 how the sheet closes (tap outside, drag down, back) and whether the page behind updates live
Navigation
- [ ] K130 page-flip carousel (tap centre then the card strip): drag, snap behaviour, card sizes and spacing, location label, scrubber thumb, "go back to where you were" affordance
- [ ] K131 thumbnail grid (the 9-dot view): layout, tap behaviour
- [ ] K132 contents screen: tabs, rows, nesting, current chapter marker, jump behaviour
- [ ] K133 notebook / bookmarks / highlights list: tabs, empty state, row layout, filter, sort, export options present
- [ ] K134 in-book search: entry, results list layout, hit highlighting on the page, result navigation, clear, empty result
Text interaction
- [ ] K140 long-press selection: handles, toolbar buttons (all of them, in order), highlight colours, note, dictionary, translate, share, search; selection across lines and pages
- [ ] K141 highlight created: look on the page for each colour (hex), tap on an existing highlight (popup contents), note editor, delete behaviour (only on a highlight you created in this survey, then remove it)
- [ ] K142 dictionary/translation popup, footnote popup, link tap (internal and external), image tap/zoom
- [ ] K143 any hint/coach mark/first-run tooltip

## P2: Library (K2xx)
- [ ] K200 library home (grid) with bounds; K201 list view; K202 view & sort sheet; K203 filter sheet; K204 collections; K205 library search (empty, typing, results); K206 book long-press menu (list items only; do not run them); K207 empty states; K208 top bar and bottom navigation bar (icons, labels, selected state)

## P3: Everything else (K3xx)
- [ ] K300 settings screens that do not show personal data (reading settings, general); K301 notification or sync UI present in the reader only; K302 anything else reachable from the overflow or bottom navigation that is safe to open

## Deliverable check per captured state
Capture id with screenshot and XML (or note), wireframe + element table, interaction lines, token measurements, gap-analysis row.
