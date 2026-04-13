# Changelog

All notable changes to the Week 1 Sovereign Agent Lab are documented here.

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
conventions. Entries are grouped by type (Fixed / Changed / Added / Notes)
and tagged with the originating GitHub issue or PR where applicable.

---

## [1.2.1] — 2026-04-13

Dummy-proofing patch release on top of [1.2.0]. No code semantics change;
this release makes the Makefile more forgiving of common setup mistakes
and addresses one piece of cohort feedback around Exercise 3 grading.

### Added

- **`make doctor` target.** A new diagnostic command for when students
  are stuck and can't tell what's wrong. It walks through every common
  setup failure mode (uv installation, upstream git remote, `.env`
  contents, BOM marker, venv existence, module imports) and prints a
  pass/fail per check with an actionable fix hint for each failure.
  Instructors should reach for this as the first response to "nothing
  works" in Discord: *"Run `make doctor` and paste the output."*
  *File:* `Makefile` (new `doctor` target).

### Fixed

- **Makefile `check-env` false positives.** The earlier `check-env`
  target grep-matched the placeholder string `sk-your-key-here`
  anywhere in `.env`, so a student who put their real key on the
  `NEBIUS_KEY=` line but left the string in a comment or in another
  variable would still fail the check. `check-env` now parses the
  uncommented `NEBIUS_KEY=` line specifically, extracts the value in
  isolation, and validates it. It also detects and reports the four
  other common `.env` mistakes with specific fix hints: a UTF-8 BOM
  marker (Windows Notepad), quotes around the value, spaces around the
  `=` sign, and an empty value. Each failure mode produces a distinct
  error message naming the exact fix.
  *File:* `Makefile` (`check-env` target rewritten).

- **Makefile `ex2-b` stale TODO messaging.** The earlier `make ex2-b`
  printed `"Implement the TODO in venue_tools.py first"` and pointed at
  a `# ── TODO` block that no longer exists after the [1.1.0] flyer-tool
  rewrite. The target now describes the graceful-fallback pattern and
  tells students to look for the `mode` field in the output and record
  it in `ex2_answers.py → TASK_B_MODE`.
  *File:* `Makefile` (`ex2-b` target).

- **`grade.py` — `CALM_VS_OLD_RASA` is now a WARN, not a FAIL** (raised
  in anonymous cohort feedback). This field asked students to compare
  Rasa Pro CALM with pre-CALM open-source Rasa 3.x — a comparison that
  requires prior knowledge of old Rasa, which was never taught in the
  course. Blocking a submission on a 30-word answer to this question
  was punishing students for material they were never assigned. The
  grader now treats the field as optional: PASS at ≥30 words, WARN at
  anything shorter or blank. The prompt in `ex3_answers.py` is
  unchanged, so students who filled it in lose nothing, and students
  who left it blank are no longer blocked. This mirrors the [1.1.0]
  handling of `WEEK_5_ARCHITECTURE`.
  *File:* `week1/grade.py` (`check_ex3` function).

### Notes

Students who are pulling Rod's tests at grading time will see the 
`CALM_VS_OLD_RASA` downgrade reflected automatically. 
There is no student-side change needed. The grader still
reports the field's status in the output, just as a warning rather than
a failure.

---

## [1.2.0] — 2026-04-13

Narrative consolidation release. Removes the "Track A (OpenClaw Automator)
vs Track B (Rasa Digital Employee)" structure from the documentation and
replaces it with the unified **PyNanoClaw** hybrid system narrative that
the final assignment (2026-04-18) will actually build. No code changes —
students who already pulled [1.1.0] do not need to re-pull for anything to
run. This release is pure documentation alignment.

### Changed

- **Course structure: no more tracks.** The module was originally planned
  as two divergent tracks that students would pick between before Week 3.
  This has been removed. Everyone builds both halves — the autonomous
  LangGraph loop and the structured Rasa CALM agent — and composes them
  into one hybrid system called PyNanoClaw in the final assignment. The
  core lesson is that real agent systems combine open-ended reasoning
  with structured, auditable logic, and you only learn that by building
  both halves and seeing where each belongs. See `PROGRESS.md` for the
  full PyNanoClaw architecture diagram.
  *Files:* `PROGRESS.md`, `README.md`, `GRADING_OVERVIEW.md`, `.env.example`.

