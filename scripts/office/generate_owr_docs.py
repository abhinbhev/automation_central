"""Generate OWR + HLR Word documents for the 3 ADO features.

Reads docs/156057-*.md, docs/156061-*.md, docs/156063-*.md and produces
styled .docx files in docs/ following the OWR+HLR document template pattern.

Usage:
    python scripts/office/generate_owr_docs.py
    python scripts/office/generate_owr_docs.py --out-dir docs/word
"""

from __future__ import annotations

from pathlib import Path

import typer
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt, RGBColor, Inches
from rich.console import Console

app = typer.Typer()
console = Console()

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = REPO_ROOT / "docs"

# ABI brand colours
YELLOW = RGBColor(0xF5, 0xC5, 0x18)   # ABI gold/yellow
DARK   = RGBColor(0x1A, 0x1A, 0x2E)   # near-black
MID    = RGBColor(0x4A, 0x4A, 0x6A)   # mid grey-blue
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GREY = RGBColor(0xF2, 0xF2, 0xF2)
HEADER_BG  = RGBColor(0x1A, 0x1A, 0x2E)


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------

def _set_cell_bg(cell, rgb: RGBColor) -> None:
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    hex_color = f"{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def _set_run_color(run, rgb: RGBColor) -> None:
    run.font.color.rgb = rgb


def _add_horizontal_rule(doc: Document) -> None:
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    pb = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "F5C518")
    pb.append(bottom)
    pPr.append(pb)
    p.paragraph_format.space_after = Pt(6)


# ---------------------------------------------------------------------------
# Document builders
# ---------------------------------------------------------------------------

def _add_cover_header(doc: Document, feature_id: str, title: str, status: str, owner: str, version: str, updated: str) -> None:
    """Dark banner header with title and metadata strip."""
    # Title paragraph with dark background simulation via shading on a table
    tbl = doc.add_table(rows=2, cols=1)
    tbl.style = "Table Grid"

    # Row 0 — title banner
    title_cell = tbl.rows[0].cells[0]
    _set_cell_bg(title_cell, HEADER_BG)
    title_para = title_cell.paragraphs[0]
    title_para.clear()
    run = title_para.add_run(f"OWR + HLR")
    run.bold = True
    run.font.size = Pt(10)
    _set_run_color(run, YELLOW)
    title_para.add_run("\n")
    run2 = title_para.add_run(title)
    run2.bold = True
    run2.font.size = Pt(16)
    _set_run_color(run2, WHITE)
    title_para.paragraph_format.space_before = Pt(10)
    title_para.paragraph_format.space_after = Pt(10)
    title_para.paragraph_format.left_indent = Inches(0.2)

    # Row 1 — metadata strip
    meta_cell = tbl.rows[1].cells[0]
    _set_cell_bg(meta_cell, LIGHT_GREY)
    meta_para = meta_cell.paragraphs[0]
    meta_para.clear()
    meta_text = f"ADO Feature: {feature_id}   |   Status: {status}   |   Owner: {owner}   |   Version: {version}   |   Last updated: {updated}"
    run3 = meta_para.add_run(meta_text)
    run3.font.size = Pt(8)
    run3.font.color.rgb = MID
    meta_para.paragraph_format.space_before = Pt(4)
    meta_para.paragraph_format.space_after = Pt(4)
    meta_para.paragraph_format.left_indent = Inches(0.2)

    doc.add_paragraph()


def _add_section1_table(doc: Document, fields: dict[str, str]) -> None:
    """Section 1 — Product Brief info table."""
    tbl = doc.add_table(rows=1, cols=2)
    tbl.style = "Table Grid"
    tbl.columns[0].width = Inches(2.0)
    tbl.columns[1].width = Inches(4.5)

    hdr = tbl.rows[0].cells
    for cell in hdr:
        _set_cell_bg(cell, HEADER_BG)
    hdr[0].paragraphs[0].clear()
    r = hdr[0].paragraphs[0].add_run("Field")
    r.bold = True; r.font.size = Pt(9); _set_run_color(r, WHITE)
    hdr[1].paragraphs[0].clear()
    r = hdr[1].paragraphs[0].add_run("Value")
    r.bold = True; r.font.size = Pt(9); _set_run_color(r, WHITE)

    for key, val in fields.items():
        row = tbl.add_row().cells
        row[0].paragraphs[0].clear()
        rk = row[0].paragraphs[0].add_run(key)
        rk.bold = True; rk.font.size = Pt(9)
        row[1].paragraphs[0].clear()
        rv = row[1].paragraphs[0].add_run(val)
        rv.font.size = Pt(9)

    doc.add_paragraph()


def _add_heading(doc: Document, text: str, level: int = 1) -> None:
    style_map = {1: "Heading 1", 2: "Heading 2", 3: "Heading 3"}
    p = doc.add_heading(text, level=level)
    # Tint H1 with brand yellow accent
    if level == 1:
        for run in p.runs:
            run.font.color.rgb = DARK
    if level == 2:
        for run in p.runs:
            run.font.color.rgb = MID


def _add_table(doc: Document, headers: list[str], rows: list[list[str]]) -> None:
    if not headers:
        return
    tbl = doc.add_table(rows=1, cols=len(headers))
    tbl.style = "Table Grid"

    hdr_cells = tbl.rows[0].cells
    for i, h in enumerate(headers):
        _set_cell_bg(hdr_cells[i], HEADER_BG)
        hdr_cells[i].paragraphs[0].clear()
        r = hdr_cells[i].paragraphs[0].add_run(h)
        r.bold = True
        r.font.size = Pt(9)
        _set_run_color(r, WHITE)

    for row_data in rows:
        row_cells = tbl.add_row().cells
        for i, val in enumerate(row_data):
            if i < len(row_cells):
                row_cells[i].paragraphs[0].clear()
                r = row_cells[i].paragraphs[0].add_run(str(val))
                r.font.size = Pt(9)

    doc.add_paragraph()


def _add_bullet_list(doc: Document, items: list[str], bold_prefix: str | None = None) -> None:
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(2)
        if bold_prefix and item.startswith(bold_prefix):
            parts = item.split(":", 1)
            if len(parts) == 2:
                run = p.add_run(parts[0] + ":")
                run.bold = True
                run.font.size = Pt(9)
                run2 = p.add_run(parts[1])
                run2.font.size = Pt(9)
                continue
        run = p.add_run(item)
        run.font.size = Pt(9)


_PHASE_GOALS = {
    "Phase 1": "Ensure problem, scope, business intent, and ownership are clear before any solutioning.",
    "Phase 2": "Lock meaning, logic, and constraints before design.",
    "Phase 3": "Validate hypotheses and decision flow with real users.",
    "Phase 4": "Define MVP scope, non-goals, and dependencies before engineering starts.",
    "Phase 5": "Confirm design decisions match business rules before any build begins.",
    "Phase 6": "Ensure engineering has everything needed to start — no ambiguity on scope, states, or criteria.",
    "Phase 7": "Communicate the release and limitations to all affected stakeholders.",
    "Phase 8": "Confirm the feature works as intended in production and inform next iteration.",
}


def _add_checklist_section(doc: Document, phase: str, items: list[str], required_output: str) -> None:
    _add_heading(doc, phase, level=3)
    for key, goal in _PHASE_GOALS.items():
        if key in phase:
            p = doc.add_paragraph()
            r = p.add_run("Goal: ")
            r.bold = True
            r.font.size = Pt(9)
            r2 = p.add_run(goal)
            r2.font.size = Pt(9)
            r2.italic = True
            p.paragraph_format.space_after = Pt(4)
            break
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        run = p.add_run(f"☐  {item}")
        run.font.size = Pt(9)
        p.paragraph_format.space_after = Pt(2)
    p = doc.add_paragraph()
    run = p.add_run("Required output: ")
    run.bold = True
    run.font.size = Pt(9)
    run2 = p.add_run(required_output)
    run2.font.size = Pt(9)
    run2.italic = True
    doc.add_paragraph()


# ---------------------------------------------------------------------------
# Document specs
# ---------------------------------------------------------------------------

