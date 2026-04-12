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
Ok, I am updating guest_count to 160 respectively.
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit                                                                                                              
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
What else can I help you with?
Your input ->  
"""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  calling to confirm a booking                                                                                              
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan                                                                                                       
Ok, I am updating guest_count to 160 respectively.
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £500 deposit                                                                                                              
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £500 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
What else can I help you with?                                                                                                                        
"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "The issue is: a deposit of £500 exceeds the organiser's authorised limit of £300."   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input ->  calling to confirm a booking                                                                                              
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                
And how many of those guests will need vegan meals?
Your input ->  can you arrange parking for the speakers?                                                                                 
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Let's continue with confirm booking.
And how many of those guests will need vegan meals?
Your input ->  
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
CALM recognied that the user's request about parking was out of scope. It responded with a polite refusal, then steered the conversation back to the expected flow.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
LangGraph's agent gave gave a vague response asking for more details while CALM explicitly said it only handles venue bookings and suggested contacting the organiser.
CALM's response is better for a real booking assistant because it clearly sets expectations and guides the user. LangGraph's response is more open-ended and could lead to confusion or a breakdown in the conversation if the user doesn't know what details to provide.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
I uncommented the cutoff guard code in ActionValidateBooking, my computer's clock was likely 18:00. The agent escalated as expected with the correct reason. However, I was expecting to excalate after I said that I want to confirm the booking for tonight, nt avfter asking me all the clarifying questions about number of guests and vegan options.
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
CALM lets the LLM handle what Python used to do: parsing natural language into 
slot values. In old Rasa, you needed regex in a ValidateBookingConfirmationForm 
to turn "about 160 people" into 160.0. In CALM, from_llm mappings handle this 
automatically. Python still handles the business rules — checking deposit limits, 
capacity ceilings, and vegan ratios — because those are deterministic constraints 
that must never be negotiated or reasoned around. The cost is that you now depend 
on an LLM for slot extraction, which is probabilistic rather than deterministic. 
With regex, "160" always parsed to 160.0. With an LLM, it almost always works but 
there is no guarantee. The gain is far less code and far more flexibility — users 
can say "one-sixty", "about 160", or "we're expecting 160" and it all works 
without writing a single regex pattern.
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
The CALM agent cannot improvise. It cannot call a tool that was not defined in 
flows.yml, it cannot invent a new conversation path, and it cannot decide on its 
own to check the weather or generate a flyer. For the confirmation use case, this 
is a feature, not a limitation. When a pub manager calls to confirm a booking and 
agree deposit terms, every word has financial and legal weight. The agent must 
collect exactly the right information, apply exactly the right constraints, and 
never go off-script. The setup cost of CALM — config files, training, two terminals, a licence — 
buys you predictability and auditability that LangGraph cannot provide.
"""
