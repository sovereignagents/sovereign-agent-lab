"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", "get_venue_details"]

QUERY_1_VENUE_NAME = "The Albanach"
QUERY_1_VENUE_ADDRESS = "2 Hunter Square, Edinburgh"
QUERY_2_FINAL_ANSWER = """  
I searched for venues in Edinburgh that can accommodate at least 300 people and offer vegan options, but unfortunately, no venues currently match these criteria. 

You might want to consider:
- Reducing the minimum capacity requirement
- Looking for venues without the vegan requirement and checking if they can accommodate vegan needs separately
- Expanding your search to include venues slightly ou..
"""

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True  # True or False

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
I changed only one file: sovereign_agent/tools/mcp_venue_server.py — I set 
The Albanach's status from 'available' to 'full'. Before the change, the agent 
found two matching venues and recommended The Albanach as the best match. After 
the change, it correctly returned only The Haymarket Vaults. Crucially, I did 
not need to change exercise4_mcp_client.py, research_agent.py, or any other 
file. The client discovered the same tools and used the same code — only the 
data in the server changed, and the results updated automatically.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 4  # count in exercise2_langgraph.py
LINES_OF_TOOL_CODE_EX4 = 0  # count in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP provides dynamic tool discovery — the client connects, asks what tools are 
available, and wraps them automatically. When you add a new tool to the MCP 
server, every client picks it up without any code changes. In Exercise 2, adding 
a tool meant importing it in research_agent.py and adding it to the TOOLS list. 
In Exercise 4, you just add a @mcp.tool() function to the server and every 
connected agent sees it immediately. This also means multiple agents — LangGraph 
and Rasa — can share the same tools from one server, ensuring consistent data 
and behaviour across both.
"""

# ── Week 5 architecture ────────────────────────────────────────────────────
# Describe your full sovereign agent at Week 5 scale.
# At least 5 bullet points. Each bullet must be a complete sentence
# naming a component and explaining why that component does that job.

WEEK_5_ARCHITECTURE = """
- The LangGraph research agent handles open-ended venue research because it can reason through unknowns, pivot when a venue is full, and decide its own sequence of tool calls autonomously.
- The Rasa CALM digital employee handles structured confirmation calls because every step is auditable, deterministic, and constrained by Python business rules that the LLM cannot override.
- The MCP venue server provides shared tools to both agents so that venue data, search logic, and availability are consistent regardless of which agent accesses them.
- A vector store and CLAUDE.md memory layer gives the research agent context from past sessions so it can learn preferences and avoid repeating failed venue checks.
- An observability layer with LangSmith tracing monitors both agents in production, tracking token costs, tool call latency, and failure rates to ensure reliability.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
The LangGraph agent handles the research because it needs to reason autonomously — 
in Exercise 2, it checked The Bow Bar, found it was full, and pivoted to checking 
three other venues without being told which ones to try. That kind of initiative 
is essential for open-ended exploration. The Rasa CALM agent handles the 
confirmation call because it must follow a strict sequence — collect guest count, 
vegan count, deposit — and enforce hard limits in Python. When I entered a £500 
deposit, the Python guard caught it and escalated with a clear reason. The LLM 
never got to negotiate. Rasa CALM cannot improvise — 
it cannot decide to check the weather or generate a flyer because those flows 
don't exist in flows.yml. For research, that rigidity would be crippling.
"""
