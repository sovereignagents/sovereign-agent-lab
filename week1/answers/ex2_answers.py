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
TASK_A_CATERING_COST_GBP = 0.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = True

TASK_A_NOTES = "Default model meta-llama/Llama-3.3-70B-Instruct was attempting to make all 5 tools calls in one go and therefore failing to do this. I had to swithc to Qwen/Qwen3.5-397B-A17B-fast so it handled it correctly"  # optional — anything unexpected

# ── Task B ─────────────────────────────────────────────────────────────────

# Has generate_event_flyer been implemented (not just the stub)?
TASK_B_IMPLEMENTED = True  # True or False

# The image URL returned (or the error message if still a stub).
TASK_B_IMAGE_URL_OR_ERROR = "https://pictures-storage.storage.eu-north1.nebius.cloud/text2img-b60f1cb4-f74c-41f2-8939-860dceaebc25_00001_.webp"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = "Professional event flyer for Edinburgh AI Meetup, tech professionals, modern venue at The Haymarket Vaults, Edinburgh. 160 guests tonight. Warm lighting, Scottish architecture background, clean modern typography."

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
The agent checked The Bow Bar and got meets_all_constraints: false (capacity 80, status full). 
It then automatically checked The Haymarket Vaults, The Guilford Arms, and The Albanach 
without being told which venues to try, finding two that met all constraints.
"""

SCENARIO_1_FALLBACK_VENUE = "The Albanach"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False  # True or False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """
  None of the known venues meet the capacity and dietary requirements. The Albanach, The Haymarket Vaults, and The Guilford Arms have a capacity of 180, 160, and 200 respectively, which is less than the required capacity of 300. The Bow Bar has a capacity of 80, which is also less than the required capacity, and it is currently full. Therefore, none of the known venues can accommodate 300 people with vegan options.
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False  # True or False

SCENARIO_3_RESPONSE = "Your input is lacking necessary details. Please provide more information or specify the task you need help with."

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
This is not ideal for a real booking assistant. The agent gave a vague response 
asking for more details instead of clearly stating that train timetables are outside 
its capabilities. A user could waste time rephrasing the question thinking the agent 
can help. A better response would explicitly say it only handles venue bookings 
and suggest checking National Rail or Trainline for train times.
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
The LangGraph graph is a single loop: start → agent → tools → agent → end. The model 
decides at every step which tool to call and when to stop — there are no predefined paths. 
In contrast, Rasa CALM's flows.yml explicitly defines two flows: confirm_booking 
(collect guest_count, then vegan_count, then deposit, then run action_validate_booking) 
and handle_out_of_scope. Every step is written out in advance. The LLM only decides 
which flow to enter — after that, execution follows the defined steps deterministically.
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
The most surprising discovery was that the default Llama 3.3 70B model completely 
failed on Task A's complex multi-step prompt. Instead of executing tools through 
the ReAct loop, it dumped all five intended tool calls as a raw JSON text string 
in a single message — the tools were never actually invoked. However, when I 
switched to Qwen 3.5 397B, the same prompt worked correctly with proper tool 
calling. This revealed that the agent's reliability depends not just on the code 
or the prompt, but on how well the specific model supports structured tool-calling 
via the API. The same LangGraph agent with the same tools and the same prompt 
produced completely different behaviour depending on the model — one reasoned 
step-by-step through the ReAct loop, the other tried to shortcut by listing all 
calls at once. This is a critical consideration for production agents: the model 
choice is an architectural decision, not just a performance one.
"""
