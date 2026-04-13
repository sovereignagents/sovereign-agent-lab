"""
Exercise 2 — LangGraph Research Agent
======================================

WHAT YOU ARE DOING
-------------------
In this exercise you run the research agent you've started building in
sovereign_agent/agents/research_agent.py against the Edinburgh scenario.

The agent is already wired together (the LangGraph loop, the tools, the
LLM connection). Your job is to:

  Task A: Run it and observe the trace — which tools were called, in what order,
          and what decisions the model made between them.

  Task B: Implement generate_event_flyer in sovereign_agent/tools/venue_tools.py.
          The function stub is there with a TODO comment. Until you implement it,
          the tool returns an error. Once you implement it, Task B re-runs the
          main brief and generates a real flyer URL.

  Task C: Run three deliberate failure scenarios and observe how the agent handles
          each one. This is the most important part — how an agent handles the
          unexpected is what separates a prototype from something reliable.

  Task D: View the agent's internal graph structure and compare it to
          exercise3_rasa/data/rules.yml.

WHY THIS MATTERS FOR YOUR SOVEREIGN AGENT
------------------------------------------
research_agent.py is the core of your sovereign agent.
Every week you extend it — real web search in Week 2, planning in Week 3, memory
in Week 4. The trace structure you observe today (Think → Tool Call → Observe →
Repeat) is the same structure it will use when it's booking venues autonomously.

HOW TO RUN
-----------
    python week1/exercise2_langgraph.py             # all tasks
    python week1/exercise2_langgraph.py task_a      # main brief
    python week1/exercise2_langgraph.py task_b      # 4th tool demo
    python week1/exercise2_langgraph.py task_c      # failure modes
    python week1/exercise2_langgraph.py task_d      # graph structure

Results saved to week1/outputs/ex2_results.json.
Then fill in week1/answers/ex2_answers.py.
"""

import json
import sys
from pathlib import Path

from dotenv import load_dotenv

# ── Import from the persistent sovereign_agent project ────────────────────────
# This is the import pattern you'll use in Weeks 2-5 as well.
# The agent lives in sovereign_agent/ — the exercises just call it.
sys.path.insert(0, str(Path(__file__).parent.parent))

from sovereign_agent.agents.research_agent import run_research_agent

load_dotenv()

OUTPUTS_DIR = Path(__file__).parent / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)


# ─── Display helper ───────────────────────────────────────────────────────────

def print_result(result: dict, label: str) -> None:
    """Print a research_agent result dict in a readable format."""
    print(f"\n{'=' * 65}")
    print(f"  {label}")
    print(f"{'=' * 65}\n")

    for entry in result["full_trace"]:
        role = entry["role"].upper()
        if role == "TOOL_CALL":
            args_str = json.dumps(entry.get("args", {}))[:80]
            print(f"  [TOOL_CALL] → {entry['tool']}({args_str})")
        else:
            content = entry.get("content", "")
            if len(content) > 500:
                content = content[:500] + "..."
            if content:
                print(f"  [{role}]\n  {content}\n")


# ─── Task A — main Edinburgh brief ────────────────────────────────────────────
#
# The agent must:
#   1. Check at least two venues (The Albanach and The Haymarket Vaults)
#   2. Check the Edinburgh weather
#   3. Calculate catering cost for the confirmed venue
#   4. Attempt to generate a flyer (returns stub error until Task B is complete)
#
# Notice: we do NOT tell the agent in which order to do these things.
# The order emerges from the model's reasoning about what information it needs.
# That is what makes it an agent rather than a script.

def task_a() -> dict:
    print("\n--- Task A: Main Edinburgh Brief ---")
    result = run_research_agent(
        task=(
            "Rod needs a pub tonight for 160 people with vegan options and a quiet "
            "corner for a 30-minute webinar segment. "
            "Check The Albanach and The Haymarket Vaults. "
            "If one works, calculate catering at £35 per head. "
            "Also check Edinburgh weather for outdoor drinks suitability. "
            "Finally, generate a promotional flyer for the confirmed venue "
            "with the theme 'AI Meetup, Edinburgh, professional'."
        ),
        max_turns=10,
    )
    print_result(result, "TASK A — Main Edinburgh Brief")

    if not result["tool_calls_made"]:
        print("  ⚠️  No tool calls were made. Check that sovereign_agent/ is importable.")
    else:
        print(f"\n  Summary: {len(result['tool_calls_made'])} tool call(s) made")
        for tc in result["tool_calls_made"]:
            print(f"    - {tc['tool']}")

    print("\n→ Record results in week1/answers/ex2_answers.py")
    return result


# ─── Task B — 4th tool implementation ─────────────────────────────────────────
#
# Until you implement generate_event_flyer in sovereign_agent/tools/venue_tools.py,
# this task will show an error in the tool result.
# Once implemented, it should return a real image URL.
#
# TO IMPLEMENT:
#   Open sovereign_agent/tools/venue_tools.py
#   Find the generate_event_flyer function
#   Follow the TODO comment — replace the stub with a real images.generate() call

