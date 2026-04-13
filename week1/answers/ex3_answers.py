"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Your input ->  calling to confirm a booking                                                                                                                                                                

How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                                                                  

And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan                                                                                                                                                                         

What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit                                                                                                                                                                                

Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
"""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  calling to confirm a booking                                                                                                                                                                

How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                                                                  

And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan                                                                                                                                                                         

What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £500 deposit                                                                                                                                                                                

I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £500 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?                          
"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "authorised limit for deposit"   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input ->  calling to confirm a booking

How many guests are you confirming for tonight's event?
Your input ->  160 guests

And how many of those guests will need vegan meals?
Your input ->  can you arrange parking for the speakers?

I'm sorry, I'm not trained to help with that.
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
Your input ->  yes

What deposit amount in GBP are you proposing to secure the booking?
Your input ->  What about vegan count?

What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit and around 50 of the guests will be vegan

I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
Your input ->  yes

Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
After the out-of-scope message agent used out-of-scope response and didn't try to ansert the question directly. Agent said that it could only help with confirming the booking and asked if I wanted to proceed with that.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
Rasa CALM handled this out-of-scope request in a more controlled way: it clearly stated what its scope is and that the question is out of scope. LangGraph agent's answer was less explicit in this way, he only mentioned that the request need to be specified or that it lacks information to complete it.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
I uncommented the cutoff guard in actions.py, retrained the Rasa model, restarted action server and ran the first (happy path) conversation again. In the end, instead of confirming the booking, agent escalated with the timing reason. After veryfying this behaviour I commented the cutoff guard. 
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
CALM uses the LLM to understand user messages and extract values like guest count or deposit amount, instead of relying on manually written intents, rules, and regex-style validation code. Python is still used for the important business rules, such as deposit limits and escalation conditions, because those decisions need to stay deterministic. The old approach felt more explicit and easier to inspect step by step, but CALM is simpler to build and handles natural language more smoothly.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
CALM agent is significantly harder to setup than LangGraph. But this costs buy us control. CALM agent cannot freely improvise or call a tool that wasn't defined in flows.yml. I think it's a feature rather than limitation for booking confirmation case because there are important constraints that always need to be kept (like deposit size, booking time, etc).
"""
