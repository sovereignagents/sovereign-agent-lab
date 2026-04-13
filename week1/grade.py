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
"""

import importlib.util
import json
import sys
from pathlib import Path

ROOT    = Path(__file__).parent.parent
WEEK1   = ROOT / "week1"
OUTPUTS = WEEK1 / "outputs"
ANSWERS = WEEK1 / "answers"

PASS = "✅"
FAIL = "❌"
WARN = "⚠️ "

_results = []


def record(status: str, msg: str) -> None:
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
    mod  = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        return mod
    except Exception as e:
        record(FAIL, f"Could not import {name}.py: {e}")
        return None


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

    for var in ["PART_A_PLAIN_ANSWER", "PART_A_XML_ANSWER", "PART_A_SANDWICH_ANSWER",
                "PART_B_PLAIN_ANSWER", "PART_B_XML_ANSWER", "PART_B_SANDWICH_ANSWER"]:
        val = getattr(a, var, "FILL_ME_IN")
        record(PASS if is_filled(val) else FAIL, f"{var} filled in")

    for var in ["PART_A_PLAIN_CORRECT", "PART_A_XML_CORRECT", "PART_A_SANDWICH_CORRECT",
                "PART_B_PLAIN_CORRECT", "PART_B_XML_CORRECT", "PART_B_SANDWICH_CORRECT",
                "PART_B_CHANGED_RESULTS", "PART_C_WAS_RUN"]:
        val = getattr(a, var, None)
        record(PASS if val is not None else FAIL, f"{var} set to True or False")

    # Check Part A answers are consistent with JSON
    for cond in ["PLAIN", "XML", "SANDWICH"]:
        ans = getattr(a, f"PART_A_{cond}_CORRECT", None)
        jsn = out.get("part_a", {}).get(cond, {}).get("correct")
        if ans is not None and jsn is not None and ans != jsn:
            record(WARN, f"PART_A_{cond}_CORRECT ({ans}) differs from JSON ({jsn}) — re-check your output")

    for var, min_w in [("PART_A_EXPLANATION", 30), ("PART_B_HARDEST_DISTRACTOR", 20),
                        ("PART_C_EXPLANATION", 30), ("CORE_LESSON", 40)]:
        val = getattr(a, var, "")
        wc  = word_count(val)
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

    # Check that sovereign_agent modules import cleanly
    for module_path, import_name in [
        (ROOT / "sovereign_agent" / "tools" / "venue_tools.py",    "venue_tools"),
        (ROOT / "sovereign_agent" / "agents" / "research_agent.py", "research_agent"),
    ]:
        if module_path.exists():
            spec = importlib.util.spec_from_file_location(import_name, module_path)
            mod  = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(mod)
                record(PASS, f"sovereign_agent/{module_path.name} imports without error")
            except Exception as e:
                record(FAIL, f"sovereign_agent/{module_path.name} import error: {e}")
        else:
            record(FAIL, f"sovereign_agent/{module_path.parent.name}/{module_path.name} not found")

    # Check generate_event_flyer is not still a stub
    vt_path = ROOT / "sovereign_agent" / "tools" / "venue_tools.py"
    if vt_path.exists():
        spec = importlib.util.spec_from_file_location("venue_tools_check", vt_path)
        mod  = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            fn = getattr(mod, "generate_event_flyer", None)
            if fn:
                raw_fn = fn.func if hasattr(fn, "func") else fn
                raw    = raw_fn(pub_name="Test", guest_count=10, event_theme="test")
                parsed = json.loads(raw) if isinstance(raw, str) else raw
                is_stub = "STUB" in str(parsed.get("error", ""))
                record(
                    FAIL if is_stub else PASS,
                    "generate_event_flyer is implemented (not stub)"
                    if not is_stub
                    else "generate_event_flyer still returns stub — implement the TODO in venue_tools.py",
                )
        except Exception as e:
            record(WARN, f"Could not call generate_event_flyer directly: {e}")

    a = load_answers("ex2_answers")
    if not a:
        return

    tools = getattr(a, "TASK_A_TOOLS_CALLED", [])
    record(
        PASS if isinstance(tools, list) and len(tools) >= 2 else FAIL,
        f"TASK_A_TOOLS_CALLED has ≥ 2 entries (found {len(tools) if isinstance(tools, list) else 0})",
    )

    venue = getattr(a, "TASK_A_CONFIRMED_VENUE", "FILL_ME_IN")
    record(
        PASS if venue in {"The Albanach", "The Haymarket Vaults", "none"} else FAIL,
        f"TASK_A_CONFIRMED_VENUE is a known venue name (got: '{venue}')",
    )

    for var in ["TASK_A_OUTDOOR_OK", "TASK_B_IMPLEMENTED",
                "SCENARIO_2_HALLUCINATED", "SCENARIO_3_TRIED_A_TOOL"]:
        val = getattr(a, var, None)
        record(PASS if val is not None else FAIL, f"{var} set to True or False")

    mermaid = getattr(a, "TASK_D_MERMAID_OUTPUT", "")
    record(
        PASS if is_filled(mermaid) and ("graph" in mermaid.lower() or "flowchart" in mermaid.lower())
        else FAIL,
        "TASK_D_MERMAID_OUTPUT contains Mermaid graph syntax",
    )

    for var, min_w in [("SCENARIO_1_PIVOT_MOMENT", 20), ("SCENARIO_3_ACCEPTABLE", 30),
                        ("TASK_D_COMPARISON", 30), ("MOST_SURPRISING", 40)]:
        val = getattr(a, var, "")
        wc  = word_count(val)
        record(
            PASS if is_filled(val) and wc >= min_w else FAIL,
            f"{var} filled in and ≥ {min_w} words (found {wc})",
        )


# ─────────────────────────────────────────────────────────────────────────────
# Exercise 3
# ─────────────────────────────────────────────────────────────────────────────

def check_ex3() -> None:
    record(None, "── Exercise 3 ──────────────────────────────────────────")

    # Check CALM required files exist
    for fname, label in [
        ("exercise3_rasa/config.yml",       "config.yml"),
        ("exercise3_rasa/domain.yml",       "domain.yml"),
        ("exercise3_rasa/endpoints.yml",    "endpoints.yml"),
        ("exercise3_rasa/data/flows.yml",   "data/flows.yml (CALM flows)"),
    ]:
        path = ROOT / fname
        record(PASS if path.exists() else FAIL,
               f"{label} exists" if path.exists()
               else f"{label} missing — check exercise3_rasa/ structure")

    actions_path = ROOT / "exercise3_rasa" / "actions" / "actions.py"
    if actions_path.exists():
        source = actions_path.read_text()
        guard_present = (
            "datetime.datetime.now()" in source
            and "now.hour" in source
            and "# now = datetime" not in source.split("now.hour")[0].split("\n")[-1]
        )
        record(
            PASS if guard_present else FAIL,
            "Cutoff guard is uncommented in exercise3_rasa/actions/actions.py"
            if guard_present
            else "Cutoff guard still commented out — uncomment the TASK B block in actions.py",
        )
        # CALM: no FormValidationAction needed
        has_form_action = "FormValidationAction" in source
        record(
            PASS if not has_form_action else WARN,
            "No FormValidationAction (correct — CALM handles slot extraction via LLM)"
            if not has_form_action
            else "FormValidationAction found — not needed in CALM (from_llm slots handle extraction)",
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
            looks_real = any(marker in trace for marker in
                             ["Your input", "input →", "Bot", "bot", ">"])
            record(
                PASS if looks_real else WARN,
                f"CONVERSATION_{num}_TRACE looks like real rasa shell output"
                if looks_real
                else f"CONVERSATION_{num}_TRACE may not be a real rasa shell trace",
            )

    conv1 = getattr(a, "CONVERSATION_1_OUTCOME", "FILL_ME_IN")
    record(PASS if conv1 in {"confirmed", "escalated"} else FAIL,
           f"CONVERSATION_1_OUTCOME is 'confirmed' or 'escalated' (got: '{conv1}')")

    conv2 = getattr(a, "CONVERSATION_2_OUTCOME", "FILL_ME_IN")
    record(PASS if conv2 == "escalated" else FAIL,
           "CONVERSATION_2_OUTCOME is 'escalated' for over-limit deposit")

    task_b = getattr(a, "TASK_B_DONE", None)
    record(PASS if task_b is True else FAIL, "TASK_B_DONE = True")

    files = getattr(a, "TASK_B_FILES_CHANGED", [])
    record(PASS if isinstance(files, list) and len(files) >= 1 else FAIL,
           f"TASK_B_FILES_CHANGED lists at least 1 file (found {len(files) if isinstance(files, list) else 0})")

    for var, min_w in [("OUT_OF_SCOPE_COMPARISON", 40), ("SETUP_COST_VALUE", 40),
                        ("TASK_B_HOW_YOU_TESTED", 20), ("CALM_VS_OLD_RASA", 30)]:
        val = getattr(a, var, "")
        wc  = word_count(val)
        record(
            PASS if is_filled(val) and wc >= min_w else FAIL,
            f"{var} filled in and ≥ {min_w} words (found {wc})",
        )


# ─────────────────────────────────────────────────────────────────────────────
# Exercise 4
# ─────────────────────────────────────────────────────────────────────────────

def check_ex4() -> None:
    record(None, "── Exercise 4 ──────────────────────────────────────────")

    mcp_path = ROOT / "sovereign_agent" / "tools" / "mcp_venue_server.py"
    record(PASS if mcp_path.exists() else FAIL,
           "sovereign_agent/tools/mcp_venue_server.py exists")

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
    record(PASS if isinstance(tools, list) and len(tools) >= 2 else FAIL,
           f"TOOLS_DISCOVERED has ≥ 2 entries (found {len(tools) if isinstance(tools, list) else 0})")

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
    record(PASS if exp_done is True else FAIL,
           "EX4_EXPERIMENT_DONE = True (you modified venue_server.py and re-ran)")

    for var, min_w in [("EX4_EXPERIMENT_RESULT", 30), ("MCP_VALUE_PROPOSITION", 30),
                        ("GUIDING_QUESTION_ANSWER", 60)]:
        val = getattr(a, var, "")
        wc  = word_count(val)
        record(
            PASS if is_filled(val) and wc >= min_w else FAIL,
            f"{var} filled in and ≥ {min_w} words (found {wc})",
        )

    arch = getattr(a, "WEEK_5_ARCHITECTURE", "")
    bullet_count = sum(1 for line in str(arch).splitlines() if line.strip().startswith("-"))
    record(
        PASS if is_filled(arch) and bullet_count >= 5 else FAIL,
        f"WEEK_5_ARCHITECTURE has ≥ 5 bullet points (found {bullet_count})",
    )


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

    if which in ("all", "ex1"): check_ex1()
    if which in ("all", "ex2"): check_ex2()
    if which in ("all", "ex3"): check_ex3()
    if which in ("all", "ex4"): check_ex4()

    sys.exit(print_results())
