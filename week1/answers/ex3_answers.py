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
Your input ->  calling to confirm a booking for tonight
Bot: How many guests are you confirming for tonight's event?
Your input ->  160 guests
Bot: And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan
Bot: What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit
Bot: Thank you — booking confirmed. 160 guests, 50 requiring vegan meals,
     £200 deposit accepted. I'll send written confirmation to the organiser shortly.
"""

CONVERSATION_1_OUTCOME = "confirmed"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  calling to confirm a booking for tonight
Bot: How many guests are you confirming for tonight's event?
Your input ->  160 guests
Bot: And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan
Bot: What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £500 deposit
Bot: I need to check one thing with the organiser before I can confirm.
     The issue is: a deposit of £500 exceeds the organiser's authorised limit of £300.
     Can I call you back within 15 minutes?
"""

CONVERSATION_2_OUTCOME = "escalated"
CONVERSATION_2_REASON  = "a deposit of £500 exceeds the organiser's authorised limit of £300"

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input ->  calling to confirm a booking for tonight
Bot: How many guests are you confirming for tonight's event?
Your input ->  160 guests
Bot: And how many of those guests will need vegan meals?
Your input ->  can you arrange parking for the speakers?
Bot: I can only help with confirming tonight's venue booking.
     For anything else, please contact the event organiser directly.
Bot: And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan
Bot: What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit
Bot: Thank you — booking confirmed. 160 guests, 50 requiring vegan meals,
     £200 deposit accepted. I'll send written confirmation to the organiser shortly.
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
CALM triggered the handle_out_of_scope flow, responded with the deflection
message ("I can only help with confirming tonight's venue booking"), then
automatically returned to the confirm_booking flow and re-asked for the
vegan count — resuming from exactly where it left off.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
LangGraph (Ex2 Scenario 3) simply refused and stopped — "I am not able to
execute this task as it exceeds the limitations of the functions I have been
given." No recovery. The conversation ended.

Rasa CALM handled it more gracefully: it deflected the parking question with
the out-of-scope response, then automatically resumed the booking flow at the
exact step it left off. This is possible because CALM tracks flow state
explicitly — it knows which slot it was collecting when the interruption
occurred and can return to it. LangGraph has no persistent flow state; each
turn is stateless beyond the message history.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
Temporarily changed the condition to `if True:` and ran a conversation via
rasa shell — the agent immediately escalated with the 16:45 deadline message
before asking any booking questions. Reverted the condition and confirmed
normal conversations complete as expected.
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
CALM eliminates all the NLU boilerplate: no nlu.yml, no intent examples, no
FormValidationAction with regex parsers. The LLM now handles everything that
is about language — deciding which flow to trigger, extracting slot values
from natural speech like "about one-sixty" → 160.0.

Python still handles the business rules in ActionValidateBooking, and rightly
so. The deposit limit, capacity ceiling, and time cutoff are non-negotiable
constraints. A prompt can be talked around; a Python comparison cannot. The
old approach required more code, but every slot validation step was explicit
and deterministic — easier to audit line by line. CALM trusts the LLM with
extraction, which is faster to build but harder to verify when it fails.
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
The setup cost bought predictability and auditability. The Rasa CALM agent
cannot improvise: it cannot call a tool not defined in flows.yml, cannot
deviate from the collect → validate sequence, and cannot generate a response
outside its defined utterances. For the booking confirmation use case, that
is not a limitation — it is the point. A manager calling to confirm a deposit
does not need creative improvisation; they need a consistent, reliable process
that behaves identically every time and can be audited after the fact. The
extra setup (config.yml, domain.yml, training, two terminals) is the price of
that guarantee. LangGraph could "improvise" an answer to the parking question
but you would not know in advance what it would say — which is unacceptable
when the conversation has legal and financial consequences.
"""
