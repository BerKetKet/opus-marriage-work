# Screenshot Index (`deliverables/diag/INDEX.md`)

This directory contains visual evidence captured from the physical Samsung Galaxy M30 (`SM-M305F`, Android 13) running the debug build of Opus Reader with the native Rust rendering engine (`NativeReaderEngine`).

| Filename | Screen ID | Canonical Screen Name | Verdict | Description |
|---|---|---|---|---|
| `01_app_start.png` | D02 | Home Screen | **PASS** | App startup showing search bar, "From your Library" carousel, bottom navigation bar. |
| `02_library_grid.png` | D01 | Library Grid View | **PASS** | Library tab showing 3x4 grid of seeded books, filter chips, view/sort toggles. |
| `03_library_filter_sheet.png` | D05 | Library Filter Sheet | **PASS** | Modal bottom sheet filtering books by Read Status (Read, Unread) and Content Type. |
| `04_library_view_sort_sheet.png` | D06 | Library View & Sort Sheet | **PASS** | Modal bottom sheet configuring Layout (Grid, List, Collections) and Sort criteria. |
| `05_library_list.png` | D07 | Library List View | **PASS** | Linear vertical listing of library titles with secondary metadata and action dots. |
| `06_collections_empty.png` | D08 | Collections Screen | **PASS** | Collections tab with "New Collection" creation action and list view. |
| `07_more_screen.png` | D03 | More Tab | **PASS (STUB)** | Placeholder screen for More section (slice S09 unbuilt). |
| `08_library_search.png` | — | Library Search | **PASS** | Search bar focused with soft keyboard visible, ready for query input. |
| `09_reader_open.png` | D10 | Reader Canvas (Before Fix) | **FAIL (INITIAL)** | Initial failure state when opening seeded book: solid black canvas due to missing file. |
| `10_fixture_d10.png` | D10 | Reader Canvas (Fixture Mode) | **PASS** | Simulated fixture mode displaying chrome and test layout. |
| `11_contents_toc.png` | D11 | Contents / TOC (Fixture Mode) | **PASS** | Table of contents modal showing fixture chapter list and section headers. |
| `12_reader_search.png` | D12 | In-Book Search | **PASS** | Search overlay inside reader showing query field, match count, hit snippets. |
| `13_annotations.png` | D13 | Annotations / Notebook | **PASS** | Notebook sheet showing user bookmarks, highlights, and annotations list. |
| `14_annotations_filter_sheet.png` | D14 | Annotations Filter Sheet | **PASS** | Filter bottom sheet for annotations (type, highlight color). |
| `15_annotations_sort_sheet.png` | D15 | Annotations Sort Sheet | **PASS** | Sort bottom sheet for annotations (by location, date added). |
| `16_annotations_export_sheet.png` | D16 | Annotations Export Sheet | **PASS** | Export options for notes and bookmarks (Plain Text, Markdown). |
| `17_display_settings.png` | D17–D20 | Display Settings (Aa) | **FAIL (UNBUILT)** | State when tapping Aa button: chrome remains without settings sheet (S07 unbuilt). |
| `18_exam3_page1.png` | D10 | Real EPUB Page 1 | **PASS** | First page of `kindle_exam_v3.epub` rendered by `NativeReaderEngine` ("KINDLE RENDER EXAM"). |
| `19_exam3_page_middle.png` | D10 | Real EPUB Middle Page | **PASS** | Chapter prose page of `kindle_exam_v3.epub` with anti-aliased FreeType typography. |
| `20_exam3_page_last.png` | D10 | Real EPUB Last Page | **PASS** | Final page of `kindle_exam_v3.epub` showing the last spine item and terminal text. |
| `21_exam3_toc.png` | D11 | Real EPUB Table of Contents | **PASS** | Table of contents parsed from `kindle_exam_v3.epub` (14 entries from E01 to X4). |
| `22_exam3_chapter_jump.png` | D10 | Real EPUB Chapter Jump | **PASS** | Reader view immediately after tapping "E03 Long Words and Names" in TOC. |