def _build_156057(doc: Document) -> None:
    """ADO 156057 — Product Analytics (IC Component Tracking)."""
    _add_cover_header(
        doc,
        feature_id="156057 — Product Analytics",
        title="Product Analytics (IC Component Tracking)",
        status="DRAFT",
        owner="POS IC X OneWay",
        version="0.1",
        updated="2026-04-30",
    )

    # Section 1
    _add_heading(doc, "Section 1 — Product Brief")
    _add_section1_table(doc, {
        "ADO Feature": "156057 — Product Analytics",
        "Area Path": "Generative AI Products \\ POS IC X OneWay",
        "Target Date": "TBD",
        "Document Status": "DRAFT",
        "Team Members": "TBD",
        "Design File": "TBD",
        "ADO Backlog": "https://dev.azure.com/ab-inbev-analytics",
    })

    _add_horizontal_rule(doc)

    # Section 2
    _add_heading(doc, "Section 2 — Feature Body")

    _add_heading(doc, "Objective", level=2)
    _add_bullet_list(doc, [
        "Implement comprehensive Google Analytics 4 (GA4) tracking for all user interactions with the IC (Insights Copilot / 'Ask OneWay AI') component in OneWay.",
        "Enable product managers to measure adoption, understand usage patterns, identify popular features, and improve the product based on data-driven insights.",
        "Track 21 distinct user interaction events across the full IC component lifecycle — from first impression through feedback and conversation management.",
    ])
    doc.add_paragraph()

    _add_heading(doc, "Success Metrics", level=2)
    _add_table(doc,
        headers=["Goal", "Metric"],
        rows=[
            ["Adoption", "ic_component_visible event fires once per new user (lifetime deduplication)"],
            ["Engagement", "Volume of ic_component_open / ic_component_close events over time"],
            ["Engagement", "Distribution of chat_submitted by mode (FAQ, Smart Flow, enter_key, button_click)"],
            ["Engagement", "Volume of chat_submitted with a conversation_id (follow-up rate)"],
            ["Outcome", "chat_response_received breakdown by status (SUCCESS / FAILURE / ABANDONED)"],
            ["Outcome", "track_feedback volume and feedback_sentiment (true / false) ratio"],
            ["Outcome", "track_feedback_submit options_count distribution (depth of feedback)"],
            ["Business Impact", "Data-driven product decisions enabled by full funnel GA4 event coverage"],
        ]
    )

    _add_heading(doc, "Assumptions", level=2)
    _add_heading(doc, "Features in scope", level=3)
    _add_bullet_list(doc, [
        "All 21 GA4 event scenarios defined in the acceptance criteria",
        "IC component within the OneWay application only",
        "currentProjectKey hardcoded to gai_copilot_marketing_brand_guidance_ghq for all events",
    ])
    _add_heading(doc, "Technical approach", level=3)
    _add_bullet_list(doc, [
        "Use Google Analytics 4 (GA4) event tracking via gtag.js or analytics.js",
        "conversation_id and chat_id extracted from Clara API responses",
        "ic_component_visible fired once per user — deduplicated via localStorage or cookie",
        "conversation_id propagated through all follow-up messages in a session",
    ])
    _add_heading(doc, "Data scope", level=3)
    _add_table(doc,
        headers=["Dimension", "Value"],
        rows=[
            ["Brands", "All brands using the IC component in OneWay"],
            ["Regions", "All regions where OneWay is deployed"],
            ["Channels", "Web (OneWay application)"],
            ["Periods", "From release date onwards"],
            ["Granularity", "Per user interaction event"],
        ]
    )

    _add_heading(doc, "Milestones", level=2)
    _add_table(doc,
        headers=["Milestone", "Date"],
        rows=[
            ["ADO Feature created", "—"],
            ["Development start", "TBD"],
            ["QA / validation", "TBD"],
            ["Release", "TBD"],
        ]
    )

    _add_heading(doc, "Requirements", level=2)
    p = doc.add_paragraph()
    r = p.add_run("Event catalogue — all events must fire with ")
    r.font.size = Pt(9)
    r2 = p.add_run("currentProjectKey = gai_copilot_marketing_brand_guidance_ghq")
    r2.bold = True; r2.font.size = Pt(9)
    doc.add_paragraph()

    _add_table(doc,
        headers=["Event Name", "Trigger", "Key Parameters"],
        rows=[
            ["ic_component_visible", "IC component first renders on screen", "currentProjectKey — fires once per user lifetime"],
            ["ic_component_open", "User opens the 'Ask OneWay AI' panel", "currentProjectKey — fires every open"],
            ["ic_component_close", "User closes the 'Ask OneWay AI' panel", "currentProjectKey — fires every close"],
            ["chat_submitted", "User submits via FAQ (landing page)", "currentProjectKey, mode=FAQ, conversation_id (follow-up only)"],
            ["chat_submitted", "User selects Smart Flow from landing page", "currentProjectKey, mode=is_smartflow_landing_page, smartflow_function, conversation_id (follow-up only)"],
            ["chat_submitted", "User selects Smart Flow from chat bar", "currentProjectKey, mode=is_smartflow_chatbar, smartflow_function, conversation_id (follow-up only)"],
            ["chat_submitted", "User submits via Enter key", "currentProjectKey, mode=enter_key, conversation_id (follow-up only)"],
            ["chat_submitted", "User clicks Send button", "currentProjectKey, mode=button_click, conversation_id (follow-up only)"],
            ["chat_response_received", "Clara returns a successful response (task_status=success)", "currentProjectKey, conversation_id, chat_id, status=SUCCESS"],
            ["chat_response_received", "Clara fails to respond (task_status=failure)", "currentProjectKey, conversation_id, chat_id, status=FAILURE"],
            ["chat_response_received", "Response abandoned (task_status=abandoned)", "currentProjectKey, conversation_id, chat_id, status=ABANDONED"],
            ["track_new_chat", "User clicks 'New Chat' icon", "currentProjectKey"],
            ["track_feedback", "User clicks 👍", "currentProjectKey, feedback_sentiment=true, source=thumbs_icon"],
            ["track_feedback", "User clicks 👎", "currentProjectKey, feedback_sentiment=false, source=thumbs_icon"],
            ["track_feedback_submit", "User submits positive feedback options", "currentProjectKey, sentiment=true, options (comma-separated), options_count (0–6)"],
            ["track_feedback_submit", "User submits negative feedback options", "currentProjectKey, sentiment=false, options (comma-separated), options_count (0–4)"],
            ["rename_button_click", "User clicks Rename button", "currentProjectKey, conversation_id"],
            ["rename_text_change", "User confirms new conversation name", "currentProjectKey, conversation_id"],
            ["delete_confirm_button_click", "User clicks Confirm on delete modal", "currentProjectKey, conversation_id"],
            ["delete_cancel_button_click", "User clicks Cancel on delete modal", "currentProjectKey, conversation_id"],
            ["copy_code_button_click", "User clicks Copy icon on a code block", "currentProjectKey, conversation_id"],
        ]
    )

    _add_heading(doc, "Business rules", level=3)
    _add_bullet_list(doc, [
        "ic_component_visible — once per user lifetime (localStorage / cookie gate)",
        "conversation_id — propagated from first message through all follow-ups in session",
        "Positive feedback options_count: 0–6 (Accuracy, Relevance, Visuals, Completion, Language, Others)",
        "Negative feedback options_count: 0–4 (Accuracy, Relevance, Completion, Others)",
        "chat_submitted mode enum: FAQ | is_smartflow_landing_page | is_smartflow_chatbar | enter_key | button_click",
        "chat_response_received status enum: SUCCESS | FAILURE | ABANDONED (from task_status in Clara API)",
    ])

    _add_heading(doc, "Out of Scope", level=2)
    _add_bullet_list(doc, [
        "Custom GA4 dashboards or report configuration",
        "Tracking outside the IC component (e.g., standard OneWay navigation events)",
        "Server-side event tracking — client-side only via gtag.js / analytics.js",
        "Cross-project currentProjectKey dynamic configuration",
        "Integration with non-GA4 analytics platforms",
    ])

    _add_heading(doc, "Design", level=2)
    _add_table(doc,
        headers=["Artefact", "Link"],
        rows=[["Design file", "TBD"], ["Event schema reference", "TBD"]]
    )

    _add_heading(doc, "User Flows", level=3)

    _add_heading(doc, "Flow 1 — First visit and panel open/close", level=3)
    _add_bullet_list(doc, [
        "User loads a OneWay page containing the IC component for the first time.",
        "IC component renders → ic_component_visible fires once; stored in localStorage to prevent re-firing.",
        "User clicks 'Ask Clara >' to open the panel → ic_component_open fires.",
        "User closes the panel → ic_component_close fires.",
        "On subsequent page loads: ic_component_visible does NOT fire again (localStorage gate active).",
    ])

    _add_heading(doc, "Flow 2 — Chat submission and response", level=3)
    _add_bullet_list(doc, [
        "User opens the IC panel (ic_component_open fires).",
        "User selects a FAQ prompt on the landing page → chat_submitted fires with mode=FAQ.",
        "  OR user selects a Smart Flow from the landing page → chat_submitted fires with mode=is_smartflow_landing_page and smartflow_function.",
        "  OR user selects a Smart Flow from the chat bar → chat_submitted fires with mode=is_smartflow_chatbar and smartflow_function.",
        "  OR user types a message and presses Enter → chat_submitted fires with mode=enter_key.",
        "  OR user types a message and clicks Send → chat_submitted fires with mode=button_click.",
        "Clara processes the query.",
        "Clara returns a successful response → chat_response_received fires with status=SUCCESS, conversation_id, chat_id.",
        "  OR Clara fails to respond → chat_response_received fires with status=FAILURE.",
        "  OR user navigates away before response arrives → chat_response_received fires with status=ABANDONED.",
        "User sends a follow-up message → chat_submitted fires again, this time including conversation_id.",
    ])

    _add_heading(doc, "Flow 3 — Feedback submission", level=3)
    _add_bullet_list(doc, [
        "User receives a Clara response.",
        "User clicks 👍 → track_feedback fires with feedback_sentiment=true, source=thumbs_icon.",
        "  OR user clicks 👎 → track_feedback fires with feedback_sentiment=false, source=thumbs_icon.",
        "Feedback options panel appears.",
        "User selects one or more options and submits → track_feedback_submit fires with sentiment, options (comma-separated), and options_count.",
        "  Positive options_count range: 0–6 (Accuracy, Relevance, Visuals, Completion, Language, Others).",
        "  Negative options_count range: 0–4 (Accuracy, Relevance, Completion, Others).",
    ])

    _add_heading(doc, "Flow 4 — Conversation management", level=3)
    _add_bullet_list(doc, [
        "User clicks the New Chat icon → track_new_chat fires with currentProjectKey.",
        "User opens conversation history and clicks '...' next to a conversation.",
        "User clicks Rename → rename_button_click fires with conversation_id.",
        "User confirms the new name → rename_text_change fires with conversation_id.",
        "User clicks Delete → delete modal appears.",
        "User clicks Confirm → delete_confirm_button_click fires with conversation_id.",
        "  OR user clicks Cancel → delete_cancel_button_click fires with conversation_id.",
        "User receives a response containing a code block and clicks the Copy icon → copy_code_button_click fires with conversation_id.",
    ])

    _add_table(doc,
        headers=["Flow", "Key Events fired", "Deduplication / Notes"],
        rows=[
            ["First visit", "ic_component_visible", "Once per user lifetime — localStorage gate"],
            ["Panel open/close", "ic_component_open, ic_component_close", "Every open and close"],
            ["Chat submission", "chat_submitted", "mode enum required; conversation_id on follow-ups only"],
            ["Response received", "chat_response_received", "status: SUCCESS / FAILURE / ABANDONED"],
            ["Feedback", "track_feedback, track_feedback_submit", "sentiment + options_count per submission"],
            ["Conversation mgmt", "track_new_chat, rename_*, delete_*, copy_code_button_click", "All carry conversation_id except track_new_chat"],
        ]
    )

    _add_heading(doc, "Open Questions", level=2)
    _add_table(doc,
        headers=["Question", "Answer", "Date Answered"],
        rows=[
            ["Which GA4 property / measurement ID?", "—", "—"],
            ["localStorage or cookie for ic_component_visible — and what TTL?", "—", "—"],
            ["Who owns the GA4 property and validates event receipt?", "—", "—"],
            ["Is conversation_id available on the first API response or follow-up only?", "—", "—"],
        ]
    )

    _add_heading(doc, "Change & Request Log", level=2)
    _add_table(doc,
        headers=["Request / Update", "Requestor / Personnel", "Date"],
        rows=[["Initial draft created from ADO 156057", "—", "2026-04-30"]]
    )

    _add_heading(doc, "Reference Links", level=2)
    _add_bullet_list(doc, [
        "ADO Feature 156057: https://dev.azure.com/ab-inbev-analytics",
        "GA4 Event tracking: https://developers.google.com/analytics/devguides/collection/ga4/events",
    ])

    _add_horizontal_rule(doc)

    # Section 3
    _add_heading(doc, "Section 3 — Discovery → Delivery Checklist")

    _add_checklist_section(doc, "Phase 1 — Discovery Framing & Alignment", [
        "Problem statement defined: measure IC component adoption and usage via GA4",
        "Business intent confirmed: data-driven product improvements for IC",
        "Scope agreed: 21 events, client-side, GA4, OneWay only",
        "Ownership assigned (PM, engineering lead, analytics)",
        "ADO feature linked and prioritised",
    ], "Signed-off problem statement + scope boundary")

    _add_checklist_section(doc, "Phase 2 — Business Rules & Data Contract", [
        "All 21 event names and parameter schemas locked (see Requirements table)",
        "ic_component_visible deduplication mechanism confirmed (localStorage vs cookie, TTL)",
        "conversation_id propagation contract confirmed with Clara API team",
        "mode enum values locked for chat_submitted",
        "status enum values locked for chat_response_received",
        "options and options_count ranges confirmed for feedback events",
        "GA4 property / measurement ID confirmed",
        "currentProjectKey value confirmed as gai_copilot_marketing_brand_guidance_ghq",
    ], "Event schema document / data contract signed off")

    _add_checklist_section(doc, "Phase 3 — Discovery Validation (Users)", [
        "Key user journeys validated against the 21 scenarios",
        "Edge cases confirmed: abandoned responses, empty feedback submissions, rename/delete cancellations",
    ], "Validated scenario list with no gaps")

    _add_checklist_section(doc, "Phase 4 — HLR (High-Level Requirements)", [
        "MVP scope confirmed: all 21 events in initial release",
        "Non-goals documented (no GA4 dashboards, no server-side tracking)",
        "Dependencies identified: Clara API (conversation_id, chat_id, task_status), GA4 property access",
        "gtag.js / analytics.js library integration approach agreed",
    ], "This document (HLR) approved")

    _add_checklist_section(doc, "Phase 5 — Design Handoff & Prototype Validation", [
        "Event firing points mapped to UI components (buttons, icons, panel open/close)",
        "No design changes required — tracking is additive/non-visual",
    ], "Component-to-event mapping reviewed by engineering")

    _add_checklist_section(doc, "Phase 6 — Delivery Prep (User Stories & Walkthrough)", [
        "User stories created in ADO for each event group (visibility, open/close, chat submission, response, feedback, conversation management, copy)",
        "Acceptance criteria include: event name, parameters, trigger conditions, deduplication rules",
        "Empty / error state handling included (e.g., FAILURE, ABANDONED statuses)",
        "GA4 debug view validation approach agreed",
    ], "ADO stories with full AC, ready for sprint")

    _add_checklist_section(doc, "Phase 7 — Release & Communication", [
        "Release note drafted covering new GA4 event instrumentation",
        "Known limitations documented (client-side only, single currentProjectKey)",
        "Stakeholders notified (PM, analytics team, data consumers)",
        "GA4 DebugView or Tag Assistant validation completed",
    ], "Release note + stakeholder comms sent")

    _add_checklist_section(doc, "Phase 8 — Post-Release Validation & Learning", [
        "Confirm all 21 events are firing in production GA4 property",
        "Confirm ic_component_visible deduplication is working (no repeat fires per user)",
        "Confirm conversation_id propagation is consistent across multi-turn conversations",
        "Adoption and engagement KPIs baselined",
        "v2 improvements identified from initial data (if any)",
    ], "GA4 event validation report + adoption baseline")


