---
mode: ask
description: Generate an HTML presentation from a bullet-point outline
---

Turn the following outline into a structured presentation slide plan.

For each slide, output:
- Slide number and title
- Key bullet points (max 5 per slide)
- Suggested visual (chart type, diagram, image description, or "none")
- Speaker notes (1-2 sentences)

Keep slides focused — one idea per slide. End with a "Next Steps" or "Summary" slide.

**Important:** Present the slide plan first and wait for user confirmation before building. Ask if they want any changes to the topics, order, or content.

Once confirmed, run `scripts/office/ppt_builder.py` to produce a self-contained HTML file. The user can optionally specify a template name — the builder checks `templates/ppt/` for a matching `.html` file to use as an aesthetic reference.
