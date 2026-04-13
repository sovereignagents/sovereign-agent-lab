"""
Week 1 — Mechanical Grade Check
=================================
Run this before submitting. It checks things that can be verified
automatically. It does NOT check reasoning quality or behavioural
correctness — those are graded separately by the instructor.

Usage:
    python week1/grade.py          # check everything
    python week1/grade.py ex1      # Exercise 1 only
    python week1/grade.py ex2      # Exercise 2 only
    python week1/grade.py ex3      # Exercise 3 only
    python week1/grade.py ex4      # Exercise 4 only

A ✅ means the check passed.
A ❌ means something is wrong — fix it before submitting.
A ⚠️  means something looks unusual but may still be acceptable.

────────────────────────────────────────────────────────────────────────────
FIXES APPLIED 2026-04-09
  - Exercise 2 flyer-tool check now uses `venue_name=` (not `pub_name=`).
  - Exercise 2 module imports are now defensive — a missing optional
    dependency no longer blocks grading unrelated exercises.
  - Exercise 2 no longer fails flyer tool when it returns the graceful
    placeholder fallback (the fallback is a valid implementation, not a stub).
  - Exercise 3 no longer false-flags the word "FormValidationAction" when
    it appears only in a comment block; we check for actual class usage.
  - Exercise 4 WEEK_5_ARCHITECTURE is now a WARNING instead of a FAIL
    if it has fewer bullets — it is a speculation question based on
    PROGRESS.md, not a test of material you have seen in class yet.
────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
WEEK1 = ROOT / "week1"
OUTPUTS = WEEK1 / "outputs"
ANSWERS = WEEK1 / "answers"

PASS = "✅"
FAIL = "❌"
WARN = "⚠️ "

_results: list[tuple[str | None, str]] = []


def record(status: str | None, msg: str) -> None:
    _results.append((status, msg))


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return {"_parse_error": True}


def load_answers(name: str):
    path = ANSWERS / f"{name}.py"
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        return mod
    except Exception as e:
        record(FAIL, f"Could not import {name}.py: {e}")
        return None


def _safe_exec_module(path: Path, label: str):
    """Import a module file and return (module, error_message_or_None)."""
    if not path.exists():
        return None, f"{label} not found at {path}"
    spec = importlib.util.spec_from_file_location(f"_grade_{label}", path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        return mod, None
    except ModuleNotFoundError as e:
        return None, f"missing dependency ({e.name}) — run `make install`"
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def is_filled(v) -> bool:
    s = str(v).strip()
    return (
        v is not None
        and s not in {"FILL_ME_IN", "FILL_ME_IN_OR_N/A", "[]", "0", ""}
        and "FILL ME IN" not in s
        and "PASTE" not in s
    )


def word_count(s: str) -> int:
    return len(str(s).split())


# ─────────────────────────────────────────────────────────────────────────────
# Exercise 1
# ─────────────────────────────────────────────────────────────────────────────

def check_ex1() -> None:
    record(None, "── Exercise 1 ──────────────────────────────────────────")

    out = load_json(OUTPUTS / "ex1_results.json")
    record(
        PASS if (out and "_parse_error" not in out) else FAIL,
        "outputs/ex1_results.json exists and is valid"
        if (out and "_parse_error" not in out)
        else "outputs/ex1_results.json missing or invalid — run exercise1_context.py",
    )
    if not out:
        return

    a = load_answers("ex1_answers")
    if not a:
        return

    for var in [
        "PART_A_PLAIN_ANSWER",
        "PART_A_XML_ANSWER",
        "PART_A_SANDWICH_ANSWER",
        "PART_B_PLAIN_ANSWER",
        "PART_B_XML_ANSWER",
        "PART_B_SANDWICH_ANSWER",
    ]:
        val = getattr(a, var, "FILL_ME_IN")
        record(PASS if is_filled(val) else FAIL, f"{var} filled in")

    for var in [
        "PART_A_PLAIN_CORRECT",
        "PART_A_XML_CORRECT",
        "PART_A_SANDWICH_CORRECT",
        "PART_B_PLAIN_CORRECT",
        "PART_B_XML_CORRECT",
        "PART_B_SANDWICH_CORRECT",
        "PART_B_CHANGED_RESULTS",
        "PART_C_WAS_RUN",
    ]:
        val = getattr(a, var, None)
        record(PASS if val is not None else FAIL, f"{var} set to True or False")

    for cond in ["PLAIN", "XML", "SANDWICH"]:
        ans = getattr(a, f"PART_A_{cond}_CORRECT", None)
        jsn = out.get("part_a", {}).get(cond, {}).get("correct")
        if ans is not None and jsn is not None and ans != jsn:
            record(
                WARN,
                f"PART_A_{cond}_CORRECT ({ans}) differs from JSON ({jsn}) — re-check your output",
            )

    for var, min_w in [
        ("PART_A_EXPLANATION", 30),
        ("PART_B_HARDEST_DISTRACTOR", 20),
        ("PART_C_EXPLANATION", 30),
        ("CORE_LESSON", 40),
    ]:
        val = getattr(a, var, "")
        wc = word_count(val)
        record(
            PASS if is_filled(val) and wc >= min_w else FAIL,
            f"{var} filled in and ≥ {min_w} words (found {wc})",
        )


# ─────────────────────────────────────────────────────────────────────────────
# Exercise 2
# ─────────────────────────────────────────────────────────────────────────────

def check_ex2() -> None:
    record(None, "── Exercise 2 ──────────────────────────────────────────")

    out = load_json(OUTPUTS / "ex2_results.json")
    record(
        PASS if (out and "_parse_error" not in out) else FAIL,
        "outputs/ex2_results.json exists and is valid"
        if (out and "_parse_error" not in out)
        else "outputs/ex2_results.json missing or invalid — run exercise2_langgraph.py",
    )

    # Defensive module import — a missing optional dep no longer nukes grading.
    for module_path, label in [
        (ROOT / "sovereign_agent" / "tools" / "venue_tools.py", "venue_tools"),
        (ROOT / "sovereign_agent" / "agents" / "research_agent.py", "research_agent"),
    ]:
        mod, err = _safe_exec_module(module_path, label)
        if mod is not None:
            record(PASS, f"sovereign_agent/{label}.py imports without error")
        else:
            # Dependency errors are a WARN not FAIL — they block this check
            # but the student may still have a valid implementation.
            if "missing dependency" in (err or ""):
                record(WARN, f"sovereign_agent/{label}.py: {err}")
            else:
                record(FAIL, f"sovereign_agent/{label}.py import error: {err}")

    # Check generate_event_flyer is not still the literal stub.
    vt_path = ROOT / "sovereign_agent" / "tools" / "venue_tools.py"
    vt_mod, _ = _safe_exec_module(vt_path, "venue_tools_check")
    if vt_mod is not None:
        fn = getattr(vt_mod, "generate_event_flyer", None)
        if fn:
            try:
                raw_fn = fn.func if hasattr(fn, "func") else fn
                # The parameter is `venue_name`, not `pub_name` — this was a
                # bug in the earlier grader.
                raw = raw_fn(
                    venue_name="The Haymarket Vaults",
                    guest_count=10,
                    event_theme="test",
                )
                parsed = json.loads(raw) if isinstance(raw, str) else raw

                # A valid implementation returns success=True, regardless of
                # whether it used a live provider or the placeholder fallback.
                # The OLD stub returned success=False with "STUB" in the error.
                is_stub = (
                    parsed.get("success") is False
                    and "STUB" in str(parsed.get("error", "")).upper()
                )
                has_url = bool(parsed.get("image_url"))
                record(
                    FAIL if is_stub else PASS,
                    "generate_event_flyer is implemented (not stub)"
                    if not is_stub
                    else "generate_event_flyer still returns stub — see venue_tools.py",
                )
                if not is_stub and not has_url:
                    record(WARN, "generate_event_flyer returned no image_url")
            except TypeError as e:
                record(
                    FAIL,
                    f"generate_event_flyer signature mismatch: {e} "
                    "(expected venue_name, guest_count, event_theme)",
                )
            except Exception as e:
                record(WARN, f"Could not call generate_event_flyer directly: {e}")

    a = load_answers("ex2_answers")
    if not a:
        return

    tools = getattr(a, "TASK_A_TOOLS_CALLED", [])
    record(
        PASS if isinstance(tools, list) and len(tools) >= 2 else FAIL,
        f"TASK_A_TOOLS_CALLED has ≥ 2 entries "
        f"(found {len(tools) if isinstance(tools, list) else 0})",
    )

    venue = getattr(a, "TASK_A_CONFIRMED_VENUE", "FILL_ME_IN")
    record(
        PASS if venue in {"The Albanach", "The Haymarket Vaults", "none"} else FAIL,
        f"TASK_A_CONFIRMED_VENUE is a known venue name (got: '{venue}')",
    )

    for var in [
        "TASK_A_OUTDOOR_OK",
        "TASK_B_IMPLEMENTED",
        "SCENARIO_2_HALLUCINATED",
        "SCENARIO_3_TRIED_A_TOOL",
    ]:
        val = getattr(a, var, None)
        record(PASS if val is not None else FAIL, f"{var} set to True or False")

    mermaid = getattr(a, "TASK_D_MERMAID_OUTPUT", "")
    record(
        PASS
        if is_filled(mermaid) and ("graph" in mermaid.lower() or "flowchart" in mermaid.lower())
        else FAIL,
        "TASK_D_MERMAID_OUTPUT contains Mermaid graph syntax",
    )

    for var, min_w in [
        ("SCENARIO_1_PIVOT_MOMENT", 20),
        ("SCENARIO_3_ACCEPTABLE", 30),
        ("TASK_D_COMPARISON", 30),
        ("MOST_SURPRISING", 40),
    ]:
        val = getattr(a, var, "")
        wc = word_count(val)
        record(
            PASS if is_filled(val) and wc >= min_w else FAIL,
            f"{var} filled in and ≥ {min_w} words (found {wc})",
        )


# ─────────────────────────────────────────────────────────────────────────────
# Exercise 3
# ─────────────────────────────────────────────────────────────────────────────

# Strip out Python comments and triple-quoted docstrings so we don't match
# reference text like "in old Rasa you had a FormValidationAction".
def _strip_comments_and_docstrings(source: str) -> str:
    # Remove triple-quoted strings (docstrings / multi-line comments-as-strings)
    source = re.sub(r'"""[\s\S]*?"""', "", source)
    source = re.sub(r"'''[\s\S]*?'''", "", source)
    # Remove single-line # comments
    lines = [re.sub(r"(?<!['\"])#.*$", "", ln) for ln in source.splitlines()]
    return "\n".join(lines)


def check_ex3() -> None:
    record(None, "── Exercise 3 ──────────────────────────────────────────")

    for fname, label in [
        ("exercise3_rasa/config.yml", "config.yml"),
        ("exercise3_rasa/domain.yml", "domain.yml"),
        ("exercise3_rasa/endpoints.yml", "endpoints.yml"),
        ("exercise3_rasa/data/flows.yml", "data/flows.yml (CALM flows)"),
    ]:
        path = ROOT / fname
        record(
            PASS if path.exists() else FAIL,
            f"{label} exists"
            if path.exists()
            else f"{label} missing — check exercise3_rasa/ structure",
        )

    actions_path = ROOT / "exercise3_rasa" / "actions" / "actions.py"
    if actions_path.exists():
        source = actions_path.read_text()
        code_only = _strip_comments_and_docstrings(source)

        # Cutoff guard: at least one un-commented `now = datetime.datetime.now()`
        # AND a `now.hour` reference in code (not in a docstring or comment).
        guard_present = (
            "datetime.datetime.now()" in code_only and "now.hour" in code_only
        )
        record(
            PASS if guard_present else FAIL,
            "Cutoff guard is uncommented in exercise3_rasa/actions/actions.py"
            if guard_present
            else "Cutoff guard still commented out — uncomment the TASK B block in actions.py",
        )

        # CALM: no FormValidationAction needed. Only flag if the word appears
        # in ACTUAL CODE (class definition or instantiation), not in the
        # explanatory comment block at the top of the file.
        has_form_action_in_code = bool(
            re.search(r"\bclass\s+FormValidationAction\b", code_only)
            or re.search(r"\bFormValidationAction\s*\(", code_only)
        )
        record(
            PASS if not has_form_action_in_code else WARN,
            "No FormValidationAction class in code (correct — CALM handles slot extraction)"
            if not has_form_action_in_code
            else "FormValidationAction used in code — not needed in CALM",
        )
    else:
        record(FAIL, "exercise3_rasa/actions/actions.py not found")

    a = load_answers("ex3_answers")
    if not a:
        return

    for num in [1, 2, 3]:
        trace = getattr(a, f"CONVERSATION_{num}_TRACE", "")
        filled = is_filled(trace)
        record(PASS if filled else FAIL, f"CONVERSATION_{num}_TRACE filled in")
        if filled:
            looks_real = any(
                marker in trace
                for marker in ["Your input", "input →", "Bot", "bot", ">"]
            )
            record(
                PASS if looks_real else WARN,
                f"CONVERSATION_{num}_TRACE looks like real rasa shell output"
                if looks_real
                else f"CONVERSATION_{num}_TRACE may not be a real rasa shell trace",
            )

    conv1 = getattr(a, "CONVERSATION_1_OUTCOME", "FILL_ME_IN")
    record(
        PASS if conv1 in {"confirmed", "escalated"} else FAIL,
        f"CONVERSATION_1_OUTCOME is 'confirmed' or 'escalated' (got: '{conv1}')",
    )

    conv2 = getattr(a, "CONVERSATION_2_OUTCOME", "FILL_ME_IN")
    record(
        PASS if conv2 == "escalated" else FAIL,
        "CONVERSATION_2_OUTCOME is 'escalated' for over-limit deposit",
    )

    task_b = getattr(a, "TASK_B_DONE", None)
    record(PASS if task_b is True else FAIL, "TASK_B_DONE = True")

    files = getattr(a, "TASK_B_FILES_CHANGED", [])
    record(
        PASS if isinstance(files, list) and len(files) >= 1 else FAIL,
        f"TASK_B_FILES_CHANGED lists at least 1 file "
        f"(found {len(files) if isinstance(files, list) else 0})",
    )

    for var, min_w in [
        ("OUT_OF_SCOPE_COMPARISON", 40),
        ("SETUP_COST_VALUE", 40),
        ("TASK_B_HOW_YOU_TESTED", 20),
    ]:
        val = getattr(a, var, "")
        wc = word_count(val)
        record(
            PASS if is_filled(val) and wc >= min_w else FAIL,
            f"{var} filled in and ≥ {min_w} words (found {wc})",
        )

    # CALM_VS_OLD_RASA is now a WARN instead of FAIL.
    #
    # Rationale (2026-04-13, addressing anonymous cohort feedback):
    # This field asks students to compare Rasa Pro CALM to "old Rasa"
    # (the pre-CALM open-source 3.x release line). Students in this cohort
    # were never taught old Rasa and have no reason to know it. Asking a
    # 30-word comparison as a FAIL-blocking check punishes people for not
    # having done prior work outside the course. A student who leaves it
    # blank is not demonstrating incompetence — they are demonstrating that
    # they read only the material they were assigned.
    #
    # We keep the prompt in ex3_answers.py for anyone who does know old Rasa
    # and wants to answer (it's a reasonable reflection for context), but
    # we downgrade the check so that a blank or short answer cannot block
    # submission. This mirrors how we already handle WEEK_5_ARCHITECTURE.
    calm = getattr(a, "CALM_VS_OLD_RASA", "")
    calm_wc = word_count(calm)
    if is_filled(calm) and calm_wc >= 30:
        record(PASS, f"CALM_VS_OLD_RASA filled in and ≥ 30 words (found {calm_wc})")
    elif is_filled(calm):
        record(
            WARN,
            f"CALM_VS_OLD_RASA has {calm_wc} words — aim for 30 if you know old Rasa, "
            f"otherwise leave as-is (not blocking)",
        )
    else:
        record(
            WARN,
            "CALM_VS_OLD_RASA not filled in — optional, not blocking. "
            "This question assumes familiarity with pre-CALM Rasa which "
            "was not part of the course material.",
        )


# ─────────────────────────────────────────────────────────────────────────────
# Exercise 4
# ─────────────────────────────────────────────────────────────────────────────

def check_ex4() -> None:
    record(None, "── Exercise 4 ──────────────────────────────────────────")

    mcp_path = ROOT / "sovereign_agent" / "tools" / "mcp_venue_server.py"
    record(
        PASS if mcp_path.exists() else FAIL,
        "sovereign_agent/tools/mcp_venue_server.py exists",
    )

    out = load_json(OUTPUTS / "ex4_results.json")
    record(
        PASS if (out and "_parse_error" not in out) else FAIL,
        "outputs/ex4_results.json exists and is valid"
        if (out and "_parse_error" not in out)
        else "outputs/ex4_results.json missing — run exercise4_mcp_client.py",
    )

    a = load_answers("ex4_answers")
    if not a:
        return

    tools = getattr(a, "TOOLS_DISCOVERED", [])
    record(
        PASS if isinstance(tools, list) and len(tools) >= 2 else FAIL,
        f"TOOLS_DISCOVERED has ≥ 2 entries "
        f"(found {len(tools) if isinstance(tools, list) else 0})",
    )

    json_tools = out.get("tools_discovered", []) if out else []
    if json_tools and isinstance(tools, list) and tools:
        record(
            PASS if set(tools) == set(json_tools) else WARN,
            f"TOOLS_DISCOVERED matches JSON ({json_tools})"
            if set(tools) == set(json_tools)
            else f"TOOLS_DISCOVERED {tools} differs from JSON {json_tools}",
        )

    for var in ["QUERY_1_VENUE_NAME", "QUERY_1_VENUE_ADDRESS", "QUERY_2_FINAL_ANSWER"]:
        val = getattr(a, var, "FILL_ME_IN")
        record(PASS if is_filled(val) else FAIL, f"{var} filled in")

    exp_done = getattr(a, "EX4_EXPERIMENT_DONE", None)
    record(
        PASS if exp_done is True else FAIL,
        "EX4_EXPERIMENT_DONE = True (you modified venue_server.py and re-ran)",
    )

    for var, min_w in [
        ("EX4_EXPERIMENT_RESULT", 30),
        ("MCP_VALUE_PROPOSITION", 30),
        ("GUIDING_QUESTION_ANSWER", 60),
    ]:
        val = getattr(a, var, "")
        wc = word_count(val)
        record(
            PASS if is_filled(val) and wc >= min_w else FAIL,
            f"{var} filled in and ≥ {min_w} words (found {wc})",
        )

    # WEEK_5_ARCHITECTURE is now a WARN instead of FAIL when short.
    # It is speculative — based on PROGRESS.md, not on material students
    # have covered in class yet. A short answer should still prompt the
    # student to revisit it, but should not block submission.
    arch = getattr(a, "WEEK_5_ARCHITECTURE", "")
    bullet_count = sum(
        1 for line in str(arch).splitlines() if line.strip().startswith("-")
    )
    if is_filled(arch) and bullet_count >= 5:
        record(PASS, f"WEEK_5_ARCHITECTURE has ≥ 5 bullet points (found {bullet_count})")
    elif is_filled(arch) and bullet_count >= 3:
        record(
            WARN,
            f"WEEK_5_ARCHITECTURE has {bullet_count} bullets — aim for 5, "
            f"see PROGRESS.md for the five-week arc",
        )
    else:
        record(FAIL, "WEEK_5_ARCHITECTURE not filled in — see PROGRESS.md")


# ─────────────────────────────────────────────────────────────────────────────
# Print and exit
# ─────────────────────────────────────────────────────────────────────────────

def print_results() -> int:
    failures = warnings = passes = 0
    for status, msg in _results:
        if status is None:
            print(f"\n{msg}")
        elif status == PASS:
            print(f"  {PASS}  {msg}")
            passes += 1
        elif status == FAIL:
            print(f"  {FAIL}  {msg}")
            failures += 1
        elif status == WARN:
            print(f"  {WARN} {msg}")
            warnings += 1

    print(f"\n{'─' * 60}")
    print(f"  Passed:   {passes}")
    print(f"  Failed:   {failures}")
    print(f"  Warnings: {warnings}")

    if failures == 0 and warnings == 0:
        print("\n  🎉  All checks passed.")
    elif failures == 0:
        print("\n  ✅  No failures. Review warnings before submitting.")
    else:
        print(f"\n  Fix the {failures} failure(s) above before submitting.")
        print("  Run `uv run pytest sovereign_agent/tests/test_week1.py -v`")
        print("  for more specific error messages on tool failures.")

    return failures


if __name__ == "__main__":
    which = sys.argv[1].lower() if len(sys.argv) > 1 else "all"
    print("Week 1 — Mechanical Grade Check")
    print("=" * 60)
    print("(Checks code runs and answers are filled in.")
    print(" Reasoning quality and behavioural correctness")
    print(" are graded separately by the instructor.)\n")

    if which in ("all", "ex1"):
        check_ex1()
    if which in ("all", "ex2"):
        check_ex2()
    if which in ("all", "ex3"):
        check_ex3()
    if which in ("all", "ex4"):
        check_ex4()

    sys.exit(print_results())