def _build_156061(doc: Document) -> None:
    """ADO 156061 — Share (Chat, Conversation, Conversation via History)."""
    _add_cover_header(
        doc,
        feature_id="156061 — Share (Chat, Conversation, Conversation via History)",
        title="Share (Chat, Conversation, Conversation via History)",
        status="DRAFT",
        owner="POS IC X OneWay",
        version="0.1",
        updated="2026-04-30",
    )

    _add_heading(doc, "Section 1 — Product Brief")
    _add_section1_table(doc, {
        "ADO Feature": "156061 — Share (Chat, Conversation, Conversation via History)",
        "Area Path": "Generative AI Products \\ POS IC X OneWay",
        "Target Date": "TBD",
        "Document Status": "DRAFT",
        "Team Members": "TBD",
        "Design File": "TBD",
        "ADO Backlog": "https://dev.azure.com/ab-inbev-analytics",
    })

    _add_horizontal_rule(doc)

    _add_heading(doc, "Section 2 — Feature Body")

    _add_heading(doc, "Objective", level=2)
    _add_bullet_list(doc, [
        "Allow Clara users to share individual responses and full conversations with colleagues via a shareable link.",
        "Enable recipients to view shared content in read-only mode and optionally fork the conversation as a new unique instance in their own history.",
        "Expose sharing from three entry points: the response action bar, the active conversation view, and the conversation history panel.",
        "Ensure shared content respects recipient RBAC permissions — data visibility is scoped to what the recipient is authorised to see.",
    ])
    doc.add_paragraph()

    _add_heading(doc, "Success Metrics", level=2)
    _add_table(doc,
        headers=["Goal", "Metric"],
        rows=[
            ["Adoption", "Number of share link generation events per week"],
            ["Adoption", "% of active Clara users who use the share feature at least once per month"],
            ["Engagement", "Number of shared links opened by recipients"],
            ["Engagement", "% of recipients who fork a shared conversation into their own history"],
            ["Outcome", "Reduction in duplicate queries (colleagues querying the same question independently)"],
            ["Outcome", "Zero access control violations — recipients never see data beyond their RBAC permissions"],
            ["Business Impact", "Faster team-level decision making using shared Clara insights"],
        ]
    )

    _add_heading(doc, "Assumptions", level=2)
    _add_heading(doc, "Features in scope", level=3)
    _add_bullet_list(doc, [
        "Share a single response via link (from response action bar)",
        "Share an entire conversation via link (from active conversation view header)",
        "Share a conversation from the history panel via '...' context menu",
        "Recipients can view shared content in read-only mode",
        "Recipients with OneWay access can fork any shared conversation as a unique instance in their own conversation history",
        "Recipients cannot edit or delete the sharer's original conversation instance",
        "RBAC permissions apply to data visibility for recipients",
    ])
    _add_heading(doc, "Technical approach", level=3)
    _add_bullet_list(doc, [
        "Shareable links generated server-side; links encode the conversation or response identifier",
        "Recipient access enforced at load time — if RBAC prevents data access, the recipient sees restricted content or an access error",
        "Forking creates a new independent conversation in the recipient's history — does not modify the original",
        "The share link icon (🔗) and 'Share Conversation' option are additive to existing UI components; no existing functionality is removed",
    ])
    _add_heading(doc, "Data scope", level=3)
    _add_table(doc,
        headers=["Dimension", "Value"],
        rows=[
            ["Brands", "All brands accessible via the user's OneWay RBAC permissions"],
            ["Regions", "All regions accessible via the user's OneWay RBAC permissions"],
            ["Channels", "Web (OneWay application)"],
            ["Periods", "From release date onwards"],
            ["Granularity", "Per response / per conversation"],
        ]
    )

    _add_heading(doc, "Milestones", level=2)
    _add_table(doc,
        headers=["Milestone", "Date"],
        rows=[
            ["ADO Feature created", "—"],
            ["Development start", "TBD"],
            ["QA / validation", "TBD"],
            ["Release", "TBD"],
        ]
    )

    _add_heading(doc, "Requirements", level=2)
    _add_heading(doc, "Share entry points", level=3)
    _add_bullet_list(doc, [
        "🔗 icon in response action bar (alongside 👍, 👎, 📋) — generates link to specific response",
        "'Share Conversation' option in active chat header — generates link to full conversation",
        "'Share Conversation' in '...' context menu on each history panel entry",
    ])
    _add_heading(doc, "Recipient experience", level=3)
    _add_bullet_list(doc, [
        "Read-only view — edit and delete actions disabled",
        "Fork to own history — creates independent instance; original conversation unchanged",
        "RBAC enforced at link open — data visibility scoped to recipient's permissions",
        "Recipient must have OneWay access to open any shared link",
    ])
    _add_heading(doc, "Link behaviour", level=3)
    _add_bullet_list(doc, [
        "Links generated server-side, encode conversation or response identifier",
        "No public / unauthenticated links",
        "User can copy link or share via Teams / email",
    ])

    _add_heading(doc, "Out of Scope", level=2)
    _add_bullet_list(doc, [
        "Public / unauthenticated share links",
        "Share link expiry or revocation controls",
        "Notifications to sharer when a link is opened or forked",
        "External sharing outside ABI / OneWay",
        "Collaborative real-time editing of shared conversations",
        "Organisation-wide shared conversation libraries",
    ])

    _add_heading(doc, "Design", level=2)
    _add_table(doc,
        headers=["Artefact", "Link"],
        rows=[
            ["Design file", "TBD"],
            ["Response action bar mockup (with 🔗 icon)", "TBD"],
            ["'Share Conversation' header option mockup", "TBD"],
            ["History panel '...' menu mockup", "TBD"],
            ["Shared conversation read-only view mockup", "TBD"],
        ]
    )

    _add_heading(doc, "User Flows", level=3)

    _add_heading(doc, "Flow 1 — Share a single response via response action bar", level=3)
    _add_bullet_list(doc, [
        "User receives a Clara response in an active conversation.",
        "User hovers over the response — action bar appears showing 👍, 👎, 📋, and 🔗 icons.",
        "User clicks 🔗 → system generates a shareable link scoped to that specific response.",
        "User copies the link or shares it directly via Teams / email.",
        "Recipient with OneWay access opens the link → response loads in read-only view.",
        "Recipient can optionally continue the conversation as a new unique instance in their own history.",
    ])

    _add_heading(doc, "Flow 2 — Share entire conversation from active chat header", level=3)
    _add_bullet_list(doc, [
        "User is in an active conversation with one or more messages.",
        "User clicks 'Share Conversation' at the top of the active chat window.",
        "System generates a shareable link for the full conversation session.",
        "User copies the link or sends it via email / chat.",
        "Recipient with OneWay access opens the link → full conversation loads in read-only view.",
        "Recipient can optionally fork the conversation as a new unique instance in their own history.",
    ])

    _add_heading(doc, "Flow 3 — Share a conversation from history panel", level=3)
    _add_bullet_list(doc, [
        "User opens the conversation history panel.",
        "User locates a past conversation and clicks the '...' context menu next to it.",
        "User selects 'Share Conversation' from the '...' menu.",
        "System generates a shareable link for that conversation session.",
        "User copies the link or sends it via email / chat.",
        "Recipient with OneWay access opens the link → conversation loads in read-only view.",
        "Recipient can optionally fork the conversation as a new unique instance in their own history.",
    ])

    _add_heading(doc, "Flow 4 — Recipient opens a shared link", level=3)
    _add_bullet_list(doc, [
        "Recipient receives a shared Clara link.",
        "Recipient clicks the link.",
        "System checks recipient's OneWay access and RBAC permissions.",
        "If RBAC permits: shared content loads in read-only view — edit and delete actions are disabled.",
        "If RBAC restricts data visibility: restricted data is hidden or an access error is shown for that content.",
        "Recipient reads the shared response or conversation.",
        "Recipient clicks 'Continue conversation' (or equivalent) → conversation is forked as a new independent instance in their own history.",
        "Recipient's fork does not affect the original sharer's conversation instance.",
    ])

    _add_table(doc,
        headers=["Flow", "Entry point", "Scope", "Recipient can fork?", "RBAC enforced?"],
        rows=[
            ["Flow 1", "Response action bar 🔗", "Single response", "Yes", "Yes"],
            ["Flow 2", "Active chat header", "Full conversation", "Yes", "Yes"],
            ["Flow 3", "History panel '...' menu", "Full conversation", "Yes", "Yes"],
            ["Flow 4 (recipient)", "Shared link", "Single response or full conversation", "Yes", "Yes"],
        ]
    )

    _add_heading(doc, "Open Questions", level=2)
    _add_table(doc,
        headers=["Question", "Answer", "Date Answered"],
        rows=[
            ["Partial view or full access error when recipient lacks RBAC access?", "—", "—"],
            ["Is fork automatic on link open, or does recipient click 'Continue conversation'?", "—", "—"],
            ["Do links expire? If yes, what TTL?", "—", "—"],
            ["Can the sharer revoke a link?", "—", "—"],
            ["Is a single response link a deep link or standalone page?", "—", "—"],
            ["GA4 tracking for share link generation and opens? (See Feature 156057)", "—", "—"],
            ["Exact label for share option in conversation header?", "—", "—"],
        ]
    )

    _add_heading(doc, "Change & Request Log", level=2)
    _add_table(doc,
        headers=["Request / Update", "Requestor / Personnel", "Date"],
        rows=[["Initial draft created from ADO 156061", "—", "2026-04-30"]]
    )

    _add_heading(doc, "Reference Links", level=2)
    _add_bullet_list(doc, [
        "ADO Feature 156061: https://dev.azure.com/ab-inbev-analytics",
        "Related: ADO 156057 (Product Analytics — share events may need GA4 tracking)",
        "Related: ADO 156063 (Domain Differentiation — Brand context applies to shared conversations)",
    ])

    _add_horizontal_rule(doc)

    _add_heading(doc, "Section 3 — Discovery → Delivery Checklist")

    _add_checklist_section(doc, "Phase 1 — Discovery Framing & Alignment", [
        "Problem statement defined: users cannot share Clara insights with colleagues without re-querying",
        "Business intent confirmed: enable team collaboration on data-driven decisions via shareable links",
        "Scope agreed: 4 scenarios (single response share, full conversation share, history panel share, access control)",
        "Ownership assigned (PM, UX, engineering, backend/API)",
        "ADO feature linked and prioritised",
    ], "Signed-off problem statement + scope boundary")

    _add_checklist_section(doc, "Phase 2 — Business Rules & Data Contract", [
        "Share link structure defined (response vs. conversation — same or different endpoint/format)",
        "RBAC enforcement mechanism confirmed: how recipient data scoping is applied at link open time",
        "Fork behaviour confirmed: what exactly is copied to recipient history (full conversation, from a specific message?)",
        "Read-only mode behaviour defined: what actions are disabled for recipients",
        "Link permanence / expiry policy confirmed",
        "Revocation capability confirmed (in or out of scope)",
        "GA4 tracking for share events — confirm with Feature 156057 team",
    ], "Share link technical spec + RBAC contract")

    _add_checklist_section(doc, "Phase 3 — Discovery Validation (Users)", [
        "Users confirm the 3 share entry points cover their sharing workflows",
        "Read-only + fork model validated as sufficient for recipient use cases",
        "RBAC restriction behaviour validated — recipients accept that restricted data will not be visible",
    ], "User validation notes")

    _add_checklist_section(doc, "Phase 4 — HLR (High-Level Requirements)", [
        "MVP scope confirmed: 4 scenarios, all 3 entry points, RBAC enforcement, fork to history",
        "Non-goals documented: no public links, no link expiry, no revocation, no external sharing",
        "Dependencies identified: share link generation API, RBAC enforcement at read time, conversation history service, link routing",
        "Fork mechanism dependency on conversation history service confirmed",
    ], "This document (HLR) approved")

    _add_checklist_section(doc, "Phase 5 — Design Handoff & Prototype Validation", [
        "Response action bar with 🔗 icon reviewed",
        "'Share Conversation' header option reviewed",
        "History panel '...' menu with share option reviewed",
        "Shared conversation read-only view reviewed (which actions are hidden/disabled)",
        "RBAC restriction state reviewed (partial data view vs. access denied message)",
    ], "Design sign-off from PO / UX lead")

    _add_checklist_section(doc, "Phase 6 — Delivery Prep (User Stories & Walkthrough)", [
        "User stories created in ADO for: single response share, full conversation share, history panel share, access control / RBAC enforcement, fork to history",
        "Acceptance criteria include: link generation, read-only mode restrictions, fork behaviour, RBAC data scoping",
        "Error states documented: invalid/expired link, insufficient RBAC access, conversation no longer available",
        "Empty states documented: conversation with no messages, single response with no conversation context",
    ], "ADO stories with full AC, ready for sprint")

    _add_checklist_section(doc, "Phase 7 — Release & Communication", [
        "Release note drafted covering sharing feature (3 entry points, read-only + fork model)",
        "Known limitations documented (OneWay access required, no link expiry/revocation, no external sharing)",
        "Stakeholders notified (PM, OneWay users, teams lead)",
        "Enablement material created if needed (short guide or tooltip copy for share UX)",
    ], "Release note + stakeholder comms sent")

    _add_checklist_section(doc, "Phase 8 — Post-Release Validation & Learning", [
        "Confirm share link generation works from all 3 entry points in production",
        "Confirm read-only mode correctly disables edit/delete for recipients",
        "Confirm fork to history creates independent conversation instances",
        "Confirm RBAC data scoping is enforced correctly for recipients with different permission levels",
        "Monitor share link generation and open rates (KPIs from Success Metrics)",
        "v2 improvements identified (e.g., link expiry, revocation, notification to sharer)",
    ], "Post-release validation checklist signed off")


