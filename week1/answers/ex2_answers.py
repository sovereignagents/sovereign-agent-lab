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
    "- check_pub_availability",
    "- check_pub_availability,",
    "get_edinburgh_weather,",
    " calculate_catering_cost,",
    " generate_event_flyer,"
 ]

# Which venue did the agent confirm? Must be one of:
# "The Albanach", "The Haymarket Vaults", or "none"
TASK_A_CONFIRMED_VENUE = "The Albanach"

# Total catering cost the agent calculated. Float, e.g. 5600.0
# Write 0.0 if the agent didn't calculate it.
TASK_A_CATERING_COST_GBP = 0.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = False

TASK_A_NOTES = ""   # optional — anything unexpected

# ── Task B ─────────────────────────────────────────────────────────────────

# Has generate_event_flyer been implemented (not just the stub)?
TASK_B_IMPLEMENTED = True   # True or False

# The image URL returned (or the error message if still a stub).
TASK_B_IMAGE_URL_OR_ERROR = "https://pictures-storage.storage.eu-north1.nebius.cloud/text2img-26c5f7cf-152e-4eed-b312-7aacf5394782_00001_.webp"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = "The Haymarket Vaults is confirmed for 160 guests tonight. Generate a promotional flyer with the theme 'Edinburgh AI Meetup, tech professionals, modern venue"

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
  - Meets all constraints: false (because capacity is insufficient)

Since The Bow Bar does not meet the capacity requirement, we must check other available venues.

"""

SCENARIO_1_FALLBACK_VENUE = "We have found a suitable venue: The Albanach, which meets the capacity (180) " \
                            "and vegan requirements."

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False  # True or False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """I've checked all known venues, and unfortunately,
 none meet your requirements for 300 people with vegan options

"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = True  # True or False

SCENARIO_3_RESPONSE = """I don't have access to real-time train schedules or transportation data through my available tools. My capabilities are limited to:

1. Checking Edinburgh pub availability
2. Getting Edinburgh weather
3. Calculating catering costs
4. Generating event flyers

For train schedules, I recommend checking:
- National Rail Enquiries website
- Trainline app
- ScotRail website
- Edinburgh Waverley station information screens"""

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
The agent recognises that the tool has not be called but on the output 'success' it has been registered as True, which is confusing\
Ideally we should have another function called 'tool checking' or another agent that checks all tools have been orcehstrated properly\
and thatall tools are called effectively ( output is not  [] etc)
"""

# ── Task D ─────────────────────────────────────────────────────────────────

# Paste the Mermaid output from `python exercise2_langgraph.py task_d` here.
TASK_D_MERMAID_OUTPUT = """
https://mermaid.ai/app/projects/27efa380-74c6-4c0d-8510-009851e7509e/diagrams/c2cce852-98eb-4880-a51e-32f5beb96707/version/v0.1/edit
"""

# Compare the LangGraph graph to exercise3_rasa/data/rules.yml. Min 30 words.
TASK_D_COMPARISON = """
  LangGraph: Utilises a one loop node, model decides the path at runtime
  Rasa CALM: flows.yml — every task described explicitly, LLM picks the flow and operates within it\
  with no deviation. So it cannot handle edge cases or out of scope questions effectively.
  But RASA is more predictable and consistent
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
In task B  the agent went into a spiral about the weather. It identified the correct pub according to the contraints we have given it\
However for the weather tool becuse there are not explicit instruction how to decide the best weather conditions, the agent\
kep questioning itself. There was a chain of thought around whether this weather conditions are suitable for outdoor\
( althgou we did not have a constraint around the venue being outdoors. So because the agent has the independenct of which tool to call first\
and emphasis given, this resulted in an unnecessary complicated thinking.
Also the flyer that was generated was kind of dreadful, full of grammatic mistakes. Probably this is  because the deepseek model is not best suitable for image generation

"""
