---
mode: agent
description: Generate an HTML presentation from a bullet-point outline
---

Turn the following outline into a complete, presentation-ready slide plan.

## Step 1 — Understand the presentation

Before planning slides, establish:
- **Audience:** technical team, executive stakeholders, external client, or mixed?
- **Goal:** inform, persuade, request approval, or share results?
- **Tone:** formal, conversational, data-driven, or narrative?
- **Length:** infer slide count from the outline depth; ask if unclear

If any of the above are not obvious from the outline, ask before proceeding.

## Step 2 — Produce the Slide Plan

Structure the deck as: **Opening → Context → Body → Takeaways → Close**

For every slide, produce the full block below — no skipping fields:

```
### Slide [N]: [Title]
**Layout:** [Title only | Title + bullets | Title + image | Two-column | Full-bleed visual | Quote | Data table]
**Headline message:** [One sentence — the single takeaway a reader gets from this slide alone]

**Bullets:**
- [max 5 bullets; max 8 words each; start with a verb or noun, not filler]
- ...

**Visual:**
- Type: [bar chart | line chart | pie chart | table | diagram | screenshot | icon set | photo | none]
- Description: [What it shows, what the axes/labels are, what story it tells]
- Data needed: [List the data points or variables required to build this visual]

**Speaker notes:**
[3–5 sentences. Cover: what to say that isn't on the slide, the "so what", any anticipated questions, and a transition to the next slide.]

**Design notes:**
[Colour emphasis, animation suggestion (e.g. "reveal bullets one at a time"), callout box, or "none"]
```

## Step 3 — Deck-level checklist

After listing all slides, output:
- **Narrative thread:** one paragraph describing the story arc across the deck
- **Slides to watch:** flag any slide that risks being too dense, too vague, or losing the audience
- **Missing content:** list anything the outline implies but didn't provide (data, a definition, a decision)
- **Total slide count and estimated presentation time** (assume ~2 min/slide)

## Step 4 — Confirm before building

Present the full plan in an md. Ask:
1. Are the slide order and topics correct?
2. Are there slides to add, remove, or merge?
3. Any branding or template preference? (builder checks `templates/ppt/` for a matching `.html` file)

**Do not build until the user explicitly confirms.**

## Step 5 — Build

Once confirmed, run `scripts/office/ppt_builder.py` to produce a self-contained HTML file with keyboard navigation, viewable in any browser.

## Design rules (always enforce)
- One idea per slide — if a slide needs two headlines, split it
- No bullet point longer than 8 words — force ruthless summarisation
- Every slide must earn its place: if removing it doesn't break the story, cut it
- Data slides must answer "so what?" in the headline — never title a chart slide "Q1 Results"
- The last slide is always a clear call-to-action or decision ask — never "Thank You" alone