def task_b() -> dict:
    print("\n--- Task B: Flyer Tool ---")
    print("  If generate_event_flyer is still a stub, you'll see 'STUB' in the output.")
    print("  Implement the TODO in sovereign_agent/tools/venue_tools.py first.\n")

    result = run_research_agent(
        task=(
            "The Haymarket Vaults is confirmed for 160 guests tonight. "
            "Generate a promotional flyer with the theme "
            "'Edinburgh AI Meetup, tech professionals, modern venue'."
        ),
        max_turns=4,
    )
    print_result(result, "TASK B — Flyer Tool")
    return result


# ─── Task C — three failure scenarios ─────────────────────────────────────────
#
# READ THE OUTPUT CAREFULLY for each scenario.
# An agent that handles failure gracefully is production-ready.
# One that crashes or makes things up is not.
#
# Scenario 1: First choice unavailable
#   The Bow Bar has status=full in VENUES. The agent should notice this
#   in the tool result and pivot to another venue without being told to.
#   Question: At which message did the pivot happen?
#
# Scenario 2: Impossible constraint
#   No venue in VENUES fits 300 people. The agent should admit this,
#   NOT make up a fictional venue.
#   Question: Did it hallucinate a venue name?
#
# Scenario 3: Completely out of scope
#   There is no tool for train times. The agent should handle this cleanly.
#   Question: Did it try to call a tool anyway? Did it make something up?

def task_c() -> list:
    results = []

    print("\n--- Task C / Scenario 1: First Choice Unavailable ---")
    r1 = run_research_agent(
        task=(
            "Check The Bow Bar first for 160 vegan guests tonight. "
            "If it doesn't meet the requirements, check any other available venue."
        ),
        max_turns=8,
    )
    print_result(r1, "TASK C / Scenario 1 — First Choice Unavailable")
    results.append(r1)

    print("\n--- Task C / Scenario 2: Impossible Constraint ---")
    r2 = run_research_agent(
        task="Find a venue from our known venues for 300 people with vegan options.",
        max_turns=8,
    )
    print_result(r2, "TASK C / Scenario 2 — Impossible Constraint (300 guests)")
    results.append(r2)

    print("\n--- Task C / Scenario 3: Out of Scope ---")
    r3 = run_research_agent(
        task="What time does the last train leave Edinburgh Waverley for London tonight?",
        max_turns=4,
    )
    print_result(r3, "TASK C / Scenario 3 — Out of Scope")
    results.append(r3)

    print("\n→ Answer the Scenario questions in week1/answers/ex2_answers.py")
    return results


# ─── Task D — graph structure ─────────────────────────────────────────────────
#
# LangGraph exports a visual representation of the agent's internal structure.
# The output is Mermaid markdown — paste it into https://mermaid.live
#
# THEN: open exercise3_rasa/data/rules.yml in your editor.
# Compare what you see there with the Mermaid graph.
# They both describe "what the agent can do" — but very differently.

def task_d() -> str:
    from langchain_openai import ChatOpenAI
    from langgraph.prebuilt import create_react_agent
    from sovereign_agent.tools.venue_tools import (
        check_pub_availability, get_edinburgh_weather,
        calculate_catering_cost, generate_event_flyer,
    )
    import os

    llm = ChatOpenAI(
        base_url="https://api.tokenfactory.nebius.com/v1/",
        api_key=os.getenv("NEBIUS_KEY"),
        model="meta-llama/Llama-3.3-70B-Instruct",
        temperature=0,
    )
    agent = create_react_agent(llm, [
        check_pub_availability, get_edinburgh_weather,
        calculate_catering_cost, generate_event_flyer,
    ])

    print(f"\n{'=' * 65}")
    print("  TASK D — Agent Graph Structure (Mermaid)")
    print("=" * 65)
    print("  Paste the output below into https://mermaid.live\n")
    mermaid = agent.get_graph().draw_mermaid()
    print(mermaid)
    print()
    print("  Now open exercise3_rasa/data/flows.yml")
    print("  Both files describe the agent's behaviour — compare them.")
    print()
    print("  LangGraph: one loop node, model decides the path at runtime")
    print("  Rasa CALM: flows.yml — every task described explicitly, LLM picks the flow")
    print("  Record your comparison in week1/answers/ex2_answers.py → TASK_D_COMPARISON")
    return mermaid


# ─── Main ─────────────────────────────────────────────────────────────────────

def main(which: str = "all") -> None:
    output = {}

    if which in ("all", "task_a"):
        output["task_a"] = task_a()

    if which in ("all", "task_b"):
        output["task_b"] = task_b()

    if which in ("all", "task_c"):
        results = task_c()
        output["task_c"] = results

    if which in ("all", "task_d"):
        output["task_d_mermaid"] = task_d()

    out_path = OUTPUTS_DIR / "ex2_results.json"
    out_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\n✅  Results saved to {out_path}")
    print("    Fill in week1/answers/ex2_answers.py")


if __name__ == "__main__":
    valid = {"all", "task_a", "task_b", "task_c", "task_d"}
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which not in valid:
        print(f"Unknown task '{which}'. Options: {sorted(valid)}")
        sys.exit(1)
    main(which)
