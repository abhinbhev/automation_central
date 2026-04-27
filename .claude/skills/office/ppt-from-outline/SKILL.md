---
name: ppt-from-outline
description: Turn a bullet-point outline into a populated PowerPoint deck using the team template
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
- Template to use: `team-update` (default) or `project-kickoff`

## Output

**Phase 1 — Slide plan (always produced):**

For each slide:
```
Slide N: [Title]
• Bullet 1
• Bullet 2
• Bullet 3
Visual: [chart type / diagram / image suggestion / none]
Notes: [Speaker note, 1-2 sentences]
```

**Phase 2 — PowerPoint file (if script available):**

Runs `scripts/office/ppt_builder.py` to produce a `.pptx` file using the template in `templates/ppt/`.

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
5. Ask if the user wants to generate the `.pptx` file
6. If yes, call `scripts/office/ppt_builder.py` with the slide plan as JSON input
