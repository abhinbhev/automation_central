---
name: ppt-from-outline
description: Turn a bullet-point outline into an HTML presentation using an optional aesthetic template
domain: office
requires_script: true
script: scripts/office/ppt_builder.py
---

## Usage

Invoke with `/ppt-from-outline` then provide:
- A bullet-point or numbered outline of the presentation content
- Presentation title and date
- Target audience (team / management / exec / external)
- Desired number of slides (optional — will be inferred from outline if not given)
- Template to use: name of an `.html` file in `templates/ppt/` (e.g. `team-update`). Falls back to a clean default theme.

### Templates

Users can place HTML or PPTX template files in `templates/ppt/`. The builder reads the `<style>` block from HTML templates as an aesthetic reference for the generated presentation. If only a `.pptx` file is provided, it will guide the user to create an HTML counterpart.

Example: drop `corporate-brand.html` in `templates/ppt/` and specify `--template corporate-brand`.

## Output

**Phase 1 — Slide plan (always produced first, requires user confirmation):**

For each slide:
```
Slide N: [Title]
• Bullet 1
• Bullet 2
• Bullet 3
Visual: [chart type / diagram / image suggestion / none]
Notes: [Speaker note, 1-2 sentences]
```

Present the plan and ask the user to confirm or request changes before proceeding.

**Phase 2 — HTML presentation (after user approval):**

Runs `scripts/office/ppt_builder.py` to produce a self-contained `.html` file with:
- Keyboard navigation (arrow keys, spacebar)
- Slide counter and prev/next buttons
- Print-friendly CSS (`@media print` with page breaks)
- Template-based styling when a template is provided

## Slide Design Rules

- One idea per slide
- Max 5 bullets per slide; max 8 words per bullet
- First slide: title + date + presenter name
- Last slide: "Next Steps" or "Summary" or "Thank You"
- Charts: use for comparisons, trends, proportions — not for single numbers
- Avoid walls of text

## Steps

1. Analyse the outline and group content into logical slides
2. For each group: write a title (noun phrase or question), extract 3-5 key bullets, suggest a visual
3. Add speaker notes with context the presenter would say but not show
4. Output the full slide plan
5. **Wait for user confirmation** — ask if they want changes before building
6. Once confirmed, call `scripts/office/ppt_builder.py` with the slide plan as JSON input
7. The output is a standalone `.html` file the user can open in any browser
