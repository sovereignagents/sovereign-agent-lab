"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = [    "search_venues",
    "get_venue_details"]

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = """I couldn't find any available venues in Edinburgh that meet both requirements:
- Minimum capacity of 300 people
- Vegan menu options available

Would you like me to try any of these alternatives?
1. Search for venues with a slightly lower capacity (e.g., 250+)
2. Search for venues that don't specifically require vegan options
3. Look for venues outside of Edinburgh
4"""

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True  # True or False

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
venue_server was the only one updated, where the VENUES dictionary was modified to set the status to full
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 143   # count in exercise2_langgraph.py
LINES_OF_TOOL_CODE_EX4 = 117   # count in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
The key insight : with hardcoded tools (Exercise 2), \
we have to update every agent separately. With MCP, you change the data in one place \
and all clients pick it up automatically. Also MCP offers better scalability\
 because makes the tools reusable and operable across different mdoels and environments \
 and enables usage across different agents simultaneously
"""

# ── Week 5 architecture ────────────────────────────────────────────────────
# Describe your full sovereign agent at Week 5 scale.
# At least 5 bullet points. Each bullet must be a complete sentence
# naming a component and explaining why that component does that job.

WEEK_5_ARCHITECTURE = """
- FILL ME IN
- FILL ME IN
- FILL ME IN
- FILL ME IN
- FILL ME IN
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
FILL ME IN
"""