def _build_156063(doc: Document) -> None:
    """ADO 156063 — Domain Differentiation (Clara dynamic domain adoption)."""
    _add_cover_header(
        doc,
        feature_id="156063 — Domain Differentiation",
        title="Domain Differentiation (Clara Dynamic Domain Adoption)",
        status="DRAFT",
        owner="POS IC X OneWay",
        version="0.2",
        updated="2026-05-07",
    )

    _add_heading(doc, "Section 1 — Product Brief")
    _add_section1_table(doc, {
        "ADO Feature": "156063 — Domain Differentiation",
        "Area Path": "Generative AI Products \\ POS IC X OneWay",
        "Target Date": "TBD",
        "Document Status": "DRAFT",
        "Team Members": "TBD",
        "Design File": "TBD",
        "ADO Backlog": "https://dev.azure.com/ab-inbev-analytics",
    })

    _add_horizontal_rule(doc)

    _add_heading(doc, "Section 2 — Feature Body")

    _add_heading(doc, "Objective", level=2)
    _add_bullet_list(doc, [
        "Clara must dynamically adopt the domain identity of the OneWay page it is loaded on — the IC component label, suggested prompts, and response scope all change to match the active page context.",
        "On a Brand page, Clara presents as 'Clara Brand Guidance' and is scoped to Brand-related queries.",
        "On a Category page, Clara presents as 'Clara Category Guidance' and is scoped to Category-related queries.",
        "On any other page where domain cannot be determined, Clara defaults to Brand Guidance mode.",
        "Users understand Clara's scope on first interaction from the label and suggested prompts alone — no additional onboarding required.",
        "Out-of-scope queries are declined gracefully with a domain-aware message; no misleading or irrelevant answers are generated.",
        "Deep links enforce the correct domain context: a shared conversation link redirects the user to the appropriate domain page before loading the conversation.",
    ])
    doc.add_paragraph()

    _add_heading(doc, "Success Metrics", level=2)
    _add_table(doc,
        headers=["Goal", "Metric"],
        rows=[
            ["Adoption", "% of users who open Clara from each domain entry point (Brand, Category)"],
            ["Adoption", "Distribution of Clara sessions by domain context (Brand vs. Category vs. default)"],
            ["Engagement", "Reduction in out-of-scope queries over time per domain (measured via graceful error response rate)"],
            ["Engagement", "% of Clara sessions where the first query matches the active domain"],
            ["Outcome", "User satisfaction with response relevance per domain (qualitative / feedback signals)"],
            ["Outcome", "Zero misleading or irrelevant responses to non-domain queries (verified via QA per domain)"],
            ["Business Impact", "Users self-serve domain-specific insights without needing to re-query or clarify scope"],
        ]
    )

    _add_heading(doc, "Assumptions", level=2)
    _add_heading(doc, "Features in scope", level=3)
    _add_bullet_list(doc, [
        "Dynamic IC component label — updates to reflect the active page domain (e.g., 'Clara Brand Guidance', 'Clara Category Guidance')",
        "Dynamic suggested prompts — landing page prompts are domain-specific and update to match the active page context",
        "Domain-aware out-of-scope handling — graceful error message references the active domain (e.g., 'I'm sorry, I can only answer questions related to Brand Power Analytics.')",
        "Default fallback — pages with no identifiable domain context load Clara in Brand Guidance mode",
        "Deep link redirect — shared conversation links detect the required domain context and redirect to the correct page before loading the conversation",
        "Initial domains supported: Brand (Brand Power Playbook page), Category (Category page)",
    ])
    _add_heading(doc, "Technical approach", level=3)
    _add_bullet_list(doc, [
        "IC component reads a domain identifier from the host page (e.g., a page-level attribute, route parameter, or config value) to determine active domain",
        "Domain identifier maps to: panel label copy, suggested prompts set, out-of-scope response message, and system prompt / prompt engineering config",
        "If no domain identifier is present or it is unrecognised, the component falls back to Brand domain defaults",
        "Deep link routing logic reads the domain from the shared conversation metadata and redirects to the appropriate page before opening the conversation",
    ])
    _add_heading(doc, "Data scope", level=3)
    _add_table(doc,
        headers=["Dimension", "Value"],
        rows=[
            ["Domains (v1)", "Brand (Brand Power Playbook), Category"],
            ["Default domain", "Brand — applied when page context is unknown or unrecognised"],
            ["Regions", "All regions where OneWay is deployed"],
            ["Channels", "Web (OneWay application)"],
            ["Periods", "From release date onwards"],
            ["Granularity", "Per session / per query"],
        ]
    )

    _add_heading(doc, "Milestones", level=2)
    _add_table(doc,
        headers=["Milestone", "Date"],
        rows=[
            ["ADO Feature created", "—"],
            ["Development start", "TBD"],
            ["QA / validation (Brand + Category + default)", "TBD"],
            ["Release", "TBD"],
        ]
    )

    _add_heading(doc, "Requirements", level=2)
    _add_heading(doc, "Domain adoption", level=3)
    _add_bullet_list(doc, [
        "Brand page (identifier: 'brand') → label: 'Clara Brand Guidance', Brand-focused prompts",
        "Category page (identifier: 'category') → label: 'Clara Category Guidance', Category-focused prompts",
        "No / unrecognised identifier → default to Brand Guidance; no error surfaced to user",
    ])
    _add_heading(doc, "Out-of-scope handling", level=3)
    _add_bullet_list(doc, [
        "Graceful refusal for non-domain queries — no misleading answers generated",
        "Error template: 'I'm sorry, I can only answer questions related to {Domain} Analytics.'",
    ])
    _add_heading(doc, "Deep link", level=3)
    _add_bullet_list(doc, [
        "Domain read from shared conversation metadata",
        "Redirect to correct domain page if user is not already there",
        "Conversation loads in correct domain context post-redirect",
    ])

    _add_heading(doc, "Out of Scope", level=2)
    _add_bullet_list(doc, [
        "Additional domains beyond Brand and Category in v1",
        "Borderline query reclassification (Clara answers or declines — no partial answers)",
        "Analytics tracking of out-of-scope volume per domain (Feature 156057)",
        "User-selectable domain switching within a session",
        "Self-service domain configuration",
        "Cross-domain query routing",
    ])

    _add_heading(doc, "Design", level=2)
    _add_table(doc,
        headers=["Artefact", "Link"],
        rows=[
            ["Design file", "TBD"],
            ["IC panel label mockup — Brand", "TBD"],
            ["IC panel label mockup — Category", "TBD"],
            ["Suggested prompts copy — Brand", "TBD"],
            ["Suggested prompts copy — Category", "TBD"],
            ["Domain identifier contract / spec", "TBD"],
        ]
    )

    _add_heading(doc, "User Flows", level=3)

    _add_heading(doc, "Flow 1 — User is on a Brand page", level=3)
    _add_bullet_list(doc, [
        "User navigates to a Brand page (e.g., Brand Power Playbook).",
        "Page exposes domain identifier: 'brand'.",
        "IC component reads identifier and configures itself for Brand domain.",
        "User opens the Clara panel — header displays: 'Clara Brand Guidance'.",
        "Suggested prompts shown are Brand-focused (brand performance, positioning, campaign insights).",
        "User submits a Brand query → Clara responds within Brand scope.",
        "User submits an out-of-scope query → Clara responds: 'I'm sorry, I can only answer questions related to Brand Power Analytics.'",
    ])

    _add_heading(doc, "Flow 2 — User is on a Category page", level=3)
    _add_bullet_list(doc, [
        "User navigates to a Category page.",
        "Page exposes domain identifier: 'category'.",
        "IC component reads identifier and configures itself for Category domain.",
        "User opens the Clara panel — header displays: 'Clara Category Guidance'.",
        "Suggested prompts shown are Category-focused.",
        "User submits a Category query → Clara responds within Category scope.",
        "User submits an out-of-scope query → Clara responds with the Category-specific graceful error.",
    ])

    _add_heading(doc, "Flow 3 — User is on any other page (default fallback)", level=3)
    _add_bullet_list(doc, [
        "User navigates to a page with no domain identifier (or an unrecognised value).",
        "IC component detects missing/unknown domain and applies Brand domain defaults.",
        "User opens the Clara panel — header displays: 'Clara Brand Guidance'.",
        "Suggested prompts shown are Brand-focused.",
        "Behaviour is identical to Flow 1 — Brand mode is the fallback for all unrecognised page contexts.",
    ])

    _add_heading(doc, "Flow 4 — User opens a shared conversation deep link", level=3)
    _add_bullet_list(doc, [
        "User receives a shared Clara conversation link (from Feature 156061).",
        "User clicks the link.",
        "System reads the domain from the shared conversation metadata.",
        "If user is not on the correct domain page → system redirects to the appropriate page.",
        "After redirect, Clara opens with the shared conversation loaded in the correct domain context.",
        "User can read the shared conversation and optionally fork it into their own history.",
    ])

    _add_table(doc,
        headers=["Page Context", "Domain Identifier", "Clara Panel Label", "Suggested Prompts", "Out-of-scope message"],
        rows=[
            ["Brand page", "'brand'", "Clara Brand Guidance", "Brand-focused", "...related to Brand Power Analytics."],
            ["Category page", "'category'", "Clara Category Guidance", "Category-focused", "...related to Category Analytics."],
            ["Other / unknown page", "None / unrecognised", "Clara Brand Guidance (default)", "Brand-focused", "...related to Brand Power Analytics."],
        ]
    )

    _add_heading(doc, "Open Questions", level=2)
    _add_table(doc,
        headers=["Question", "Answer", "Date Answered"],
        rows=[
            ["How is the domain identifier exposed — page attribute, route, or config object?", "—", "—"],
            ["Exact suggested prompts per domain (Brand and Category)?", "—", "—"],
            ["Fixed error template or custom string per domain?", "—", "—"],
            ["Who owns the domain identifier contract — FE or platform?", "—", "—"],
            ["Domain metadata: stored at share time or derived at link open?", "—", "—"],
            ["What if the deep link domain page is unavailable to the recipient?", "—", "—"],
            ["Any domains beyond Brand and Category planned for v1 or near-v2?", "—", "—"],
            ["Is the Brand default configurable per deployment?", "—", "—"],
        ]
    )

    _add_heading(doc, "Change & Request Log", level=2)
    _add_table(doc,
        headers=["Request / Update", "Requestor / Personnel", "Date"],
        rows=[
            ["Initial draft created from ADO 156063", "—", "2026-04-30"],
            ["Rewritten: feature scope expanded from Brand-only to dynamic domain adoption (Brand, Category, default fallback); all sections updated", "—", "2026-05-07"],
        ]
    )

    _add_heading(doc, "Reference Links", level=2)
    _add_bullet_list(doc, [
        "ADO Feature 156063: https://dev.azure.com/ab-inbev-analytics",
        "Related: ADO 156057 (Product Analytics — tracks IC component interactions per domain)",
        "Related: ADO 156061 (Share — shared conversation deep links must carry domain context)",
    ])

    _add_horizontal_rule(doc)

    _add_heading(doc, "Section 3 — Discovery → Delivery Checklist")

    _add_checklist_section(doc, "Phase 1 — Discovery Framing & Alignment", [
        "Problem statement defined: Clara has a fixed Brand identity that does not adapt to page context; users on non-Brand pages receive a mismatched experience",
        "Business intent confirmed: Clara should feel native to whichever page it is on — domain identity, prompts, and scope all match the active context",
        "Scope agreed: dynamic domain adoption for Brand + Category + default fallback; 5 scenarios including deep link redirect",
        "Ownership assigned (PM, UX, FE engineering, prompt engineering, platform/routing)",
        "ADO feature linked and prioritised",
    ], "Signed-off problem statement + scope boundary")

    _add_checklist_section(doc, "Phase 2 — Business Rules & Data Contract", [
        "Domain identifier contract defined: name, expected values ('brand', 'category'), location in page, fallback behaviour",
        "Label copy confirmed per domain: 'Clara Brand Guidance', 'Clara Category Guidance'",
        "Suggested prompt lists confirmed per domain (Brand and Category)",
        "Out-of-scope error message template confirmed: 'I'm sorry, I can only answer questions related to {Domain} Analytics.'",
        "Out-of-scope detection mechanism agreed per domain (prompt engineering / system prompt config)",
        "Default domain confirmed as Brand for unrecognised / missing identifiers",
        "Deep link domain metadata contract confirmed: what is stored at share time, how it is read at open time",
        "Edge case: deep link domain page unavailable — behaviour defined",
    ], "Domain identifier contract doc + per-domain UI copy + out-of-scope spec")

    _add_checklist_section(doc, "Phase 3 — Discovery Validation (Users)", [
        "Users on Brand pages confirm 'Clara Brand Guidance' label communicates scope clearly",
        "Users on Category pages confirm 'Clara Category Guidance' label communicates scope clearly",
        "Out-of-scope query examples tested per domain — graceful errors confirmed as satisfactory",
        "Deep link redirect flow tested end-to-end for both Brand and Category domains",
        "Default fallback (Brand) confirmed as acceptable for unrecognised pages",
    ], "User validation notes per domain")

    _add_checklist_section(doc, "Phase 4 — HLR (High-Level Requirements)", [
        "MVP scope confirmed: 5 scenarios (Brand adoption, Category adoption, default fallback, out-of-scope handler, deep link redirect)",
        "Non-goals documented: no additional domains in v1, no user-selectable domain switching, no borderline query reclassification",
        "Dependencies identified: domain identifier contract (host page ↔ IC component), per-domain prompt engineering config, deep link routing with domain metadata",
        "Dependency on Feature 156061 (Share) confirmed for deep link domain metadata",
    ], "This document (HLR) approved")

    _add_checklist_section(doc, "Phase 5 — Design Handoff & Prototype Validation", [
        "IC panel header label reviewed for Brand and Category domains",
        "Suggested prompts layout reviewed per domain",
        "Out-of-scope response UI treatment confirmed (consistent across domains)",
        "Default fallback state reviewed (no visual indication of fallback to user)",
        "Deep link redirect UX reviewed (loading state, timing, domain context confirmation)",
    ], "Design sign-off from PO / UX lead for all domain states")

    _add_checklist_section(doc, "Phase 6 — Delivery Prep (User Stories & Walkthrough)", [
        "User stories created in ADO for: Brand domain adoption, Category domain adoption, default fallback, out-of-scope handler (per domain), deep link redirect (per domain)",
        "Acceptance criteria include: domain identifier values, exact label strings, prompt content, error message template, redirect trigger conditions",
        "Error states documented: unrecognised domain (→ fallback), deep link domain page unavailable, conversation ID invalid in deep link",
        "QA test cases created for all 5 scenarios across both domains + default fallback",
    ], "ADO stories with full AC, ready for sprint")

    _add_checklist_section(doc, "Phase 7 — Release & Communication", [
        "Release note drafted covering dynamic domain adoption (Brand, Category, default), user-facing label changes, and deep link behaviour",
        "Known limitations documented: v1 supports Brand and Category only; default fallback is always Brand",
        "Stakeholders notified (PM, Brand analytics users, Category analytics users, comms team)",
    ], "Release note + stakeholder comms sent")

    _add_checklist_section(doc, "Phase 8 — Post-Release Validation & Learning", [
        "Confirm 'Clara Brand Guidance' label and Brand prompts load correctly on Brand pages in production",
        "Confirm 'Clara Category Guidance' label and Category prompts load correctly on Category pages in production",
        "Confirm default fallback (Brand) activates correctly on pages with no domain identifier",
        "Confirm out-of-scope queries return the correct domain-specific graceful error in production",
        "Confirm deep link redirect works correctly for both Brand and Category domain links",
        "Monitor out-of-scope query rate per domain and feedback signals",
        "v2 improvements identified (e.g., additional domains, configurable domain defaults, smarter out-of-scope detection)",
    ], "Post-release validation checklist signed off per domain")


