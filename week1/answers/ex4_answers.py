"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", "get_venue_details"]

QUERY_1_VENUE_NAME    = "The Albanach"
QUERY_1_VENUE_ADDRESS = "2 Hunter Square, Edinburgh"
QUERY_2_FINAL_ANSWER  = "No venue in the known Edinburgh database can accommodate 300 guests with vegan options — the largest available vegan venue is The Albanach at 180 capacity."

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
Changed The Albanach's status from 'available' to 'full' in
mcp_venue_server.py. On rerun, search_venues(160, vegan=True) returned only
The Haymarket Vaults — The Albanach was automatically excluded by the filter.
The exercise4_mcp_client.py and research_agent.py required zero changes.
The agent discovered the updated results dynamically at runtime. Only the
server (the data layer) changed; the client and agent were completely unaffected.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 4   # explicit named imports of 4 tool functions
LINES_OF_TOOL_CODE_EX4 = 0   # client discovers tools dynamically, names 0 tools

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP decouples tool discovery from tool definition. A client never needs to
know the names or signatures of the tools in advance — it discovers them at
runtime. This means: add a new tool to the server and every client gets it
automatically. More importantly, multiple clients (LangGraph agent, Rasa
action server, future Week 2+ clients) can share exactly the same tool
implementation without duplicating code. A change in mcp_venue_server.py
propagates to all consumers simultaneously.
"""

# ── Week 5 architecture ────────────────────────────────────────────────────
# Describe your full sovereign agent at Week 5 scale.
# At least 5 bullet points. Each bullet must be a complete sentence
# naming a component and explaining why that component does that job.

WEEK_5_ARCHITECTURE = """
- The LangGraph Planner (DeepSeek R1) interprets Rod's instructions and decomposes them into a structured task plan, because reasoning and execution are separated for reliability.
- The LangGraph Executor (Llama 3.3 70B) carries out individual tool calls from the plan, calling real web search (Tavily) and file operations to gather and store venue data.
- The MCP Tool Server exposes all tools (venue search, web search, file ops) as a shared layer, so both LangGraph and Rasa consume the same implementations without duplication.
- The Rasa Pro CALM Agent handles all inbound structured interactions (manager confirmation calls), enforcing business rules deterministically in Python where no LLM improvisation is acceptable.
- A vector store (Pinecone) with CLAUDE.md memory persists cross-session context so the agent can recall prior decisions, previously visited venues, and Rod's preferences without re-researching from scratch.
- LangSmith observability traces every agent action, tool call, and LLM response, making it possible to audit decisions and diagnose failures in production.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
LangGraph handles the research; Rasa handles the confirmation call. Swapping
feels wrong because each agent's failure mode is exactly wrong for the other's
job.

In Ex2 Task A, the LangGraph agent returned its entire tool plan as a JSON
list in its response text rather than executing the tools — it improvised its
output format. That unpredictability is acceptable for research (you check the
result before acting), but catastrophic for a manager confirmation call where
every response has legal and financial weight.

In Ex3, Rasa CALM could not improvise at all — it responded to the parking
question with a fixed deflection and then resumed the booking flow. That rigid
determinism is useless for open-ended venue research where the agent must
decide which tools to call, in what order, and how to pivot when a venue is
full. A Rasa agent given Rod's WhatsApp message would have no flow to trigger.
The architecture is not symmetric — it is deliberate.
"""
