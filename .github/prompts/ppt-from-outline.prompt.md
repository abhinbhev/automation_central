---
mode: ask
description: Generate a PowerPoint slide plan from a bullet-point outline
---

Turn the following outline into a structured PowerPoint slide plan.

For each slide, output:
- Slide number and title
- Key bullet points (max 5 per slide)
- Suggested visual (chart type, diagram, image description, or "none")
- Speaker notes (1-2 sentences)

Keep slides focused — one idea per slide. End with a "Next Steps" or "Summary" slide.

After generating the plan, offer to run `scripts/office/ppt_builder.py` to produce the actual file.