def _build_156056(doc: Document) -> None:
    """ADO 156056 — Feedback Nudge."""
    _add_cover_header(
        doc,
        feature_id="156056 — Feedback Nudge",
        title="Feedback Nudge",
        status="DRAFT",
        owner="POS IC X OneWay",
        version="0.1",
        updated="2026-05-11",
    )

    # Section 1
    _add_heading(doc, "Section 1 — Product Brief")
    _add_section1_table(doc, {
        "ADO Feature": "156056 — Feedback Nudge",
        "Area Path": "Generative AI Products \\ POS IC X OneWay",
        "Target Date": "",
        "Document Status": "DRAFT",
        "Team Members": "Sangani Kartik, Abhinav Gupta",
        "Design File": "",
        "ADO Backlog": "https://dev.azure.com/ab-inbev-analytics/Generative%20AI%20Products/_boards/board/t/POS%20IC%20X%20Oneway",
    })

    _add_horizontal_rule(doc)

    # Section 2
    _add_heading(doc, "Section 2 — Feature Body")

    _add_heading(doc, "Objective", level=2)
    _add_bullet_list(doc, [
        "Add a proactive, non-blocking feedback nudge to Clara after every response is rendered — including error responses.",
        "Allow users to submit thumbs-up / thumbs-down ratings inline, without leaving their current workflow.",
        "Increase the volume and consistency of user feedback captured per Clara session.",
        "Create a reliable feedback signal to inform response quality improvements over time.",
        "Ensure the nudge is unobtrusive — it must not interrupt, delay, or compete with the primary response UI.",
    ])
    doc.add_paragraph()

    _add_heading(doc, "Success Metrics", level=2)
    _add_table(doc,
        headers=["Goal", "Metric", "Category"],
        rows=[
            ["Users engage with the nudge", "% of Clara responses that receive a thumbs-up or thumbs-down", "Adoption"],
            ["Nudge visibility is high", "% of responses where nudge is rendered vs. dismissed without interaction", "Engagement"],
            ["Dismiss rate is low", "Ratio of dismiss clicks vs. rating clicks", "Engagement"],
            ["Feedback volume increases", "Total feedback events per day vs. pre-nudge baseline", "Outcome"],
            ["Response quality improves", "Thumbs-up ratio trend over rolling 30 days", "Business Impact"],
        ]
    )

    _add_heading(doc, "Assumptions", level=2)
    _add_heading(doc, "Features in scope", level=3)
    _add_bullet_list(doc, [
        "Nudge renders after every Clara response, including error / fallback responses",
        "Nudge displays inline thumbs-up and thumbs-down icons (reusing existing feedback icons)",
        "Nudge includes a dismiss (X) button",
        "Nudge copy: \"Was this response helpful? Let us know!\"",
        "Nudge disappears immediately on any user interaction (thumbs-up, thumbs-down, or dismiss)",
        "Once dismissed or rated, the nudge does not reappear for that response instance",
    ])
    _add_heading(doc, "Technical approach", level=3)
    _add_bullet_list(doc, [
        "Nudge is a frontend UI component that slides in near the response actions area",
        "Triggered client-side once the response streaming / rendering is complete",
        "Reuses existing thumbs-up / thumbs-down feedback event handlers",
        "State is managed per response instance (not persisted across sessions for suppression)",
        "No backend changes required for nudge visibility logic",
    ])
    _add_heading(doc, "Data scope", level=3)
    _add_table(doc,
        headers=["Dimension", "Value"],
        rows=[
            ["Product", "POS Clara"],
            ["Surface", "Clara chat interface (OneWay)"],
            ["Trigger", "All response types (success + error)"],
            ["Granularity", "Per response instance"],
            ["Regions", "All regions using Clara"],
        ]
    )

    _add_heading(doc, "Milestones", level=2)
    _add_table(doc,
        headers=["Milestone", "Date"],
        rows=[
            ["HLR sign-off", ""],
            ["Design handoff", ""],
            ["Dev complete", ""],
            ["UAT / QA", ""],
            ["Go-live", ""],
        ]
    )

    _add_heading(doc, "Requirements", level=2)
    _add_heading(doc, "Nudge display", level=3)
    _add_bullet_list(doc, [
        "Response fully rendered → nudge slides in near the response actions area",
        "Nudge text: \"Was this response helpful? Let us know!\"",
        "Thumbs-up and thumbs-down icons rendered inline within the nudge",
        "Nudge appears for all response types including errors and fallback messages",
        "Nudge does not block, overlap, or delay the primary response content",
    ])
    _add_heading(doc, "Nudge dismissal and state", level=3)
    _add_bullet_list(doc, [
        "Thumbs-up click → nudge disappears immediately; feedback event fired",
        "Thumbs-down click → nudge disappears immediately; feedback event fired",
        "Dismiss (X) click → nudge disappears immediately; no feedback event fired",
        "Once interacted with → nudge does not reappear for the same response instance",
        "No suppression logic required across sessions or users (v1)",
    ])

    _add_heading(doc, "Out of Scope", level=2)
    _add_bullet_list(doc, [
        "Free-text / comment-based feedback input",
        "Feedback analytics dashboard or reporting UI",
        "Per-user nudge frequency capping or cooldown logic",
        "Feedback-triggered model retraining or automated response adjustment",
        "Push / email follow-up after a thumbs-down rating",
        "Session-level or user-level nudge suppression",
    ])

    _add_heading(doc, "Design", level=2)
    _add_table(doc,
        headers=["Artefact", "Link"],
        rows=[
            ["Figma / design file", ""],
            ["Component reference (existing feedback icons)", ""],
        ]
    )

    _add_heading(doc, "User Flows", level=3)

    _add_heading(doc, "Flow 1 — User asks a question and sees the nudge", level=3)
    _add_bullet_list(doc, [
        "User submits a question to Clara.",
        "Clara generates and renders the full response (KPI table, narrative, etc.).",
        "Once rendering is complete → nudge slides in near the response actions area.",
        "Nudge displays: \"Was this response helpful? Let us know!\" with thumbs-up, thumbs-down, and X icons.",
    ])

    _add_heading(doc, "Flow 2 — User clicks thumbs-up", level=3)
    _add_bullet_list(doc, [
        "Nudge is visible after a Clara response.",
        "User clicks thumbs-up icon → positive feedback event fires.",
        "Nudge disappears immediately.",
        "No further nudge shown for that response.",
    ])

    _add_heading(doc, "Flow 3 — User clicks thumbs-down", level=3)
    _add_bullet_list(doc, [
        "Nudge is visible after a Clara response.",
        "User clicks thumbs-down icon → negative feedback event fires.",
        "Nudge disappears immediately.",
        "No further nudge shown for that response.",
    ])

    _add_heading(doc, "Flow 4 — User dismisses the nudge", level=3)
    _add_bullet_list(doc, [
        "Nudge is visible after a Clara response.",
        "User clicks X (dismiss) → nudge disappears immediately.",
        "No feedback event fired.",
        "No further nudge shown for that response.",
    ])

    _add_heading(doc, "Flow 5 — Error response with nudge", level=3)
    _add_bullet_list(doc, [
        "Clara returns an error or fallback message.",
        "Nudge renders the same as for a successful response.",
        "All dismissal and rating behaviours apply identically.",
    ])

    _add_table(doc,
        headers=["Flow", "Entry point", "Key events", "Notes"],
        rows=[
            ["1 — See nudge", "Response render complete", "Nudge slide-in", "All response types"],
            ["2 — Thumbs-up", "Nudge visible", "Feedback event (positive)", "Nudge disappears"],
            ["3 — Thumbs-down", "Nudge visible", "Feedback event (negative)", "Nudge disappears"],
            ["4 — Dismiss", "Nudge visible", "No event fired", "Nudge disappears"],
            ["5 — Error response", "Error render complete", "Same nudge behaviour", "No special handling"],
        ]
    )

    _add_heading(doc, "Open Questions", level=2)
    _add_table(doc,
        headers=["Question", "Answer", "Date Answered"],
        rows=[
            ["Should thumbs-down trigger a follow-up prompt or secondary flow in a future iteration?", "", ""],
            ["Is there a defined delay between response render complete and nudge appearance, or is it immediate?", "", ""],
            ["Should the nudge appear on streaming responses mid-render, or only after the full response is done?", "", ""],
            ["Do we need to log dismiss events (X clicks) to the feedback data store, or only thumbs interactions?", "", ""],
            ["What is the target go-live date / sprint?", "", ""],
        ]
    )

    _add_heading(doc, "Change & Request Log", level=2)
    _add_table(doc,
        headers=["Request / Update", "Requestor / Personnel", "Date"],
        rows=[["Initial HLR draft created from ADO Feature #156056", "Abhinav Gupta", "2026-05-11"]]
    )

    _add_heading(doc, "Reference Links", level=2)
    _add_bullet_list(doc, [
        "ADO Feature 156056: https://dev.azure.com/ab-inbev-analytics/Generative%20AI%20Products/_workitems/edit/156056",
        "POS IC X Oneway Board: https://dev.azure.com/ab-inbev-analytics/Generative%20AI%20Products/_boards/board/t/POS%20IC%20X%20Oneway",
    ])

    _add_horizontal_rule(doc)

    # Section 3
    _add_heading(doc, "Section 3 — Discovery \u2192 Delivery Checklist")

    _add_checklist_section(doc, "Phase 1 — Discovery Framing & Alignment", [
        "Problem validated: users are not providing feedback consistently due to friction",
        "Business intent confirmed: increase labelled feedback volume to improve Clara response quality",
        "Feature owner identified (Sangani Kartik)",
        "Scope boundary agreed: nudge only, no free-text, no downstream retraining in v1",
        "ADO Feature #156056 created and linked to parent Epic",
    ], "Confirmed problem statement + feature owner assignment")

    _add_checklist_section(doc, "Phase 2 — Business Rules & Data Contract", [
        "Nudge trigger condition defined: render complete (not mid-stream)",
        "Feedback event schema confirmed: what fields are logged on thumbs-up / thumbs-down",
        "Dismiss event logging decision made (log or not log)",
        "Per-response uniqueness rule confirmed: nudge state is per-response-instance, not persisted",
        "Error response inclusion confirmed: nudge appears on all response types",
    ], "Feedback event schema + trigger rule doc")

    _add_checklist_section(doc, "Phase 3 — Discovery Validation (Users)", [
        "User interviews or survey run on current feedback friction points",
        "Nudge copy validated: \"Was this response helpful? Let us know!\" confirmed as clear",
        "Placement validated: response actions area confirmed as visible and non-intrusive",
        "Dismiss pattern validated: X button understood as optional, not required",
    ], "Validation summary (interviews or usability test notes)")

    _add_checklist_section(doc, "Phase 4 — HLR (High-Level Requirements)", [
        "This document reviewed and signed off by PM and engineering lead",
        "Open questions resolved (delay, dismiss logging, thumbs-down follow-up)",
        "Out-of-scope items agreed and communicated to stakeholders",
        "Milestone dates filled in",
        "Dependencies on existing feedback icon components confirmed",
    ], "Signed-off HLR document (this file)")

    _add_checklist_section(doc, "Phase 5 — Design Handoff & Prototype Validation", [
        "Nudge component designed in Figma (placement, copy, icons, animation)",
        "Responsive / mobile behaviour defined",
        "Animation spec: slide-in direction, speed, and easing confirmed",
        "Design reviewed against existing Clara UI patterns for consistency",
        "Prototype tested with at least 2 internal users",
    ], "Approved Figma file + design handoff notes")

    _add_checklist_section(doc, "Phase 6 — Delivery Prep (User Stories & Walkthrough)", [
        "User stories written for: nudge render, thumbs-up, thumbs-down, dismiss, error response",
        "Acceptance criteria written and reviewed for each story",
        "Frontend component identified or scaffolded (reuse vs. new)",
        "Feedback event logging confirmed with backend / data team",
        "Story walkthrough completed with engineering team",
        "Stories estimated and added to sprint",
    ], "Ready user stories in ADO with acceptance criteria and estimates")

    _add_checklist_section(doc, "Phase 7 — Release & Communication", [
        "Release notes drafted covering nudge behaviour and known limitations",
        "Internal comms sent to Clara users (Teams / email)",
        "Known limitations documented: no session-level suppression, no free-text in v1",
        "Support team briefed on expected user questions",
    ], "Release notes + comms sent")

    _add_checklist_section(doc, "Phase 8 — Post-Release Validation & Learning", [
        "Nudge render rate monitored (nudges shown vs. responses rendered)",
        "Feedback interaction rate tracked (thumbs vs. dismiss vs. no action)",
        "Thumbs-up / thumbs-down ratio baselined",
        "Regression check: no impact on response render time or UX",
        "Retro held: what to change in v2 (free-text? frequency capping? thumbs-down follow-up?)",
    ], "Post-release metrics report + v2 recommendation")


