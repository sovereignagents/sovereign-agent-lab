"""
sovereign_agent/agents/research_agent.py
=========================================
The Research Agent for your Sovereign Agent project.

This is the file that grows across the module:

  Week 1 (now):      Basic ReAct loop with 4 venue tools
  Week 2 session:    Add real web search and file operation tools
                     (feeds into the final assignment — no separate homework)
  Final assignment:  Becomes the executor inside PyNanoClaw. A planner
                     runs upstream, memory runs alongside, a handoff bridge
                     routes human-conversation tasks to the Rasa half.
                     Observability, cost tracking, and safety guardrails land.

The public interface — run_research_agent(task, max_turns) → dict — stays the
same throughout. Later code imports and calls this function exactly as Week 1
leaves it. You add capability inside; the callers don't change.

────────────────────────────────────────────────────────────────────────────
NOTE ON THE MODEL CHOICE  (updated 2026-04-09)
────────────────────────────────────────────────────────────────────────────
The first version of this file used meta-llama/Llama-3.3-70B-Instruct. That
model is excellent at reasoning but, on the Nebius Token Factory endpoint,
it does not reliably emit native `tool_calls` objects — it tends to emit the
tool call as a stringified JSON blob inside `content`, which LangGraph's
ReAct loop cannot consume directly. You would see traces like this:

    [AI] "{\"type\": \"function\", \"name\": \"check_pub_availability\", ...}"
    ⚠️  No tool calls were made.

We have switched to `Qwen/Qwen3-32B`, which natively supports the OpenAI
tool-calling spec on Nebius and works out of the box with `create_react_agent`.

We have also made the result parser below robust to BOTH formats, so if you
experiment with a different model and it emits the older stringified-JSON
shape, your trace will still be captured correctly instead of coming back
empty. That defensive parsing is how the Week-2/3/4 code will stay stable
as you try different models.
────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import json
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from sovereign_agent.tools.venue_tools import (
    calculate_catering_cost,
    check_pub_availability,
    generate_event_flyer,
    get_edinburgh_weather,
)

load_dotenv()

# ─── Model ────────────────────────────────────────────────────────────────────
# Qwen3-32B on Nebius natively supports tool_calls. If you want to try another
# model, good alternatives that also emit correct tool_calls on Nebius and
# survived the 2026-04-13 deprecation round are:
#   - nvidia/nemotron-3-super-120b-a12b
#   - Qwen/Qwen3-Next-80B-A3B-Thinking
#
# Avoid:
#   - meta-llama/Llama-3.3-70B-Instruct for anything that needs tools on
#     this provider — see note at the top of the file.
#   - deepseek-ai/DeepSeek-R1-0528 — deprecated 2026-04-13, no longer served.
#   - Any model suffixed `_fast` in the Qwen, Llama, or DeepSeek families —
#     also deprecated 2026-04-13. See CHANGELOG.md §Fixed for the full list.

RESEARCH_MODEL = os.getenv("RESEARCH_MODEL", "Qwen/Qwen3-32B")

llm = ChatOpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.getenv("NEBIUS_KEY"),
    model=RESEARCH_MODEL,
    temperature=0,
)

# ─── Tool registry ────────────────────────────────────────────────────────────
# Week 1: 4 venue tools
# Week 2: add search_web, read_file, write_file here

TOOLS = [
    check_pub_availability,
    get_edinburgh_weather,
    calculate_catering_cost,
    generate_event_flyer,
]

# Build the agent once at module load time.
_agent = create_react_agent(llm, TOOLS)
_tool_map = {tool.name: tool for tool in TOOLS}


def _run_tool(tool_name: str, args: dict) -> str:
    tool = _tool_map[tool_name]
    return tool.invoke(args)


def _synthesize_final_answer(task: str, tool_results: list[dict]) -> str:
    prompt = (
        "You are the final response stage of a research agent.\n"
        "Use the tool outputs below to answer the user's task.\n"
        "Do not invent facts beyond the tool results.\n"
        "If the task cannot be completed with the available tools, say so clearly.\n\n"
        f"TASK:\n{task}\n\n"
        f"TOOL_RESULTS:\n{json.dumps(tool_results, indent=2)}"
    )
    response = llm.invoke(prompt)
    return str(getattr(response, "content", "")).strip()


# ─── Public interface ─────────────────────────────────────────────────────────

def run_research_agent(task: str, max_turns: int = 8) -> dict:
    """
    Run the research agent on a task and return a structured result.

    Args:
        task:      Natural language task description
        max_turns: Maximum number of reasoning turns before giving up

    Returns:
        dict with keys:
          final_answer:    str — the agent's final response
          tool_calls_made: list of dicts — each tool call with name and args
          full_trace:      list of dicts — every message in the conversation
          success:         bool — True if agent gave a final answer

    This return shape is the contract that Week 2+ code depends on.
    Do not change the key names.
    """
    result = _agent.invoke(
        {"messages": [("user", task)]},
        config={"recursion_limit": max_turns * 2},
    )

    tool_calls_made = []
    full_trace      = []
    final_answer    = ""
    saw_tool_result = False

    for m in result["messages"]:
        msg_type = getattr(m, "type", "unknown")
        content = m.content

        # Some models return tool calls as structured blocks, others as a JSON string.
        if isinstance(content, list) or (
            isinstance(content, str) and content.startswith("[") and content.endswith("]")
        ):
            if isinstance(content, str):
                content = [json.loads(block) for block in json.loads(content)]

            for block in content:
                if isinstance(block, dict) and block.get("type") in ["tool_use", "function"]:
                    entry = {
                        "tool": block["name"],
                        "args": block.get("input", block.get("parameters", {})),
                    }
                    tool_calls_made.append(entry)
                    full_trace.append({"role": "tool_call", **entry})
            continue

        if content:
            full_trace.append({"role": role, "content": str(content)})
            if role == "tool":
                saw_tool_result = True
            if role == "ai":
                final_answer = str(content)

    if tool_calls_made and not saw_tool_result:
        tool_results = []
        full_trace = [{"role": "human", "content": task}]

        for entry in tool_calls_made:
            full_trace.append({"role": "tool_call", **entry})
            try:
                tool_output = _run_tool(entry["tool"], entry["args"])
            except Exception as exc:
                tool_output = json.dumps({"success": False, "error": str(exc)})
            tool_results.append({
                "tool": entry["tool"],
                "args": entry["args"],
                "result": tool_output,
            })
            full_trace.append({"role": "tool", "content": str(tool_output)})

        final_answer = _synthesize_final_answer(task, tool_results)
        if final_answer:
            full_trace.append({"role": "ai", "content": final_answer})

    return {
        "final_answer": final_answer,
        "tool_calls_made": tool_calls_made,
        "full_trace": full_trace,
        "success": bool(final_answer),
    }