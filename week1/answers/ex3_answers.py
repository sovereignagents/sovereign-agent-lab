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
RASA_NOT_YET_RUN — requires RASA_PRO_LICENSE.
> Expected behavior based on code review:
> Your input: I'm calling to confirm a booking
> Bot: How many guests are you expecting?
> Your input: 160 guests
> Bot: How many of those need vegan meals?
> Your input: about 50 need vegan
> Bot: What deposit amount in GBP are you offering?
> Your input: 200 pounds
> Bot: Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
"""

CONVERSATION_1_OUTCOME = "confirmed"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
RASA_NOT_YET_RUN — requires RASA_PRO_LICENSE.
> Expected behavior based on code review:
> Your input: I'm calling to confirm a booking
> Bot: How many guests are you expecting?
> Your input: 160 guests
> Bot: How many of those need vegan meals?
> Your input: about 50 need vegan
> Bot: What deposit amount in GBP are you offering?
> Your input: 500 pounds
> Bot: I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £500 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
"""

CONVERSATION_2_OUTCOME = "escalated"
CONVERSATION_2_REASON  = "a deposit of £500 exceeds the organiser's authorised limit of £300"

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
RASA_NOT_YET_RUN — requires RASA_PRO_LICENSE.
> Expected behavior based on code review:
> Your input: I'm calling to confirm a booking
> Bot: How many guests are you expecting?
> Your input: can you arrange parking for the speakers?
> Bot: I'm sorry, I can only help with booking confirmations. How many guests are you expecting?
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
Based on the CALM flow design, the agent would recognize the parking question as out of scope
via the utter_out_of_scope response, then redirect the conversation back to the booking
confirmation flow by re-asking for the guest count. CALM's flow-based architecture keeps the
conversation on track because the LLM can only trigger flows defined in flows.yml — there is
no way for it to improvise an answer about parking.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
LangGraph and Rasa CALM handle out-of-scope requests very differently. LangGraph's agent gave a
vague non-answer ("Your input is lacking necessary details") and stopped — it did not try to call
tools, which was correct, but it also did not explain that train times are outside its scope or
suggest an alternative resource. Rasa CALM, by contrast, would deflect with a clear out-of-scope
message and then immediately resume the booking flow from where it left off, re-asking for the
missing slot. The key difference is that CALM maintains conversational state: it knows it is in
the middle of collecting booking details and returns to that task. LangGraph has no such memory
of an ongoing flow — each query is essentially stateless. For a booking confirmation assistant,
CALM's approach is clearly superior because it keeps the call on track.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
The cutoff guard was uncommented in actions.py. The four lines that check datetime.datetime.now()
against 16:45 are now active. To verify the guard works, you would temporarily change the condition
to 'if True:' and run a conversation — the agent should immediately escalate with the message about
insufficient time before the 5 PM deadline. Then revert the condition back to the time check.
Rasa was not actually run due to missing RASA_PRO_LICENSE, but the code change is in place.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

CALM_VS_OLD_RASA = """
CALM simplifies development significantly by offloading language understanding to the LLM. In old
Rasa, you needed regex-based slot extraction in Python (parsing "about 160 people" into 160.0),
extensive NLU training examples in nlu.yml, and explicit dialogue rules. CALM eliminates all of
that: the LLM handles natural language parsing via from_llm slot mappings, and flow descriptions
replace rigid rules. What Python still handles — and must handle — are the deterministic business
rules: deposit limits, capacity checks, vegan ratios, and the time cutoff guard. These cannot be
trusted to an LLM because the LLM might rationalize exceptions. The cost of CALM is that you lose
fine-grained control over how language is interpreted and depend on the LLM's quality. The gain is
dramatically less boilerplate code and better handling of natural language variations without
explicit training data.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

SETUP_COST_VALUE = """
CALM's setup cost — config.yml, domain.yml, flows.yml, endpoints.yml, training, two terminals,
and a Rasa Pro license — buys you something specific: constrained execution. The CALM agent cannot
improvise responses outside its defined flows, cannot call tools not specified in flows.yml, and
cannot skip the business rule validation in ActionValidateBooking. It will always collect all three
slots before running the validation action. LangGraph, by contrast, is a single Python file with
a generic loop — faster to set up but the agent can do anything the LLM decides, including skipping
steps or making up information. For a booking confirmation call where legal and financial constraints
must be enforced deterministically, CALM's rigidity is a feature: the agent physically cannot confirm
a booking without running the Python guards. That guarantee is what the setup cost pays for.
"""
