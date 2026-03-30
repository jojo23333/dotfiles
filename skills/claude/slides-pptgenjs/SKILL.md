---
name: slides-pptgenjs
description: This skill should be used when the user asks to create, recreate, edit, debug, or validate an editable PowerPoint deck (`.pptx`) with PptxGenJS, including screenshot or PDF recreation, chart or diagram slides, and layout or font troubleshooting.
version: 1.0.0
---

# Slides PptxGenJS

Create editable PowerPoint decks with PptxGenJS. Keep the authored output in JavaScript and deliver both the `.pptx` and the source `.js` unless the user asked for something narrower.

## Overview

- Use PptxGenJS for deck generation.
- Avoid `python-pptx` for authoring unless the task is inspection-only.
- Keep work in a task-local directory and move only validated artifacts to the final destination.

## Bundled resources

- `assets/pptxgenjs_helpers/`: Copy this helper folder into the deck workspace and import it locally instead of reimplementing layout logic.
- `scripts/render_slides.py`: Rasterize a `.pptx` or `.pdf` to per-slide PNGs.
- `scripts/slides_test.py`: Detect content that leaks beyond the slide canvas.
- `scripts/create_montage.py`: Build a contact-sheet montage from rendered slides.
- `scripts/detect_font.py`: Report missing or substituted fonts during rendering.
- `scripts/ensure_raster_image.py`: Convert SVG, EMF, HEIC, or PDF-like assets into PNGs for inspection.
- `references/pptxgenjs-helpers.md`: Load when helper API details or dependency notes are needed.

## Workflow

1. Inspect the request and classify it as new deck creation, deck recreation, or deck editing.
2. Set slide size first. Default to 16:9 (`LAYOUT_WIDE`) unless the source clearly uses another aspect ratio.
3. Copy `assets/pptxgenjs_helpers/` into the working directory and import helpers from there.
4. Build the deck in JavaScript with explicit theme fonts, stable spacing, and native PowerPoint elements when practical.
5. Render the result with `render_slides.py`, review the PNGs, and fix layout issues before delivery.
6. Run `slides_test.py` when the layout is dense or elements run close to slide edges.
7. Deliver the `.pptx`, the authoring `.js`, and any required generated assets.

## Authoring rules

- Set theme fonts explicitly instead of relying on PowerPoint defaults.
- Use `autoFontSize`, `calcTextBox`, and related helpers instead of PptxGenJS `fit` or `autoFit`.
- Use bullet options, not literal `•` characters.
- Use `imageSizingCrop` or `imageSizingContain` instead of PptxGenJS built-in image sizing.
- Use `latexToSvgDataUri()` for equations and `codeToRuns()` for syntax-highlighted code blocks.
- Prefer native PowerPoint charts for simple visuals that users may want to edit later.
- For diagrams that PptxGenJS cannot express well, render SVG externally and place the SVG in the slide.
- Include both `warnIfSlideHasOverlaps(slide, pptx)` and `warnIfSlideElementsOutOfBounds(slide, pptx)` whenever generating or substantially editing slides.
- Fix all unintended overlap and out-of-bounds warnings before delivery. If an overlap is intentional, leave a short code comment nearby.

## Recreate or edit existing slides

- Render the source deck or reference PDF first for geometric comparison.
- Match the original aspect ratio before rebuilding layout.
- Preserve editability where possible: text stays text, simple charts stay native charts.
- If a reference slide uses awkward raster or vector artwork, use `ensure_raster_image.py` to create debug PNGs before placement.

## Validation commands

Examples below assume the needed scripts were copied into the working directory. Otherwise invoke them from this skill folder.

```bash
python3 scripts/render_slides.py deck.pptx --output_dir rendered
python3 scripts/create_montage.py --input_dir rendered --output_file montage.png
python3 scripts/slides_test.py deck.pptx
python3 scripts/detect_font.py deck.pptx --json
```

Load `references/pptxgenjs-helpers.md` when helper API details or dependency requirements matter.
