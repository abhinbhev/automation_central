---
name: email-draft
description: Draft a professional email — stakeholder update, sprint comms, incident notification, or general
domain: comms
requires_script: false
---

## Usage

Invoke with `/email-draft` then describe:
- **Purpose:** what the email is for (sprint update / incident / stakeholder ask / announcement / other)
- **Audience:** who is receiving it (team / manager / exec / external stakeholder)
- **Key points:** what needs to be communicated
- **Tone:** formal / semi-formal / casual (default: semi-formal)
- **Action required:** what you want the recipient to do, if anything

## Output

A ready-to-send email with:
- Subject line
- Greeting
- Body (concise paragraphs, bullets where appropriate)
- Clear call-to-action or next step
- Sign-off

## Email Types

| Type | Characteristic |
|---|---|
| Sprint update | Highlights velocity, completed items, blockers, next sprint goals |
| Incident notification | What happened, impact, current status, next steps, ETA |
| Stakeholder ask | Context, specific ask, deadline, what "yes" looks like |
| Team announcement | What's changing, why, when, what team members need to do |

## Steps

1. Identify email type and audience from the provided description
2. Calibrate tone: exec audience → concise + formal; team → conversational
3. Draft subject line (specific, not vague — "Sprint 14 Complete: 3 blockers for your review" not "Sprint Update")
4. Draft body: context → key points → ask or next steps
5. If key information is missing (dates, names, specific metrics), mark as `[INSERT]`
