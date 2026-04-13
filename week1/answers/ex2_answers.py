"""
Exercise 2 — Answers
====================
Fill this in after running exercise2_langgraph.py.
Run `python grade.py ex2` to check for obvious issues.
"""

# ── Task A ─────────────────────────────────────────────────────────────────

# List of tool names called during Task A, in order of first appearance.
# Look at [TOOL_CALL] lines in your terminal output.
# Example: ["check_pub_availability", "get_edinburgh_weather"]

TASK_A_TOOLS_CALLED = [
    "check_pub_availability",
    "check_pub_availability",
    "calculate_catering_cost",
    "get_edinburgh_weather",
    "generate_event_flyer",
]

# Which venue did the agent confirm? Must be one of:
# "The Albanach", "The Haymarket Vaults", or "none"
TASK_A_CONFIRMED_VENUE = "none"

# Total catering cost the agent calculated. Float, e.g. 5600.0
# Write 0.0 if the agent didn't calculate it.
TASK_A_CATERING_COST_GBP = 0.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = True

TASK_A_NOTES = (
    "Task A exposed an interesting failure: the model returned all 5 intended "
    "tool calls as a JSON array inside its AI response text rather than "
    "executing them through the tool-calling mechanism. The tools listed above "
    "are what the model planned to call (visible in the trace), not what was "
    "actually executed. Tasks B and C worked correctly with real tool calls."
)

# ── Task B ─────────────────────────────────────────────────────────────────

# Has generate_event_flyer been implemented (not just the stub)?
TASK_B_IMPLEMENTED = True

# The image URL returned (or the error message if still a stub).
TASK_B_IMAGE_URL_OR_ERROR = "https://pictures-storage.storage.eu-north1.nebius.cloud/text2img-2cc214e3-827c-4441-9a2d-2088e79bdebc_00001_.webp"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = (
    "Professional event flyer for Edinburgh AI Meetup, tech professionals, "
    "modern venue at The Haymarket Vaults, Edinburgh. 160 guests tonight. "
    "Warm lighting, Scottish architecture background, clean modern typography."
)

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
After receiving the Bow Bar tool result showing status=full and
meets_all_constraints=false, the agent immediately called check_pub_availability
for The Haymarket Vaults, The Guilford Arms, and The Albanach in sequence —
pivoting without any human instruction to check all remaining known venues.
"""

SCENARIO_1_FALLBACK_VENUE = "The Haymarket Vaults"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """
None of the known venues meet the capacity and dietary requirements.
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False

SCENARIO_3_RESPONSE = "I am not able to execute this task as it exceeds the limitations of the functions I have been given."

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
Yes, this is acceptable. The agent correctly recognised it had no tool for
train times and refused rather than hallucinating an answer or misusing a
venue tool. In a production system you would want a cleaner user-facing
message, but the underlying behaviour — admitting scope limits rather than
making things up — is exactly right for a reliable booking assistant.
"""

# ── Task D ─────────────────────────────────────────────────────────────────

# Paste the Mermaid output from `python exercise2_langgraph.py task_d` here.
TASK_D_MERMAID_OUTPUT = """
---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	agent(agent)
	tools(tools)
	__end__([<p>__end__</p>]):::last
	__start__ --> agent;
	agent -.-> __end__;
	agent -.-> tools;
	tools --> agent;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
"""

# Compare the LangGraph graph to exercise3_rasa/data/rules.yml. Min 30 words.
TASK_D_COMPARISON = """
LangGraph has just three nodes — start, agent, tools — in an open loop. The
model decides at runtime which tools to call, in what order, and when to stop.
Rasa CALM's flows.yml explicitly names every step and every slot to collect;
the LLM picks which flow to enter but cannot deviate from the defined sequence
within it. LangGraph trades auditability for flexibility; Rasa trades
flexibility for predictability.
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
In Task A the agent returned all five intended tool calls as a JSON array
inside its AI response content text, rather than executing them through the
tool-calling mechanism. It planned correctly — the right tools in the right
order — but produced output that looked like executable instructions instead
of actually triggering them. Tasks B and C worked with real tool calls on
simpler, single-focus prompts, suggesting the failure was specific to the
complexity of the multi-step Task A prompt.
"""
