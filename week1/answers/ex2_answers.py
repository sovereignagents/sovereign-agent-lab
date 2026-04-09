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
TASK_A_CONFIRMED_VENUE = "The Albanach"

# Total catering cost the agent calculated. Float, e.g. 5600.0
# Write 0.0 if the agent didn't calculate it.
TASK_A_CATERING_COST_GBP = 5600.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = False

TASK_A_NOTES = (
    "The agent produced tool calls as text content rather than structured tool_call objects, "
    "which is a known behavior with Llama models on the Nebius OpenAI-compatible endpoint. "
    "Both The Albanach and The Haymarket Vaults met all constraints; the agent chose The Albanach."
)

# ── Task B ─────────────────────────────────────────────────────────────────

# Has generate_event_flyer been implemented (not just the stub)?
TASK_B_IMPLEMENTED = True

# The image URL returned (or the error message if still a stub).
TASK_B_IMAGE_URL_OR_ERROR = "https://pictures-storage.storage.eu-north1.nebius.cloud/text2img-0bba0044-d869-4946-bef7-6ffa370f1db1_00001_.webp"

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
The agent checked The Bow Bar first and found it did not meet constraints (capacity 80, status full).
It then pivoted to checking The Haymarket Vaults and The Albanach without being prompted. It chose
The Albanach as the fallback because it had the higher capacity (180 vs 160). The agent also
calculated catering cost at 160 guests times 20 pounds per head equalling 3200 pounds, and checked
the weather (8 degrees Celsius, Overcast, outdoor_ok false).
"""

SCENARIO_1_FALLBACK_VENUE = "The Albanach"

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

SCENARIO_3_RESPONSE = "Your input is lacking necessary details. Please provide more information or specify the task you need help with."

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
This behavior is partially acceptable. The agent correctly avoided calling irrelevant tools and did
not hallucinate train times, which is good. However, the response is unhelpful and vague — it says
the input is "lacking necessary details" when in reality the request is simply outside the agent's
domain. A production assistant should clearly state that train schedule queries are outside its
capabilities and suggest the user check National Rail or another appropriate resource, rather than
implying the user's question was malformed.
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
The LangGraph graph is a simple cycle: start goes to agent, agent can go to tools or end, and tools
always returns to agent. The model decides at runtime whether to call a tool or finish — there are no
explicit rules about which tool to call when. In contrast, Rasa CALM flows.yml defines each task
explicitly with named steps, slot collection sequences, and specific actions. LangGraph is one
generic loop where the LLM has full autonomy; Rasa CALM constrains the LLM to predefined flows
and only lets it pick which flow matches the user's intent. LangGraph is more flexible but less
predictable; Rasa is more rigid but guarantees the conversation follows a known path.
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
The most unexpected behavior was in Scenario 1, where the agent not only pivoted from The Bow Bar
after finding it was full and too small, but proactively checked both remaining viable venues and
chose The Albanach specifically because of its higher capacity margin (180 vs 160 for 160 guests).
It also independently calculated catering cost and checked weather without further prompting. This
emergent multi-step recovery — checking alternatives, comparing them, and selecting the better
option — was not explicitly coded anywhere. The LLM reasoned about backup strategies on its own,
demonstrating the power and the risk of agentic loops: the agent did the right thing here, but
the same autonomy could lead to unwanted decisions in other scenarios.
"""
