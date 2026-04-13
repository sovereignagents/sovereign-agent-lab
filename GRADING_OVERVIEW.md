# Week 1 — Grading Overview
**AI Performance Engineering · Module 1 · Nebius Academy**

Read this before starting. Understanding how you will be evaluated
changes how you approach the work.

---

## Total: 100 points

The assignment is graded in three layers. Each layer tests something different,
and no single layer can be gamed without doing the actual work.

---

## Layer 1 — Mechanical (30 points)

Checked automatically by `grade.py`. Binary pass/fail per check.

Run `python grade.py` yourself before submitting. The instructor runs
the same script on your submission. If your local run says pass and the
instructor's run says fail, that is an integrity concern.

**What is checked:**
- Output JSON files exist and are valid (proves you ran the code)
- `sovereign_agent/` modules import without errors
- `generate_event_flyer` in Exercise 2 returns a valid success dict
  (either live-provider mode or the deterministic placeholder fallback —
  both pass; see `CHANGELOG.md` §Changed for why this changed)
- The cutoff guard in `exercise3_rasa/actions/actions.py` is uncommented
- All answer files have been filled in (no placeholder text remaining)

No partial credit on mechanical checks. Either it works or it doesn't.

---

## Layer 2 — Behavioural (40 points)

The instructor will run your code against specific inputs that are not
published in advance. You know which scenarios will be tested — not the
exact values.

**Scenarios that will be tested:**

| Scenario | What we check |
|---|---|
| Venue tool called with a full pub | Does it correctly report `meets_all_constraints: false`? |
| Research agent, first choice is unavailable | Does it find an alternative without being told to? |
| Research agent, impossible constraint (very high guest count) | Does it admit failure rather than hallucinate a venue? |
| Rasa, valid booking details | Does it confirm without escalating? |
| Rasa, deposit above your `MAX_DEPOSIT_GBP` | Does it escalate with a clear reason? |
| MCP server called with capacity filter | Does it return only venues that satisfy all constraints? |

**Why we don't publish exact inputs:**

If we told you "we'll test with £500 deposit", you could hardcode
`if deposit == 500: escalate()` and pass the test without understanding anything.
Instead, we test with *a deposit above your MAX_DEPOSIT_GBP* — so the only way
to pass is to have correctly implemented the general logic.

Partial credit is available on behavioural tests when code partially works.

---

## Layer 3 — Reasoning (30 points)

Three questions, 10 points each. The questions are in your answer files.
You know which questions will be graded. You do not know the rubric criteria.

**The three questions:**

| Question | Location | Topic |
|---|---|---|
| Q1 | `answers/ex1_answers.py` → `CORE_LESSON` | When does context formatting matter? |
| Q2 | `answers/ex2_answers.py` → `MOST_SURPRISING` | Most unexpected agent behaviour |
| Q3 | `answers/ex4_answers.py` → `GUIDING_QUESTION_ANSWER` | Which agent for which problem |

**Why we don't publish the rubric:**

If we published exact criteria, the answer becomes a template-filling exercise.
The rubric rewards things that require you to have actually run the code and thought
about what happened. Generic descriptions of how technology works will not score well.

What we can tell you: a strong answer references something specific that happened
in your run. A weak answer could have been written by someone who never opened
a terminal.

**Minimum word counts are enforced by `grade.py`.** Meeting minimum word count
is necessary but not sufficient for a good score.

---

## Progression

This assignment is the foundation of **PyNanoClaw**, the hybrid agent
system you will build across the module. The code you write in
`sovereign_agent/` and `exercise3_rasa/` will be extended in the final
consolidated assignment (released 2026-04-18), which merges both halves
into one system: planner/executor split upstream of the research loop,
memory, a handoff bridge between the two halves, observability, and an
optional voice pipeline. See `CHANGELOG.md` §Added for the course
structure change and `PROGRESS.md` for the full architecture diagram.

If you submit a poorly implemented `research_agent.py` or a broken
`exercise3_rasa/` this week, you start the final assignment with broken
foundations. There is no "redo from scratch" — both halves get composed
into PyNanoClaw, and both need to work.

This is important: **everyone builds both halves**. There are no tracks
to pick between. The earlier version of this module split students into
an "OpenClaw Automator" track and a "Rasa Digital Employee" track; that
split has been removed. The core lesson of the module is that real agent
systems combine open-ended reasoning with structured, auditable logic —
you only learn that by building both and seeing where each belongs.

---

## Late Submission

- Up to 24 hours late: −5 points
- 24–72 hours late: −15 points
- 72 hours – 5 days late: −25 points, feedback only (no grade revision)
- After 5 days: submission accepted for feedback only, not graded

---

## Academic Integrity

You may use AI assistants to help write code. You may not use them to write
your reasoning answers.

The reasoning questions ask about your specific results — what your model
returned, which condition failed, what turn the agent pivoted. An AI cannot
know this without having run your code. Answers that don't reference your
specific outputs will score in the lower bands.

The instructor cross-checks your reasoning answers against your
`outputs/*.json` files. Claiming a result that your JSON contradicts
is flagged for review.