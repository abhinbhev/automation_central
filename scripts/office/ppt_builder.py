"""Build an HTML presentation from a JSON slide plan.

Usage:
    python ppt_builder.py --plan slides.json --output presentation.html
    python ppt_builder.py --plan slides.json --template team-update --output deck.html

The JSON plan format:
[
  {
    "title": "Slide Title",
    "bullets": ["Bullet 1", "Bullet 2", "Bullet 3"],
    "notes": "Speaker note text",
    "visual": "bar chart / image / none"
  }
]

Templates: place an HTML file in templates/ppt/ — the builder reads its
<style> block (and optional layout structure) as an aesthetic reference.
Falls back to a clean built-in theme if no template is found.
"""

import json
import re
from pathlib import Path

import typer
from jinja2 import Environment, BaseLoader
from rich.console import Console

app = typer.Typer()
console = Console()

TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates" / "ppt"

# ── Built-in fallback theme ──────────────────────────────────────────────

FALLBACK_CSS = """\
:root {
  --bg: #ffffff;
  --text: #1a1a2e;
  --accent: #e94560;
  --accent-light: #f5f5f5;
  --font: 'Segoe UI', system-ui, -apple-system, sans-serif;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; font-family: var(--font); color: var(--text); background: var(--bg); }

/* Slide container */
.slide-deck { width: 100%; }
.slide {
  width: 100%; min-height: 100vh;
  display: flex; flex-direction: column; justify-content: center;
  padding: 6vh 8vw; page-break-after: always;
}
.slide-number {
  position: absolute; top: 2vh; right: 3vw;
  font-size: 0.85rem; color: #999;
}

/* Title slide */
.slide.title-slide { text-align: center; }
.slide.title-slide h1 { font-size: 3rem; margin-bottom: 0.5em; color: var(--accent); }
.slide.title-slide .subtitle { font-size: 1.3rem; color: #666; }

/* Content slide */
.slide h2 { font-size: 2rem; margin-bottom: 1em; color: var(--accent); border-bottom: 3px solid var(--accent); padding-bottom: 0.3em; }
.slide ul { list-style: none; padding: 0; }
.slide ul li {
  font-size: 1.25rem; padding: 0.5em 0 0.5em 1.5em;
  position: relative; line-height: 1.5;
}
.slide ul li::before {
  content: ''; position: absolute; left: 0; top: 0.85em;
  width: 8px; height: 8px; background: var(--accent); border-radius: 50%;
}
.slide .visual-note {
  margin-top: 1.5em; padding: 1em;
  background: var(--accent-light); border-left: 4px solid var(--accent);
  font-style: italic; color: #555; border-radius: 0 6px 6px 0;
}
.slide .speaker-notes {
  margin-top: auto; padding-top: 2em;
  font-size: 0.85rem; color: #999; border-top: 1px solid #eee;
}

/* Navigation */
.nav-bar {
  position: fixed; bottom: 0; left: 0; right: 0;
  display: flex; justify-content: center; gap: 1em;
  padding: 1em; background: rgba(255,255,255,0.95);
  border-top: 1px solid #eee; z-index: 100;
}
.nav-bar button {
  padding: 0.5em 1.5em; border: 2px solid var(--accent);
  background: white; color: var(--accent); border-radius: 6px;
  cursor: pointer; font-size: 0.9rem; font-weight: 600;
  transition: all 0.2s;
}
.nav-bar button:hover { background: var(--accent); color: white; }
.nav-bar .slide-counter { line-height: 2.4; color: #666; }

@media print {
  .nav-bar { display: none; }
  .slide { min-height: auto; page-break-after: always; padding: 2cm; }
}
"""

