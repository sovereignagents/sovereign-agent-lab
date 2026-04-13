"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ['search_venues', 'get_venue_details']

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = "Unfortunately, the search results did not find any venues that can accommodate 300 people and offer vegan options."

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True   # True or False

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
I changed The Albanach's status from available to full in mcp_venue_server.py and ran the MCP client again. Before the edit, Query 1 returned both The Albanach and The Haymarket Vaults, and after the edit only The Haymarket Vaults remained. Query 2 did not change. I did not need to update any agent logic, because I only changed the shared MCP server data, which is the main architectural benefit.
"""


# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 283   # count in exercise2_langgraph.py
LINES_OF_TOOL_CODE_EX4 = 265   # count in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP is useful not just because the tools live in a separate file, but because they become a shared service other agents can connect to. The main advantage is that I can change the tool server in one place and the client behaviour updates without rewriting the agent code.
"""

# ── Week 5 architecture ────────────────────────────────────────────────────
# Describe your full sovereign agent at Week 5 scale.
# At least 5 bullet points. Each bullet must be a complete sentence
# naming a component and explaining why that component does that job.

WEEK_5_ARCHITECTURE = """
- A LangGraph research agent should handle open-ended investigation because it can decide which tools to call and adapt its reasoning at runtime.
- A Rasa CALM confirmation agent should handle the manager call because it follows explicit flows and keeps the conversation inside strict business constraints.
- A shared MCP server should provide the venue tools so both agents can use the same source of truth instead of duplicating tool logic.
- A planner component should decide when the system needs research work and when it needs a controlled confirmation flow.
- A memory and logging component should store past context, decisions, and traces so the full agent becomes more reliable over time.
"""


# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
The research should be handled by the LangGraph agent, because in Exercises 2 and 4 it could search, compare results, use tools, and work through uncertainty step by step. The manager call should be handled by the Rasa CALM agent, because in Exercise 3 it stayed inside a controlled flow, collected the required fields, and escalated when constraints were violated. Swapping them feels wrong because the research task needs flexibility, while the call needs control. A free-form agent is too risky for a binding confirmation conversation, and a tightly scripted CALM flow would be too rigid for open-ended research.
"""