def _build_156058(doc: Document) -> None:
    """ADO 156058 — Landing Page Personalization & Slider (Smartflows + FAQs)."""
    _add_cover_header(
        doc,
        feature_id="156058 — Landing Page Personalization & Slider",
        title="Landing Page Personalization & Slider to have more than 2 Smartflows and FAQs",
        status="DRAFT",
        owner="POS IC X OneWay",
        version="0.1",
        updated="2026-05-11",
    )

    # Section 1
    _add_heading(doc, "Section 1 — Product Brief")
    _add_section1_table(doc, {
        "ADO Feature": "156058 — Landing Page Personalization & Slider",
        "Area Path": "Generative AI Products \\ POS IC X OneWay",
        "Target Date": "",
        "Document Status": "DRAFT",
        "Team Members": "Sangani Kartik, Abhinav Gupta",
        "Design File": "",
        "ADO Backlog": "https://dev.azure.com/ab-inbev-analytics/Generative%20AI%20Products/_boards/board/t/POS%20IC%20X%20Oneway",
    })

    _add_horizontal_rule(doc)

    # Section 2
    _add_heading(doc, "Section 2 — Feature Body")

    _add_heading(doc, "Objective", level=2)
    _add_bullet_list(doc, [
        "Replace the fixed 2-item display of Smart Flows and FAQs on the Clara landing page with a scrollable carousel or paginated list exposing all available items.",
        "Allow Clara users to discover the full catalogue of Smart Flows and FAQs before they type a query, reducing friction and increasing feature discoverability.",
        "Provide intuitive left/right navigation with a position indicator so users always know where they are in the carousel.",
        "Ensure the carousel is responsive within the constrained right-sidebar layout of the OneWay application.",
        "Add a subtle, non-intrusive nudge that hints at carousel interactivity for first-time or idle users without disrupting the primary content experience.",
    ])
    doc.add_paragraph()

    _add_heading(doc, "Success Metrics", level=2)
    _add_table(doc,
        headers=["Goal", "Metric"],
        rows=[
            ["Adoption", "% of Clara landing page sessions where a user interacts with a Smart Flow or FAQ card (clicks or scrolls beyond the first 2)"],
            ["Adoption", "% of users who click a Smart Flow that was previously hidden (position 3+)"],
            ["Engagement", "Average number of carousel navigation arrow clicks per session on landing page"],
            ["Engagement", "Click-through rate on FAQ items surfaced via carousel vs. previous static list"],
            ["Outcome", "Increase in first-query submission rate from landing page (user selects a Smart Flow or FAQ)"],
            ["Outcome", "Reduction in blank query submissions (users who type without browsing available options)"],
            ["Business Impact", "More Clara sessions initiated via Smart Flow — measurable through existing chat_submitted mode tracking (Feature 156057)"],
        ]
    )

    _add_heading(doc, "Assumptions", level=2)
    _add_heading(doc, "Features in scope", level=3)
    _add_bullet_list(doc, [
        "Scrollable carousel or paginated vertical list for all Smart Flows on the Clara landing page",
        "Scrollable carousel or expandable list for all FAQs in the 'Some questions you can ask' section",
        "Left / right navigation arrows with smooth slide transition",
        "Pagination indicator — dots or counter (e.g., '2/5') showing current position in the carousel",
        "Responsive layout: 2 cards visible at a time within the constrained right-sidebar width; no card cut-off or overlap",
        "Subtle idle nudge: dim, non-intrusive pulse or glow on carousel navigation arrows; disappears on any user interaction; not shown too frequently",
    ])
    _add_heading(doc, "Technical approach", level=3)
    _add_bullet_list(doc, [
        "Carousel is a frontend-only UI component — no backend changes required for the carousel mechanics",
        "Smart Flows and FAQs are fetched from the existing API; the carousel renders all returned items dynamically",
        "Navigation state (current position, arrow visibility) is managed in local component state",
        "Responsive layout: component reads panel width and enforces 2-card display when width is constrained",
        "Idle nudge: CSS animation (keyframe glow/pulse) triggered after a configurable inactivity timeout; cleared on first interaction event",
        "Pagination counter or dot indicator derived from total items and current scroll/page position",
    ])
    _add_heading(doc, "Data scope", level=3)
    _add_table(doc,
        headers=["Dimension", "Value"],
        rows=[
            ["Surface", "Clara landing page (IC component, OneWay)"],
            ["Sections", "Smart Flows carousel + FAQs carousel"],
            ["Regions", "All regions where Clara / OneWay is deployed"],
            ["Channels", "Web (OneWay application, right-sidebar view)"],
            ["Periods", "From release date onwards"],
            ["Granularity", "Per session / per user interaction with carousel"],
        ]
    )

    _add_heading(doc, "Milestones", level=2)
    _add_table(doc,
        headers=["Milestone", "Date"],
        rows=[
            ["HLR sign-off", ""],
            ["Design handoff", ""],
            ["Dev complete", ""],
            ["UAT / QA", ""],
            ["Go-live", ""],
        ]
    )

    _add_heading(doc, "Requirements", level=2)

    _add_heading(doc, "Smart Flows carousel", level=3)
    _add_bullet_list(doc, [
        "Landing page loads → all Smart Flows rendered in a scrollable carousel (not capped at 2)",
        "Each card shows: Smart Flow title and example query description",
        "Left / right navigation arrows visible; left arrow hidden when at the first card, right arrow hidden when at the last",
        "Clicking right arrow → next set of cards slides into view smoothly",
        "Clicking left arrow → previous set of cards slides into view",
        "Pagination dots or counter (e.g., '2/5') rendered below or beside the carousel to indicate current position",
    ])

    _add_heading(doc, "FAQs carousel", level=3)
    _add_bullet_list(doc, [
        "'Some questions you can ask' section loads → all FAQs accessible via scrollable carousel or expandable list",
        "Navigation and pagination behaviour mirrors the Smart Flows carousel",
        "All FAQs reachable without truncation",
    ])

    _add_heading(doc, "Responsive layout", level=3)
    _add_bullet_list(doc, [
        "Constrained sidebar width → carousel displays 2 cards at a time",
        "Cards must not be cut off or overlap the panel boundary",
        "Wider view (if applicable) → carousel may show more cards; defined by breakpoint spec in design",
    ])

    _add_heading(doc, "Idle nudge", level=3)
    _add_bullet_list(doc, [
        "User lands on new chat page and has not interacted with the carousel within the inactivity threshold",
        "A dim, non-intrusive glow or pulse animation activates on the carousel navigation arrows",
        "Nudge disappears immediately when the user interacts with the carousel or any other page element",
        "Nudge must not recur too frequently — minimum interval between nudge activations to be defined in design/dev",
        "Nudge must not distract from, overlap, or visually compete with the main response or chat area",
    ])

    _add_heading(doc, "Out of Scope", level=2)
    _add_bullet_list(doc, [
        "Personalised Smart Flow ordering based on user history or role",
        "User-configurable pinning or reordering of carousel cards",
        "Auto-play or auto-advance carousel behaviour",
        "Touch / swipe gesture support (mobile-first; can be added in v2 based on usage)",
        "Adding or editing Smart Flow or FAQ content from the landing page",
        "Carousel on pages other than the Clara landing page",
    ])

    _add_heading(doc, "Design", level=2)
    _add_table(doc,
        headers=["Artefact", "Link"],
        rows=[
            ["Figma / design file", ""],
            ["Smart Flows carousel mockup", ""],
            ["FAQs carousel mockup", ""],
            ["Responsive layout (2-card constrained view)", ""],
            ["Idle nudge animation spec", ""],
            ["Pagination indicator design", ""],
        ]
    )

    _add_heading(doc, "User Flows", level=3)

    _add_heading(doc, "Flow 1 — User opens Clara landing page and browses Smart Flows", level=3)
    _add_bullet_list(doc, [
        "User opens the Clara IC panel on a OneWay page.",
        "Clara landing page loads with all Smart Flows displayed in a carousel.",
        "User sees the first 2 Smart Flow cards and a right arrow indicating more items.",
        "User clicks the right arrow → next set of cards slides in; left arrow appears; pagination counter updates (e.g., '2/5').",
        "User clicks a Smart Flow card → chat_submitted fires with mode=is_smartflow_landing_page.",
    ])

    _add_heading(doc, "Flow 2 — User browses all FAQs", level=3)
    _add_bullet_list(doc, [
        "User sees the 'Some questions you can ask' section on the Clara landing page.",
        "All FAQs are accessible via a scrollable carousel or expandable list.",
        "User navigates through FAQs using left/right arrows or scrolling.",
        "User clicks a FAQ → chat_submitted fires with mode=FAQ.",
    ])

    _add_heading(doc, "Flow 3 — Constrained sidebar responsive view", level=3)
    _add_bullet_list(doc, [
        "User opens the Clara panel in right-sidebar mode (constrained width).",
        "Carousel automatically enforces 2-card display — no overflow, cut-off, or panel boundary violation.",
        "Navigation arrows remain accessible and functional.",
    ])

    _add_heading(doc, "Flow 4 — Idle nudge activates", level=3)
    _add_bullet_list(doc, [
        "User opens the Clara new chat page but has not interacted with the carousel.",
        "After the inactivity threshold elapses → a dim glow or pulse animation appears on the carousel navigation arrows.",
        "Nudge draws attention to the carousel without interrupting the user.",
        "User clicks an arrow or any other element → nudge disappears immediately.",
        "Nudge does not reappear for a defined minimum interval.",
    ])

    _add_heading(doc, "Flow 5 — User reaches the last card in the carousel", level=3)
    _add_bullet_list(doc, [
        "User has navigated to the last set of Smart Flow cards.",
        "Right arrow is hidden (or disabled) — user cannot scroll beyond the last item.",
        "Pagination counter shows the final position (e.g., '5/5').",
        "User can navigate back via the left arrow.",
    ])

    _add_table(doc,
        headers=["Flow", "Entry point", "Key events", "Notes"],
        rows=[
            ["1 — Browse Smart Flows", "Clara landing page", "Right/left arrow clicks; chat_submitted", "All Smart Flows accessible"],
            ["2 — Browse FAQs", "FAQ section", "Right/left arrow clicks; chat_submitted", "All FAQs accessible"],
            ["3 — Constrained layout", "Sidebar view", "2-card display enforced", "No cut-off or overflow"],
            ["4 — Idle nudge", "Landing page (inactive)", "Glow/pulse animation on arrows", "Clears on any interaction"],
            ["5 — Last card reached", "Smart Flows carousel end", "Right arrow hidden / disabled", "Left arrow still active"],
        ]
    )

    _add_heading(doc, "Open Questions", level=2)
    _add_table(doc,
        headers=["Question", "Answer", "Date Answered"],
        rows=[
            ["Carousel or vertical paginated list? ADO allows either — which is preferred for Smart Flows?", "", ""],
            ["How many Smart Flows are currently returned by the API? (determines carousel sizing)", "", ""],
            ["How many FAQs are currently returned? (determines FAQ section sizing)", "", ""],
            ["What is the inactivity threshold before the idle nudge activates?", "", ""],
            ["What is the minimum interval between nudge activations for the same session?", "", ""],
            ["Is touch/swipe required in v1 (if Clara is used on tablet/mobile surfaces)?", "", ""],
            ["Exact breakpoint for '2 cards at a time' — panel width value?", "", ""],
            ["Should GA4 tracking be added for carousel arrow clicks? (Coordinate with Feature 156057)", "", ""],
        ]
    )

    _add_heading(doc, "Change & Request Log", level=2)
    _add_table(doc,
        headers=["Request / Update", "Requestor / Personnel", "Date"],
        rows=[["Initial HLR draft created from ADO Feature #156058", "Abhinav Gupta", "2026-05-11"]]
    )

    _add_heading(doc, "Reference Links", level=2)
    _add_bullet_list(doc, [
        "ADO Feature 156058: https://dev.azure.com/ab-inbev-analytics/Generative%20AI%20Products/_workitems/edit/156058",
        "Parent Epic 156052: https://dev.azure.com/ab-inbev-analytics/Generative%20AI%20Products/_workitems/edit/156052",
        "Related: ADO 156057 (Product Analytics — carousel interactions may need GA4 events)",
        "POS IC X Oneway Board: https://dev.azure.com/ab-inbev-analytics/Generative%20AI%20Products/_boards/board/t/POS%20IC%20X%20Oneway",
    ])

    _add_horizontal_rule(doc)

    # Section 3
    _add_heading(doc, "Section 3 — Discovery \u2192 Delivery Checklist")

    _add_checklist_section(doc, "Phase 1 — Discovery Framing & Alignment", [
        "Problem validated: Clara landing page shows only 2 Smart Flows and 2 FAQs, limiting discoverability of the full catalogue",
        "Business intent confirmed: expose all Smart Flows and FAQs to drive higher feature adoption and more intentional first queries",
        "Scope agreed: scrollable carousel for Smart Flows + FAQs, responsive 2-card layout, idle nudge",
        "Feature owner identified (Sangani Kartik)",
        "ADO Feature #156058 created and linked to parent Epic #156052",
    ], "Confirmed problem statement + scope boundary")

    _add_checklist_section(doc, "Phase 2 — Business Rules & Data Contract", [
        "Total number of Smart Flows and FAQs returned by API confirmed (informs carousel sizing)",
        "Cards-per-view rule confirmed per breakpoint (default: 2 in sidebar view)",
        "Idle nudge: inactivity threshold value agreed (e.g., 5 seconds)",
        "Idle nudge: minimum re-activation interval agreed",
        "Pagination indicator format agreed: dots vs. counter (e.g., '2/5')",
        "Arrow visibility rules confirmed: left hidden at first card, right hidden at last card",
        "GA4 event tracking for carousel interactions confirmed with Feature 156057 team (in or out of v1)",
    ], "Carousel behaviour spec + API item count confirmation")

    _add_checklist_section(doc, "Phase 3 — Discovery Validation (Users)", [
        "Users confirm carousel model (scroll or paginate) covers their browsing workflow on the landing page",
        "Idle nudge tested with 2–3 internal users — confirmed as non-intrusive and helpful",
        "Responsive 2-card layout validated in constrained sidebar view — no card cut-off observed",
        "FAQ carousel / expandable list validated — all items accessible without confusion",
    ], "User validation notes + nudge feedback")

    _add_checklist_section(doc, "Phase 4 — HLR (High-Level Requirements)", [
        "MVP scope confirmed: Smart Flows carousel, FAQ carousel, responsive layout, idle nudge, pagination indicator",
        "Non-goals documented: no personalised ordering, no touch/swipe in v1, no auto-advance",
        "Dependencies identified: Smart Flows API (all items), FAQs API (all items), existing chat_submitted event handlers (Feature 156057)",
        "Open questions on nudge timing and carousel type resolved",
        "This document reviewed and signed off by PM and engineering lead",
    ], "Signed-off HLR document (this file)")

    _add_checklist_section(doc, "Phase 5 — Design Handoff & Prototype Validation", [
        "Smart Flows carousel Figma mockup reviewed — card layout, arrow placement, pagination indicator",
        "FAQ section carousel / expandable list mockup reviewed",
        "Responsive 2-card constrained-view layout reviewed — no overflow or cut-off",
        "Idle nudge animation spec reviewed — glow/pulse style, timing, and disappear trigger confirmed",
        "Prototype tested with internal users for intuitiveness of carousel navigation",
    ], "Approved Figma file + design handoff notes")

    _add_checklist_section(doc, "Phase 6 — Delivery Prep (User Stories & Walkthrough)", [
        "User stories written for: Smart Flows carousel (pagination + navigation), FAQ carousel/list, responsive layout, idle nudge, pagination indicator, arrow edge-case (first/last card)",
        "Acceptance criteria include: all items accessible, arrow visibility rules, nudge timing, card count per view, no cut-off",
        "Error states documented: API returns 0 Smart Flows / 0 FAQs — carousel hidden or fallback state shown",
        "Story walkthrough completed with engineering team",
        "Stories estimated and added to sprint",
    ], "Ready user stories in ADO with acceptance criteria and estimates")

    _add_checklist_section(doc, "Phase 7 — Release & Communication", [
        "Release notes drafted covering expanded Smart Flows and FAQ carousel on landing page",
        "Known limitations documented: no personalised ordering, swipe/touch not in v1",
        "Internal comms sent to Clara users (Teams / email) highlighting new discoverability",
        "Support team briefed on expected user questions about carousel navigation",
    ], "Release notes + comms sent")

    _add_checklist_section(doc, "Phase 8 — Post-Release Validation & Learning", [
        "Confirm all Smart Flows and FAQs are accessible via carousel in production",
        "Confirm carousel navigation arrows show/hide correctly at first and last card",
        "Confirm idle nudge activates and clears as specified",
        "Confirm 2-card layout in constrained sidebar — no cut-off or overflow in production",
        "Track carousel click-through rate and Smart Flow adoption uplift (compare to pre-carousel baseline)",
        "v2 improvements identified (e.g., touch/swipe, personalised ordering, auto-advance toggle)",
    ], "Post-release metrics report + v2 recommendation")


