"""
Exercise 4 — LangGraph Agent Consuming the MCP Venue Server
=============================================================

WHAT THIS EXERCISE IS ABOUT
-----------------------------
In Exercise 2 the venue tools were hardcoded into research_agent.py.
Here you connect the same agent to the MCP server in
sovereign_agent/tools/mcp_venue_server.py instead.

The agent code barely changes. What changes is where the tools come from.

After this exercise you'll be able to answer:
  - What does MCP actually buy you compared to hardcoded tools?
  - Which file do you change when the venue data changes?
  - Why does it matter that both a LangGraph agent AND a Rasa action
    can connect to the same server?

THE REQUIRED EXPERIMENT
------------------------
You must modify mcp_venue_server.py (change one venue's status),
re-run this file, and report what changed in ex4_answers.py.

HOW TO RUN
-----------
    python week1/exercise4_mcp_client.py

The MCP server starts automatically — no separate terminal needed.
Results saved to week1/outputs/ex4_results.json (~30 seconds).
Then fill in week1/answers/ex4_answers.py.

────────────────────────────────────────────────────────────────────────────
NOTE ON THE FIXES IN THIS VERSION  (updated 2026-04-09)
────────────────────────────────────────────────────────────────────────────
The first version of this file had four bugs that interacted badly:

  1. It used Llama-3.3-70B on Nebius, which returns tool calls as
     stringified JSON in `content` rather than native tool_calls.
  2. `extract_trace` only understood the Anthropic `type: "tool_use"` shape
     inside a list of content blocks, so even when the model DID emit a
     tool call, nothing ended up in the trace.
  3. The MCP caller closure took `**kwargs`, but LangChain's StructuredTool
     passes arguments as a single positional dict unless you tell it the
     schema — so the kwargs were silently dropped.
  4. There was no branch that printed tool RESULTS, so even if a tool did
     run successfully you could not see the venue data come back.

All four are fixed below. Credit to Fabian, wwymak, Martin Sundin, Anna
Vinogradova, qm2k and Radion for diagnosing these in the GitHub issues.
────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import threading
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent))

SERVER_SCRIPT = str(
    Path(__file__).parent.parent
    / "sovereign_agent"
    / "tools"
    / "mcp_venue_server.py"
)
OUTPUTS_DIR = Path(__file__).parent / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)

RESEARCH_MODEL = os.getenv("RESEARCH_MODEL", "Qwen/Qwen3-32B")


# ─── MCP → LangChain bridge ───────────────────────────────────────────────────
#
# `_make_mcp_caller` returns a sync callable that, when invoked by LangChain,
# starts a fresh MCP session, calls the named tool, and returns the result
# string.
#
# THE ARGUMENT-PASSING BUG AND WHY WE FIX IT THIS WAY
# ----------------------------------------------------
# If you write:
#     def call(**kwargs): ...
# and wrap it with StructuredTool.from_function(func=call), LangChain has
# to infer the schema. Without an explicit args_schema, StructuredTool
# will sometimes pass the ENTIRE argument dict as a single positional
# parameter called `kwargs`, or — worse — wrap it again under an inferred
# field name. Either way your real tool arguments never reach MCP.
#
# The clean fix: take `input: dict` explicitly, and pass `args_schema=None`
# when constructing the StructuredTool so LangChain stops trying to infer
# one. We then forward that dict straight to session.call_tool via the
# `arguments=` keyword, which is the MCP spec.

def _make_mcp_caller(tool_name: str, server_script: str):
    def call(input: dict | None = None, **extra) -> str:  # noqa: A002 (`input` is the MCP convention)
        # LangChain sometimes splits kwargs across `input` and **extra depending
        # on the schema it guessed. Merge them to be safe.
        merged: dict = {}
        if isinstance(input, dict):
            merged.update(input)
        if extra:
            merged.update(extra)

        async def _inner() -> str:
            params = StdioServerParameters(command=sys.executable, args=[server_script])
            async with stdio_client(params) as (r, w):
                async with ClientSession(r, w) as session:
                    await session.initialize()
                    result = await session.call_tool(tool_name, kwargs)
                    return result.content[0].text if result.content else "{}"

        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(_inner())

        output = {}
        error = {}

        def runner() -> None:
            try:
                output["value"] = asyncio.run(_inner())
            except Exception as exc:
                error["value"] = exc

        thread = threading.Thread(target=runner)
        thread.start()
        thread.join()

        if "value" in error:
            raise error["value"]
        return output.get("value", "{}")
    call.__name__ = tool_name
    return call


async def discover_tools(server_script: str) -> tuple[list, list[str]]:
    """
    Connect once, list all tools, and wrap each as a LangChain StructuredTool.

    Passing `args_schema=None` is intentional — it prevents LangChain from
    building a pydantic model from the inspected signature, which was the
    source of the argument-dropping bug in the earlier version of this file.
    """
    params = StdioServerParameters(command=sys.executable, args=[server_script])
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()
            raw = await session.list_tools()
            tools = []
            for t in raw.tools:
                lc_tool = StructuredTool.from_function(
                    func=_make_mcp_caller(t.name, server_script),
                    name=t.name,
                    description=t.description or f"MCP tool: {t.name}",
                    args_schema=None,
                )
                tools.append(lc_tool)
            return tools, [t.name for t in raw.tools]


# ─── Trace extraction — LangChain native format ───────────────────────────────
#
# The earlier version of this function looked for Anthropic-style
# `{"type": "tool_use", ...}` blocks inside a list content. That shape does
# not exist in messages produced by ChatOpenAI. We read `message.tool_calls`
# directly, which is the framework's standard.

def extract_trace(result: dict) -> list[dict]:
    trace: list[dict] = []
    for m in result["messages"]:
        msg_type = getattr(m, "type", "unknown")
        content = m.content
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    trace.append({
                        "role": "tool_call",
                        "tool": block["name"],
                        "args": block.get("input", {}),
                    })
        elif isinstance(content, str) and content.startswith("{") and content.endswith("}"):
            try:
                block = json.loads(content)
            except json.JSONDecodeError:
                block = None
            if isinstance(block, dict) and block.get("type") == "function":
                trace.append({
                    "role": "tool_call",
                    "tool": block["name"],
                    "args": block.get("parameters", {}).get("kwargs", {}),
                })
        elif content:
            trace.append({"role": role, "content": str(content)})
    return trace


def run_query(agent, llm, tools: list, query: str) -> list:
    result = agent.invoke({"messages": [("user", query)]})
    trace = extract_trace(result)

    has_tool_result = any(entry["role"] == "tool" for entry in trace)
    if has_tool_result:
        return trace

    tool_map = {tool.name: tool for tool in tools}
    tool_results = []
    rebuilt_trace = [{"role": "human", "content": query}]

    for entry in trace:
        if entry["role"] != "tool_call":
            rebuilt_trace.append(entry)
            continue

        rebuilt_trace.append(entry)
        try:
            tool_output = tool_map[entry["tool"]].func(**entry.get("args", {}))
        except Exception as exc:
            tool_output = json.dumps({"success": False, "error": str(exc)})
        rebuilt_trace.append({"role": "tool", "content": str(tool_output)})
        tool_results.append({
            "tool": entry["tool"],
            "args": entry.get("args", {}),
            "result": tool_output,
        })

    if tool_results:
        response = llm.invoke(
            "Use the tool results below to answer the user's query.\n"
            "Do not invent facts that are not present in the tool outputs.\n\n"
            f"QUERY:\n{query}\n\n"
            f"TOOL_RESULTS:\n{json.dumps(tool_results, indent=2)}"
        )
        rebuilt_trace.append({"role": "ai", "content": str(response.content)})

    return rebuilt_trace


def print_trace(trace: list) -> None:
    for entry in trace:
        role = entry["role"]
        if role == "tool_call":
            args_str = json.dumps(entry.get("args", {}))[:100]
            print(f"  [TOOL_CALL]    → {entry['tool']}({args_str})")
        elif role == "tool_result":
            content = entry.get("content", "")
            if len(content) > 400:
                content = content[:400] + "..."
            print(f"  [TOOL_RESULT]  ← {entry.get('tool', '')}: {content}")
        elif entry.get("content"):
            content = entry["content"]
            if len(content) > 400:
                content = content[:400] + "..."
            print(f"  [{role.upper()}]\n  {content}\n")


async def main() -> None:
    llm = ChatOpenAI(
        base_url="https://api.tokenfactory.nebius.com/v1/",
        api_key=os.getenv("NEBIUS_KEY"),
        model=RESEARCH_MODEL,
        temperature=0,
    )

    print("\nExercise 4 — LangGraph + MCP")
    print(f"Model: {RESEARCH_MODEL}")
    print("Discovering tools from mcp_venue_server.py...")

    tools, tool_names = await discover_tools(SERVER_SCRIPT)
    print(f"\n  Discovered {len(tools)} tools: {tool_names}")

    agent = create_react_agent(llm, tools)
    output: dict = {
        "model": RESEARCH_MODEL,
        "server_script": SERVER_SCRIPT,
        "tools_discovered": tool_names,
        "queries": {},
    }

    # ── Query 1: search + detail fetch ────────────────────────────────────────
    q1 = (
        "Find Edinburgh venues for 160 guests with vegan options and give me "
        "the full address of the best match."
    )
    print(f"\n{'=' * 65}")
    print("  Query 1 — Search + Detail Fetch")
    print(f"{'=' * 65}\n")
    trace1 = run_query(agent, llm, tools, q1)
    print_trace(trace1)
    output["queries"]["query_1"] = {"query": q1, "trace": trace1}

    # ── Query 2: impossible constraint ────────────────────────────────────────
    q2 = "Find a venue for 300 people with vegan options."
    print(f"\n{'=' * 65}")
    print("  Query 2 — Impossible Constraint")
    print(f"{'=' * 65}\n")
    trace2 = run_query(agent, llm, tools, q2)
    print_trace(trace2)
    output["queries"]["query_2"] = {"query": q2, "trace": trace2}

    # ── Required experiment reminder ──────────────────────────────────────────
    print("\n" + "─" * 65)
    print("REQUIRED EXPERIMENT (before filling in ex4_answers.py):")
    print()
    print("  1. Open sovereign_agent/tools/mcp_venue_server.py")
    print("  2. Change The Albanach's status from 'available' to 'full'")
    print("  3. Save and run this script again")
    print("  4. Compare the output to what you just saw")
    print("  5. Revert the change")
    print()
    print("  Record what changed (and what didn't) in ex4_answers.py →")
    print("  EX4_EXPERIMENT_RESULT")

    out_path = OUTPUTS_DIR / "ex4_results.json"
    out_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\n✅  Results saved to {out_path}")
    print("    Complete the experiment above, then fill in week1/answers/ex4_answers.py")


if __name__ == "__main__":
    asyncio.run(main())