---
name: Week 1 Assignment Context
description: Lecturer's framing of the Week 1 Edinburgh Agent assignment — the narrative, submission rules, and support process
type: project
---

This is a course assignment from a lecturer at Nebius Academy.

**The scenario:** Rod sends a WhatsApp ("sort the pub for tonight, 160 people, vegan options, confirm by 5pm") and disappears for three hours.

**Two agents to build:**
1. **Headless Automator** — searches venues, checks weather, estimates catering costs, generates flyer. Autonomous, no human in loop.
2. **Digital Employee** — takes the call from the pub manager, confirms the booking, enforces limits. Structured, auditable, no improvising.

**Why:** They grow together across all five weeks into a combined system. Week 5 applies the whole thing to something from the student's own work.

**Submission:**
- Submit entire fork (not just files) — lecturer pulls from it directly
- Run `make check-submit` before pushing — it lists exactly what's missing
- Grading is 30/40/30 (mechanical / behavioral / reasoning) per GRADING_OVERVIEW.md

**Support process:** When stuck, run command directly (not via make) for full error, then open a GitHub issue in the repo with: exercise number, command run, OS, and `uv --version`.

**Repo:** https://github.com/sovereignagents/sovereign-agent-lab (student forks this — do not clone directly)

**Why/How to apply:** Understand that this is coursework with real grading and a submission deadline. When helping with code, prioritize correctness of the graded artifacts (`week1/outputs/*.json`, `week1/answers/*.py`, tool implementations, Rasa actions). The fork workflow means the student's repo is a fork of the upstream.