def _build_156281(doc: Document) -> None:
    """ADO 156281 — Creative Mode Toggle (Internet Search vs Internal Analysis)."""
    _add_cover_header(
        doc,
        feature_id="156281 — Creative Mode Toggle",
        title="Creative Mode Toggle (Internet Search Augmented vs Internal Analysis)",
        status="DRAFT",
        owner="POS IC X OneWay",
        version="0.1",
        updated="2026-05-11",
    )

    # Section 1
    _add_heading(doc, "Section 1 — Product Brief")
    _add_section1_table(doc, {
        "ADO Feature": "156281 — Creative Mode Toggle",
        "Area Path": "Generative AI Products \\ POS IC X OneWay",
        "Target Date": "TBD",
        "Document Status": "DRAFT",
        "Team Members": "TBD",
        "Design File": "TBD",
        "ADO Backlog": "https://dev.azure.com/ab-inbev-analytics/ABI/_workitems/edit/156281",
    })

    _add_horizontal_rule(doc)

    # Section 2
    _add_heading(doc, "Section 2 — Feature Body")

    _add_heading(doc, "Objective", level=2)
    _add_bullet_list(doc, [
        "Introduce a non-intrusive toggle in the IC component allowing users to freely switch between Internet Search Augmented mode (web-grounded responses) and Internal Analysis mode (internal data / RAG only).",
        "Give users persistent, profile-level control over their preferred grounding source — defaulting to Internal Analysis on first use.",
        "Surface a one-time contextual nudge on first toggle encounter to explain the two modes without interrupting the conversation flow.",
        "Toggle state is sent to IC APIs on each question submission; all routing logic is owned by the backend — the toggle is a signal, not an executor.",
    ])
    doc.add_paragraph()

    _add_heading(doc, "Success Metrics", level=2)
    _add_table(doc,
        headers=["Goal", "Metric"],
        rows=[
            ["Adoption", "% of active IC users who interact with the toggle at least once"],
            ["Adoption", "% of first-time users who engage with the onboarding nudge"],
            ["Engagement", "Distribution of mode selections — Internal Analysis vs Internet Search — per session"],
            ["Engagement", "Average number of mode switches per conversation"],
            ["Outcome", "Reduction in 'inaccurate response' feedback on internal-data questions post-release"],
            ["Outcome", "% of internet-mode queries returning grounded web results (IC API success rate)"],
            ["Business Impact", "Increased user trust in AI responses through transparent, user-controlled grounding source"],
        ]
    )

    _add_heading(doc, "Assumptions", level=2)
    _add_heading(doc, "Features in scope", level=3)
    _add_bullet_list(doc, [
        "Per-question mode toggle rendered non-intrusively in the IC component input area",
        "Two modes: Internal Analysis (default) and Internet Search Augmented",
        "Toggle state persisted at user profile level — same setting across sessions unless the user changes it",
        "First-time nudge — one-time inline tooltip/popover explaining both modes, gated per user profile",
        "Toggle state passed as a parameter on each question submission to IC APIs",
        "GA4 analytics events for toggle interactions and nudge display/dismissal",
    ])
    _add_heading(doc, "Technical approach", level=3)
    _add_bullet_list(doc, [
        "Toggle renders adjacent to the question input bar within the IC component",
        "User's preferred mode stored in their profile (backend) — fetched on IC component initialisation",
        "Mode selection sent as a boolean/enum parameter on each IC API call; IC APIs own the routing",
        "First-time nudge gated via user profile flag (server-side) — no localStorage dependency",
        "No changes to IC API routing logic on the client side — toggle is additive, non-breaking",
        "Default mode on first profile creation: Internal Analysis",
    ])
    _add_heading(doc, "Data scope", level=3)
    _add_table(doc,
        headers=["Dimension", "Value"],
        rows=[
            ["Brands", "All brands using the IC component in OneWay"],
            ["Regions", "All regions where OneWay is deployed"],
            ["Channels", "Web (OneWay application)"],
            ["Periods", "From release date onwards"],
            ["Granularity", "Per question submitted; preference persisted at user-profile level"],
        ]
    )

    _add_heading(doc, "Milestones", level=2)
    _add_table(doc,
        headers=["Milestone", "Date"],
        rows=[
            ["ADO Feature created", "2026-05-11"],
            ["HLR sign-off", "TBD"],
            ["Development start", "TBD"],
            ["QA / validation", "TBD"],
            ["Release", "TBD"],
        ]
    )

    _add_heading(doc, "Requirements", level=2)

    _add_heading(doc, "Toggle component", level=3)
    _add_bullet_list(doc, [
        "Toggle renders in the IC question input area — visible on every question input interaction",
        "Two states: Internal Analysis (default) and Internet Search Augmented",
        "Active mode label visible next to or within the toggle — no icon-only ambiguity",
        "Toggle click → mode switches immediately; no confirmation dialog required",
        "Switched mode persisted to user profile on change — applied to all subsequent sessions",
    ])

    _add_heading(doc, "First-time nudge", level=3)
    _add_bullet_list(doc, [
        "Nudge fires once per user on first encounter with the toggle — gated via user profile flag",
        "Inline tooltip/popover explaining: Internal Analysis uses internal brand data only; Internet Search adds live web results",
        "Dismissed by clicking elsewhere, clicking X, or interacting with the toggle",
        "Dismissal recorded in user profile — nudge never shown again for that user",
        "Nudge does not block question submission",
    ])

    _add_heading(doc, "IC API integration", level=3)
    _add_bullet_list(doc, [
        "Mode selection sent as a parameter on every question submission to IC APIs",
        "IC APIs own the routing: internet search or internal analysis based on parameter value",
        "No client-side search or retrieval logic — toggle is a signal only",
        "API parameter contract (name and value enum) to be locked before build",
    ])

    _add_heading(doc, "Profile persistence", level=3)
    _add_bullet_list(doc, [
        "Toggle state stored in user profile — fetched on IC component initialisation each session",
        "Profile update triggered on toggle switch — asynchronous, non-blocking",
        "If profile fetch fails on load → fall back to Internal Analysis mode; retry silently",
        "New users with no profile setting default to Internal Analysis",
    ])

    _add_heading(doc, "Analytics events", level=3)
    _add_table(doc,
        headers=["Event Name", "Trigger", "Key Parameters"],
        rows=[
            ["toggle_mode_switched", "User clicks the mode toggle", "currentProjectKey, from_mode, to_mode, question_index"],
            ["nudge_shown", "First-time nudge displays to a user", "currentProjectKey"],
            ["nudge_dismissed", "User dismisses the first-time nudge", "currentProjectKey, dismiss_method (click_outside | click_x | toggle_interact)"],
        ]
    )

    _add_heading(doc, "Out of Scope", level=2)
    _add_bullet_list(doc, [
        "Admin or tenant-level controls to disable internet search mode",
        "Third-party search engine selection or configuration",
        "Toggle on SmartFlow inputs — free-text questions only",
        "Internet search result citation or source attribution UI",
        "Session-only (non-persisted) toggle mode variant",
        "Mobile app IC component — web only",
    ])

    _add_heading(doc, "Design", level=2)
    _add_table(doc,
        headers=["Artefact", "Link"],
        rows=[
            ["Design file", "TBD"],
            ["Toggle component mockup", "TBD"],
            ["First-time nudge mockup", "TBD"],
        ]
    )

    _add_heading(doc, "User Flows", level=3)

    _add_heading(doc, "Flow 1 — New user: first-time nudge and toggle discovery", level=3)
    _add_bullet_list(doc, [
        "User opens IC component for the first time (or first time since feature release).",
        "IC component initialises → fetches user profile → mode = Internal Analysis (default), nudge_shown flag = false.",
        "User types a question → toggle visible in input area in Internal Analysis state.",
        "Nudge appears inline → explains the two modes in plain language.",
        "User reads nudge → dismisses (clicks elsewhere, X, or toggle) → nudge_dismissed fires; profile flag updated.",
        "User submits question → IC API receives mode=internal_analysis.",
    ])

    _add_heading(doc, "Flow 2 — User switches to Internet Search Augmented mode", level=3)
    _add_bullet_list(doc, [
        "User is in an active IC conversation (Internal Analysis mode active).",
        "User clicks toggle → mode switches to Internet Search Augmented → toggle_mode_switched fires (from=internal, to=internet).",
        "Profile updated asynchronously with new preference.",
        "User submits question → IC API receives mode=internet_search.",
        "Response generated using web-grounded sources.",
        "User closes IC and returns in a later session → mode initialises as Internet Search Augmented (from profile).",
    ])

    _add_heading(doc, "Flow 3 — User submits without switching (default flow)", level=3)
    _add_bullet_list(doc, [
        "Returning user opens IC — mode initialises to their saved profile preference (Internal Analysis or Internet Search Augmented).",
        "No nudge shown (profile flag already set).",
        "User types and submits question without touching the toggle.",
        "IC API receives the saved preference mode — no toggle event fires.",
    ])

    _add_heading(doc, "Flow 4 — Profile fetch failure fallback", level=3)
    _add_bullet_list(doc, [
        "User opens IC → profile fetch fails (network error or timeout).",
        "IC component falls back to Internal Analysis mode silently.",
        "User can still interact with toggle — any switch updates profile when connectivity recovers.",
        "No error state shown to the user for this edge case.",
    ])

    _add_table(doc,
        headers=["Flow", "Entry point", "Key events", "Notes"],
        rows=[
            ["New user nudge", "First question input", "nudge_shown, nudge_dismissed", "Once per user — profile flag gate"],
            ["Mode switch", "Toggle click", "toggle_mode_switched", "Profile updated async on each switch"],
            ["Submit with saved mode", "Question submission", "(existing chat_submitted) + mode param", "Mode from profile, no toggle event"],
            ["Profile fetch failure", "IC component init", "None", "Fallback to Internal Analysis silently"],
        ]
    )

    _add_heading(doc, "Open Questions", level=2)
    _add_table(doc,
        headers=["Question", "Answer", "Date Answered"],
        rows=[
            ["What is the IC API parameter name and value enum for mode selection (e.g. mode=internal | internet)?", "", ""],
            ["Which profile service / endpoint stores and retrieves the toggle preference?", "", ""],
            ["What is the nudge copy — who owns the final wording (PM / UX)?", "", ""],
            ["Is the toggle visible on SmartFlow inputs, or strictly free-text questions?", "Out of scope — free-text only", "2026-05-11"],
            ["What is the fallback TTL / retry strategy if the profile update call fails?", "", ""],
        ]
    )

    _add_heading(doc, "Change & Request Log", level=2)
    _add_table(doc,
        headers=["Request / Update", "Requestor / Personnel", "Date"],
        rows=[["Initial draft created from ADO 156281", "—", "2026-05-11"]]
    )

    _add_heading(doc, "Reference Links", level=2)
    _add_bullet_list(doc, [
        "ADO Feature 156281: https://dev.azure.com/ab-inbev-analytics/ABI/_workitems/edit/156281",
    ])

    _add_horizontal_rule(doc)

    # Section 3
    _add_heading(doc, "Section 3 — Discovery → Delivery Checklist")

    _add_checklist_section(doc, "Phase 1 — Discovery Framing & Alignment", [
        "Problem statement defined: users lack persistent, explicit control over AI grounding source in IC",
        "Business intent confirmed: increase response trust and relevance through user-controlled mode",
        "Scope agreed: per-question toggle with profile-level persistence, IC component only, IC APIs own routing",
        "Default mode confirmed: Internal Analysis",
        "Ownership assigned (PM, design, IC API team, frontend, profile service team)",
        "ADO feature 156281 linked and prioritised",
    ], "Signed-off problem statement + scope boundary")

    _add_checklist_section(doc, "Phase 2 — Business Rules & Data Contract", [
        "IC API mode parameter name, type, and value enum locked",
        "Profile service endpoint and schema confirmed for storing toggle preference",
        "Profile fetch failure fallback behaviour agreed (Internal Analysis default)",
        "First-time nudge gate mechanism confirmed (profile flag — field name and initial value)",
        "Analytics event schema locked: toggle_mode_switched, nudge_shown, nudge_dismissed",
        "Toggle availability on SmartFlow inputs confirmed as out of scope",
    ], "IC API contract + profile schema + analytics event schema doc")

    _add_checklist_section(doc, "Phase 3 — Discovery Validation (Users)", [
        "Users understand the distinction between both modes without reading docs",
        "Nudge copy validated: users can explain both modes after reading nudge text",
        "Toggle placement validated: users discover it without guidance",
        "Profile persistence expectation validated: users expect setting to carry across sessions",
        "Edge case confirmed: user reaction when internet mode fails or returns no results",
    ], "Validated user research findings or usability test summary")

    _add_checklist_section(doc, "Phase 4 — HLR (High-Level Requirements)", [
        "MVP scope confirmed: toggle + nudge + IC API mode parameter + profile persistence",
        "Non-goals documented (no admin controls, no SmartFlow toggle, no source attribution UI)",
        "Dependencies identified: IC API team (mode parameter), profile service, design, analytics",
        "This HLR document approved by PM and tech lead",
    ], "This document (HLR) approved")

    _add_checklist_section(doc, "Phase 5 — Design Handoff & Prototype Validation", [
        "Toggle design: two-state, label visible, placement in IC input area confirmed",
        "Nudge design reviewed: copy, dismissal behaviour, placement, non-blocking",
        "Design validated against IC component constraints — no layout disruption on existing flows",
        "Toggle visual state on init (profile fetch in-progress) handled in design",
        "Responsive / sidebar layout reviewed",
    ], "Design files linked; prototype signed off by PM and engineering")

    _add_checklist_section(doc, "Phase 6 — Delivery Prep (User Stories & Walkthrough)", [
        "User stories created: toggle component, first-time nudge, IC API integration, profile persistence, analytics events",
        "AC covers: default state, mode label, profile fetch on init, async profile update on switch, fallback on fetch failure",
        "AC covers: nudge trigger, gate via profile flag, dismissal methods, profile flag update on dismiss",
        "AC covers: analytics events with correct parameters for all toggle and nudge interactions",
        "Edge cases included: profile fetch failure, network timeout on profile update",
        "Engineering walkthrough completed — no open questions remaining before sprint start",
    ], "ADO stories with full AC, ready for sprint")

    _add_checklist_section(doc, "Phase 7 — Release & Communication", [
        "Release note drafted: new profile-persisted mode toggle in IC component",
        "Known limitations documented (internet mode subject to search availability, web only)",
        "IC API team and profile service team notified of go-live date",
        "Stakeholders informed via release comms (PM, analytics, OneWay users)",
    ], "Release note + stakeholder comms sent")

    _add_checklist_section(doc, "Phase 8 — Post-Release Validation & Learning", [
        "Confirm toggle renders correctly across all IC entry points in production",
        "Confirm nudge fires once per user and profile flag is correctly set on dismissal",
        "Confirm IC API receives correct mode parameter on all question submissions",
        "Confirm profile preference persists and initialises correctly across sessions",
        "Adoption and engagement KPIs baselined: toggle usage %, mode distribution, nudge dismissal rate",
        "v2 improvements identified (e.g., per-conversation override, admin defaults, mobile support)",
    ], "Post-release validation report + adoption baseline")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