PRESENTATION_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ title }}</title>
<style>
{{ css }}
</style>
</head>
<body>
<div class="slide-deck">
{% for slide in slides %}
<div class="slide{% if loop.first %} title-slide{% endif %}" id="slide-{{ loop.index }}">
  <span class="slide-number">{{ loop.index }} / {{ slides | length }}</span>
{% if loop.first and not slide.bullets %}
  <h1>{{ slide.title }}</h1>
  {% if slide.notes %}<p class="subtitle">{{ slide.notes }}</p>{% endif %}
{% else %}
  <h2>{{ slide.title }}</h2>
  {% if slide.bullets %}
  <ul>
    {% for b in slide.bullets %}<li>{{ b }}</li>
    {% endfor %}
  </ul>
  {% endif %}
  {% if slide.visual and slide.visual != 'none' %}
  <div class="visual-note">📊 Visual: {{ slide.visual }}</div>
  {% endif %}
  {% if slide.notes %}
  <div class="speaker-notes">🗣️ {{ slide.notes }}</div>
  {% endif %}
{% endif %}
</div>
{% endfor %}
</div>

<div class="nav-bar">
  <button onclick="navigate(-1)">← Prev</button>
  <span class="slide-counter" id="counter">1 / {{ slides | length }}</span>
  <button onclick="navigate(1)">Next →</button>
</div>

<script>
(function() {
  let current = 0;
  const slides = document.querySelectorAll('.slide');
  const counter = document.getElementById('counter');
  const total = slides.length;

  function show(idx) {
    current = Math.max(0, Math.min(idx, total - 1));
    slides.forEach((s, i) => s.style.display = i === current ? 'flex' : 'none');
    counter.textContent = (current + 1) + ' / ' + total;
  }
  show(0);

  window.navigate = function(dir) { show(current + dir); };
  document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); navigate(1); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); navigate(-1); }
  });
})();
</script>
</body>
</html>
"""


def extract_template_css(template_path: Path) -> str | None:
    """Extract <style> content from an HTML template file."""
    content = template_path.read_text(encoding="utf-8")
    match = re.search(r"<style[^>]*>(.*?)</style>", content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def resolve_template(template_name: str) -> str:
    """Resolve a template name to CSS. Checks for .html files in templates/ppt/."""
    html_candidate = TEMPLATES_DIR / f"{template_name}.html"
    if html_candidate.exists():
        extracted = extract_template_css(html_candidate)
        if extracted:
            console.print(f"[green]Using template aesthetic from {html_candidate.name}[/green]")
            return extracted
        console.print(f"[yellow]Template '{html_candidate.name}' has no <style> block — using default theme.[/yellow]")
        return FALLBACK_CSS

    # Check for any matching file (user might drop .pptx — we can't extract CSS but
    # we let them know the new system expects .html templates)
    pptx_candidate = TEMPLATES_DIR / f"{template_name}.pptx"
    if pptx_candidate.exists():
        console.print(
            f"[yellow]Found '{pptx_candidate.name}' but HTML builder needs .html templates.\n"
            f"  Place an HTML template at {html_candidate} for aesthetic reference.\n"
            f"  Using default theme.[/yellow]"
        )
        return FALLBACK_CSS

    console.print(f"[dim]No template '{template_name}' found in {TEMPLATES_DIR} — using default theme.[/dim]")
    return FALLBACK_CSS


def build_deck(plan: list[dict], template_name: str, output_path: Path) -> None:
    css = resolve_template(template_name)
    deck_title = plan[0].get("title", "Presentation") if plan else "Presentation"

    env = Environment(loader=BaseLoader(), autoescape=True)
    tmpl = env.from_string(PRESENTATION_TEMPLATE)
    html = tmpl.render(title=deck_title, css=css, slides=plan)

    output_path.write_text(html, encoding="utf-8")


@app.command()
def main(
    plan: Path = typer.Option(..., help="Path to JSON slide plan file"),
    output: Path = typer.Option(..., help="Output .html file path"),
    template: str = typer.Option("team-update", help="Template name from templates/ppt/ (.html file)"),
) -> None:
    """Build an HTML presentation from a JSON slide plan."""
    if not plan.exists():
        console.print(f"[red]Plan file not found:[/red] {plan}")
        raise typer.Exit(1)

    slides = json.loads(plan.read_text(encoding="utf-8"))
    if not isinstance(slides, list):
        console.print("[red]Plan file must be a JSON array of slide objects.[/red]")
        raise typer.Exit(1)

    console.print(f"Building {len(slides)}-slide HTML presentation using template '{template}'...")
    build_deck(slides, template, output)
    console.print(f"[green]✓ Presentation saved to {output}[/green]")


if __name__ == "__main__":
    app()
