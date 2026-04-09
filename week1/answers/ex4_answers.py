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
QUERY_2_FINAL_ANSWER  = "No venue in the known database meets the requirements for 300 guests with vegan options."

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
Changed The Albanach's status from "available" to "full" in mcp_venue_server.py. After re-running
exercise4_mcp_client.py, The Albanach no longer appeared in search_venues results for available
venues matching 160 guests with vegan options — only The Haymarket Vaults was returned as a match.
Crucially, only one file needed modification: mcp_venue_server.py. The client code in
exercise4_mcp_client.py was not touched at all. The agent automatically adapted to the new data
because it discovers tools and their results dynamically at runtime. This demonstrates MCP's core
value: data changes propagate through a single file without requiring any client-side updates.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 0   # count in exercise2_langgraph.py
LINES_OF_TOOL_CODE_EX4 = 0   # count in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP provides dynamic tool discovery at runtime via a standard protocol, not just code separation.
When you add a new @mcp.tool() to the server, every connected client — whether LangGraph, Rasa,
or any other MCP-compatible agent — picks it up automatically without code changes. This is
fundamentally different from importing functions: with imports, every client must update its import
list and redeploy. With MCP, the server is the single source of truth for what tools exist and
what data they return. Multiple heterogeneous agents can share the same tool server, ensuring
consistent behavior. The stdio transport means the server starts on demand — no separate process
management. In Week 2, adding real web search tools to the MCP server will make them available
to all clients simultaneously.
"""

# ── Week 5 architecture ────────────────────────────────────────────────────
# Describe your full sovereign agent at Week 5 scale.
# At least 5 bullet points. Each bullet must be a complete sentence
# naming a component and explaining why that component does that job.

WEEK_5_ARCHITECTURE = """
- The MCP venue server acts as the shared tool layer, exposing venue search, availability checks, and booking operations to all agent clients through a standard protocol, ensuring consistent data across the system.
- The LangGraph research agent handles open-ended venue research and comparison tasks, because its flexible loop structure allows the LLM to reason freely about which tools to call and in what order when exploring options.
- The Rasa CALM confirmation agent handles the actual booking confirmation phone calls, because its constrained flow architecture guarantees that all required information is collected and all business rules are enforced before any commitment is made.
- A persistent memory store (vector database or structured state) maintains context across conversations and sessions, so the agent remembers previous research findings, venue preferences, and past booking outcomes without re-discovering them each time.
- A planning module decomposes complex multi-step tasks (like organizing a full event) into subtasks assigned to the appropriate agent — research goes to LangGraph, confirmations go to Rasa — because each agent type excels at different aspects of the workflow.
- A human-in-the-loop escalation gateway routes decisions that exceed predefined thresholds (deposit limits, capacity overrides, unusual requirements) to a human operator, because deterministic Python guards can detect but not resolve edge cases that require judgment.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
LangGraph is the right agent for research, and Rasa CALM is the right agent for the confirmation
call. This became clear from the exercises. In Exercise 2, the LangGraph agent demonstrated
creative multi-step reasoning: when The Bow Bar was full in Scenario 1, it autonomously checked
two alternatives, compared their capacities, and selected the better one. That emergent behavior
is exactly what you want when exploring options. But that same autonomy is dangerous for the
confirmation call — in Scenario 3, the agent gave a vague non-answer instead of staying on task.

Rasa CALM is the opposite: it cannot improvise or explore, but it guarantees the conversation
follows the defined flow. It will always collect guest count, vegan count, and deposit before
running ActionValidateBooking. The Python guards (MAX_DEPOSIT_GBP, MAX_GUESTS, the 16:45 cutoff)
execute deterministically — the LLM cannot talk its way around them. Swapping feels wrong because
putting CALM on research would mean predefining every possible search path in flows.yml, destroying
the flexibility that makes research useful. And putting LangGraph on the confirmation call would
mean trusting the LLM to enforce financial constraints it could rationalize away. The research
agent needs freedom to think; the confirmation agent needs guardrails to prevent thinking.
"""