DOCS: list[tuple[str, str, callable]] = [
    ("156056", "156056-feedback-nudge-owr.docx", _build_156056),
    ("156057", "156057-product-analytics-owr.docx", _build_156057),
    ("156058", "156058-landing-page-slider-owr.docx", _build_156058),
    ("156061", "156061-share-conversation-owr.docx", _build_156061),
    ("156063", "156063-domain-differentiation-owr.docx", _build_156063),
    ("156281", "156281-creative-mode-toggle-owr.docx", _build_156281),
]

_VALID_FEATURES = [feature_id for feature_id, _, _ in DOCS]


def _build_doc(out_dir: Path, filename: str, builder: callable) -> None:
    out_path = out_dir / filename
    console.print(f"Building [bold]{filename}[/bold]...")
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
    builder(doc)
    doc.save(str(out_path))
    console.print(f"  [green]✓ Saved → {out_path}[/green]")


@app.command()
def main(
    out_dir: Path = typer.Option(DOCS_DIR, help="Output directory for generated .docx files"),
    feature: list[str] = typer.Option(
        None,
        "--feature",
        "-f",
        help=f"ADO feature number(s) to build. Repeatable. Valid: {', '.join(_VALID_FEATURES)}. Omit to build all.",
    ),
) -> None:
    """Generate OWR + HLR Word documents for one or more ADO features."""
    out_dir.mkdir(parents=True, exist_ok=True)

    if feature:
        unknown = [f for f in feature if f not in _VALID_FEATURES]
        if unknown:
            console.print(f"[red]Unknown feature(s): {', '.join(unknown)}[/red]")
            console.print(f"Valid options: {', '.join(_VALID_FEATURES)}")
            raise typer.Exit(code=1)
        selected = [(fid, fname, builder) for fid, fname, builder in DOCS if fid in feature]
    else:
        selected = DOCS

    for _, filename, builder in selected:
        _build_doc(out_dir, filename, builder)

    console.print(f"\n[bold green]Done.[/bold green] {len(selected)} document(s) written to {out_dir}/")


if __name__ == "__main__":
    app()