- **Terminology.** "The Headless Automator" → "the autonomous loop".
  "The Digital Employee" → "the structured agent". Both names made the
  halves sound like separate products rather than components of one
  system. The new terminology makes it clearer that neither half is
  complete on its own.
  *Files:* `README.md`, `PROGRESS.md`.

- **Voice pipeline is now explicitly optional.** Under the old two-track
  structure, the voice pipeline was a core feature of Track B. In the
  unified PyNanoClaw, voice is an optional wrapper around the structured
  agent — the core system works without it, and students who don't care
  about voice can skip it entirely without missing the main lesson.
  *File:* `.env.example` (Speechmatics section renamed from "TRACK B
  ONLY" to "OPTIONAL").

### Notes

**Impact on Week 1 submissions.** Zero. Week 1 exercises are unchanged;
every student was already building both halves. This release only affects
how the work is framed in the docs, not what gets graded.

**Impact on the final assignment.** The final assignment (2026-04-18)
now has a single, shared spec that everyone works against. There will
not be two parallel assignment documents. One scenario, one architecture,
one rubric — with the voice pipeline as an optional extension worth a
small amount of extra credit.

---

## [1.1.0] — 2026-04-13

Consolidated fix release ahead of the Week 1 submission deadline. Addresses
all blocking issues reported in `#module1-agents` and GitHub between
2026-04-01 and 2026-04-12. Pull `upstream/main` and re-run `make install`
to apply.

### Fixed

- **Ex1 — `SMALL_MODEL` points at a model removed on 2026-04-13**
  (2026-04-13 Nebius deprecation round) `exercise1_context.py` used
  `meta-llama/Meta-Llama-3.1-8B-Instruct` as the small stress-test
  model for Part C. Both variants of that model (Base and Fast) were
  removed from the Token Factory on 2026-04-13, so Part C would fail
  outright from that date forward. Migrated to `google/gemma-2-2b-it`,
  which is smaller and cheaper, and arguably a better pedagogical fit:
  structural formatting effects (lost-in-the-middle, distractor
  sensitivity) are more visible on a weaker model, so a 2B gives a
  clearer signal than the old 8B. `MAIN_MODEL` continues to use
  `meta-llama/Llama-3.3-70B-Instruct` — the Base variant survived the
  deprecation round; only the `_fast` variant was removed.
  *File:* `week1/exercise1_context.py`.

- **Ex2 / Ex4 — agent emits tool calls as text instead of executing them**
  (#2, #9; reproduced by @FabianTheFab, @WitnessOfThe, and several others)
  The scaffold's default model, `meta-llama/Llama-3.3-70B-Instruct`, does
  not reliably populate the OpenAI-spec `tool_calls` field on the Nebius
  Token Factory endpoint. It encodes intended tool calls as stringified
  JSON inside `content` — and, when it wants to call multiple tools in
  parallel, as a JSON list of JSON strings inside a single content block.
  LangGraph's `create_react_agent` finds `tool_calls=[]`, hands control
  back to the LLM, and the loop no-ops. Default model swapped to
  `Qwen/Qwen3-32B`, which emits native `tool_calls` correctly. The
  `RESEARCH_MODEL` environment variable overrides the default without
  code changes.
  *Files:* `sovereign_agent/agents/research_agent.py`,
  `week1/exercise4_mcp_client.py`.

- **Ex2 / Ex4 — trace parser drops tool calls from non-compliant models**
  (root-caused by @MartinSundin, @AnnaVinogradova)
  `_extract_tool_calls_from_message` now reads native `m.tool_calls`
  first and falls back to parsing the stringified-JSON-in-content shape
  so trace output remains correct even when users experiment with
  alternative models. Malformed JSON no longer raises.
  *File:* `sovereign_agent/agents/research_agent.py`.

- **Ex4 — MCP caller silently drops tool arguments** (#9; @FabianTheFab,
  @qm2k, @MartinSundin)
  `_make_mcp_caller` previously took `**kwargs`, which LangChain's
  `StructuredTool` wrapped under an inferred `kwargs` field, discarding
  the real tool arguments before they reached the MCP server. Caller now
  takes an explicit `input: dict`, merges any stray keyword arguments
  defensively, and forwards the result via `session.call_tool(name,
  arguments=merged)` per the MCP specification. `StructuredTool.
  from_function(..., args_schema=None)` prevents LangChain from
  re-introducing the problem via schema inference.
  *File:* `week1/exercise4_mcp_client.py`.

- **Ex4 — tool results not rendered in trace** (#9)
  `extract_trace` had no branch for `ToolMessage` objects, so tool
  invocations appeared in the trace but their return values did not.
  Added a `tool_result` role that captures and truncates tool output
  for display.
  *File:* `week1/exercise4_mcp_client.py`.

- **Ex3 — Rasa CALM fails with `Provider List:
  https://docs.litellm.ai/docs/providers`** (fixed by @AlexeyKhabalov)
  `endpoints.yml` specified `provider: self-hosted`, which litellm does
  not recognize. Switched to `provider: openai` with model names
  prefixed `openai/...`, which routes OpenAI-compatible endpoints
  (including Nebius Token Factory) through litellm's OpenAI adapter.
  Model groups also updated to Qwen3-32B for consistency with the
  research agent. **Re-run `make ex3-train` after pulling** — the model
  group is baked into the trained model at train time.
  *File:* `exercise3_rasa/endpoints.yml`.

- **grade.py — `TypeError` when checking `generate_event_flyer`** (#4;
  @qm2k) The grader called the flyer tool with `pub_name=`, but the
  function signature uses `venue_name=`. The grader crashed before
  evaluating whether the tool was implemented. Call site corrected.
  *File:* `week1/grade.py`.

- **grade.py — `FormValidationAction` false positive** (#10; @slenas)
  The grader flagged any occurrence of `FormValidationAction` as the
  deprecated Rasa pattern, including references inside the explanatory
  docstring block of `actions.py`. Grader now strips triple-quoted
  docstrings and `#` comments from source before searching, and only
  flags actual class definitions (`class FormValidationAction`) or
  instantiations (`FormValidationAction(`).
  *File:* `week1/grade.py` (`_strip_comments_and_docstrings`).

- **grade.py — `ModuleNotFoundError` aborts entire grading run** (#6;
  @FabianTheFab) If any optional dependency was missing from the active
  environment, module-level imports raised and blocked grading of
  unrelated exercises. Imports are now wrapped in `_safe_exec_module`,
  which distinguishes missing dependencies (reported as warnings with
  a "run `make install`" hint) from real import errors.
  *File:* `week1/grade.py`.

- **Makefile — `.env` validation false positive** (#1, #5;
  @FabianTheFab, PR by @RadionBik) `check-env` target grep-matched the
  placeholder string `sk-your-key-here` anywhere in `.env`, which
  collided with other placeholder values in the file. Target now parses
  the `NEBIUS_KEY=` line specifically and validates its value in
  isolation.
  *File:* `Makefile` (`check-env` target).

### Changed

- **Ex2 Task B — `generate_event_flyer` reimplemented with graceful
  fallback** (#3; reported by @wwymak)
  Nebius removed all text-to-image models (FLUX-schnell, FLUX-dev) from
  the Token Factory on 2026-04-13, eliminating the provider the original
  task targeted. The same deprecation round also removed several text
  models the scaffold referenced elsewhere (see the Ex1 `SMALL_MODEL`
  entry above). The tool now attempts live image generation if
  `FLYER_IMAGE_MODEL` is set in the environment, and otherwise returns
  a deterministic `placehold.co` URL with `mode: "placeholder"` and the
  full prompt recorded for audit. The tool contract (`success=True`,
  `prompt_used`, `image_url`) is satisfied in both paths, and the tool
  never raises — preserving the ReAct loop's control flow across
  provider failures. Students who want live image generation can wire
  in any non-Nebius provider (OpenAI, Replicate, local SDXL) through
  `FLYER_IMAGE_MODEL` without touching the code.
  *File:* `sovereign_agent/tools/venue_tools.py`. See
  [Nebius deprecation notice](https://docs.tokenfactory.nebius.com/other-capabilities/deprecation-info).

- **grade.py — `WEEK_5_ARCHITECTURE` check relaxed** (raised by
  @AlexeyKhabalov) The field describes Week 5 architecture that has
  not yet been covered in class. Grader now returns `PASS` at 5+
  bullets, `WARN` at 3–4, and `FAIL` only when the field is blank.
  The prompt in `ex4_answers.py` now clearly frames it as a speculative
  exercise based on `PROGRESS.md`, with an example of the level of
  detail expected.
  *Files:* `week1/grade.py`, `week1/answers/ex4_answers.py`.

### Added

- **Course structure consolidation — two assignments total**
  The module was originally scheduled to include three homework
  assignments. This has been reduced to two:
  - **Assignment 1** (this release): Week 1 foundations.
  - **Assignment 2** (release date 2026-04-18): consolidated
    Week 3–5 assignment, covering planner/executor split, memory,
    observability, the voice pipeline, and the full PyNanoClaw demo.
  Week 2's scheduled session proceeds as planned; its material feeds
  directly into Assignment 2.

### Notes

**Submission mechanics.** Submissions are read from the `main` branch
of each student's GitHub fork. There is no separate upload or form.
Commits on feature branches are not graded.

```bash
git checkout main
git merge <your-branch>
make check-submit
git push origin main
```

**Deadline.** The final commit must land on `main` by
**2026-04-13 23:59 UTC−12** (equivalent to **2026-04-14 12:00 London
time**). Commits after this timestamp are not graded.

**Workarounds honored.** Students who patched the scaffold locally
before this release do not need to revert their changes. The grader
evaluates the submitted code against the intended behaviour, not
against conformance with the canonical patch. Specifically:

- Any alternative model that emits correct `tool_calls` and is NOT
  on the 2026-04-13 Nebius deprecation list is accepted. Good picks:
  `Qwen/Qwen3-32B` (the scaffold default, Base variant),
  `nvidia/nemotron-3-super-120b-a12b`,
  `Qwen/Qwen3-Next-80B-A3B-Thinking`. Do **not** use
  `deepseek-ai/DeepSeek-R1-0528` — it was deprecated in the same round
  as FLUX. Avoid any model suffixed `_fast` in the Qwen, Llama, or
  DeepSeek families. Record the model used in `ex2_answers.py` →
  `TASK_A_NOTES`.
- Any working `generate_event_flyer` implementation is accepted,
  including direct calls to non-Nebius providers (OpenAI, Replicate,
  local SDXL). Wrap such calls in `try/except` to guard against
  provider unavailability and return the fallback shape on failure.
- Local parser fixes to `research_agent.py` that predate the defensive
  parser in this release are accepted.
- Renames of `FormValidationAction` inside comments made to work around
  the grader bug (#10) may be reverted or left in place.

**Bug reports and PRs.** Issues filed and PRs opened against the
scaffold during the assignment window are tracked against submissions
at grading time. Reproducing a bug with a minimal case, isolating the
root cause, or proposing a fix counts as open-source contribution
credit.

### Office hours

Final session before the Assignment 1 deadline:

- **Date:** 2026-04-13, 18:30 London time (1 hour)
- **Zoom:** https://rasa.zoom.us/j/85135751478?pwd=pvEBhgIxqGo5ibEmtIPE3ebePQcDdM.1
- **Meeting ID:** 851 3575 1478 · **Passcode:** 934561

Session is not recorded. A takeaways summary will be posted to
`#module1-agents` afterwards.

### Upgrade path

From an existing fork:

```bash
git fetch upstream
git merge upstream/main
make install
make smoke
make ex2-a       # verify tool calls now execute
make ex4         # verify MCP bridge works
make check-submit
```

Merge conflicts are most likely in `sovereign_agent/agents/research_agent.py`
and `sovereign_agent/tools/venue_tools.py` for students who applied local
patches. Conflicts in any file not listed under *Fixed* or *Changed* above
are unexpected; report via GitHub issue with the conflict block attached.

---

## [1.0.0] — 2026-03-31

Initial release of the Week 1 Sovereign Agent Lab assignment.

### Added

- Exercise 1: context engineering benchmark (plain / XML / sandwich
  presentation formats on frontier and small models).
- Exercise 2: LangGraph ReAct research agent with four venue tools
  (`check_pub_availability`, `get_edinburgh_weather`,
  `calculate_catering_cost`, `generate_event_flyer`).
- Exercise 3: Rasa Pro CALM confirmation agent with `confirm_booking`
  flow and `ActionValidateBooking` custom action enforcing three
  business constraints.
- Exercise 4: shared MCP venue server (`mcp_venue_server.py`) and
  LangGraph client demonstrating tool-layer portability.
- `sovereign_agent/` persistent project skeleton designed to extend
  across Weeks 2–5.
- `grade.py` mechanical checker, `check-submit` Makefile target,
  and `GRADING_OVERVIEW.md` describing the 30/40/30 point breakdown.
- `PROGRESS.md` describing the five-week arc and track selection
  (OpenClaw Automator vs Rasa Digital Employee). *Superseded in [1.2.0]
  — the two-track structure was consolidated into the unified PyNanoClaw
  hybrid system.*

### Known issues at release

See entries in [1.1.0] above.