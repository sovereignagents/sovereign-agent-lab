"""
sovereign_agent/agents/research_agent.py
=========================================
The Research Agent for your Sovereign Agent project.

This is the file that grows each week:

  Week 1 (now):    Basic ReAct loop with 4 venue tools
  Week 2:          Add real web search and file operation tools
  Week 3:          Split into Planner (DeepSeek R1) + Executor (Llama 70B)
  Week 4:          Add CLAUDE.md memory so the agent remembers past sessions
  Week 5:          Add observability, cost tracking, and safety guardrails

The public interface — run_research_agent(task, max_turns) → dict — stays the
same across all weeks. Week 2's code imports and calls this function exactly
as Week 1 leaves it. You add capability inside; the callers don't change.

HOW TO USE
----------
Import and call from exercise files:

    from sovereign_agent.agents.research_agent import run_research_agent

    result = run_research_agent(
        task="Find a pub for 160 vegan guests tonight.",
        max_turns=8,
    )
    print(result["final_answer"])
    print(result["tool_calls_made"])

ADDING TOOLS IN FUTURE WEEKS
-----------------------------
To add a new tool, import it and add it to the TOOLS list below.
The agent picks up the new capability automatically — no other changes needed.

    # Week 2 example:
    from sovereign_agent.tools.web_search import search_web
    TOOLS = [
        check_pub_availability,
        get_edinburgh_weather,
        calculate_catering_cost,
        generate_event_flyer,
        search_web,           # ← just add here
    ]
"""

import json
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# Import tools from the shared tool layer
# This import path is why the project structure matters —
# sovereign_agent/ is a Python package that can be imported from anywhere
from sovereign_agent.tools.venue_tools import (
    check_pub_availability,
    get_edinburgh_weather,
    calculate_catering_cost,
    generate_event_flyer,
)

load_dotenv()

# ─── Model ────────────────────────────────────────────────────────────────────
# Week 1: single model handles everything
# Week 3: this gets split into llm_planner (DeepSeek R1) and llm_executor (Llama 70B)

llm = ChatOpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.getenv("NEBIUS_KEY"),
    model="meta-llama/Llama-3.3-70B-Instruct",
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
# Rebuilding it on every call would be wasteful.
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
          success:         bool — True if agent gave a final answer (not max_turns)

    This return shape is the contract that Week 2+ code will depend on.
    Do not change the key names.
    """
    result = _agent.invoke(
        {"messages": [("user", task)]},
        config={"recursion_limit": max_turns * 2},  # LangGraph uses steps, not turns
    )

    tool_calls_made = []
    full_trace      = []
    final_answer    = ""
    saw_tool_result = False

    for m in result["messages"]:
        role    = getattr(m, "type", "unknown")
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
        "final_answer":    final_answer,
        "tool_calls_made": tool_calls_made,
        "full_trace":      full_trace,
        "success":         bool(final_answer),
    }
