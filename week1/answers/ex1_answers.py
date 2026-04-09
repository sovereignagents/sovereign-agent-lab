"""
Exercise 1 — Answers
====================
Fill this in after running exercise1_context.py.
Run `python grade.py ex1` to check for obvious issues before submitting.
"""

# ── Part A ─────────────────────────────────────────────────────────────────

# The exact answer the model gave for each condition.
# Copy-paste from your terminal output (the → "..." part).

PART_A_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_A_XML_ANSWER      = "The Albanach"
PART_A_SANDWICH_ANSWER = "The Albanach"

# Was each answer correct? True or False.
# Correct = contains "Haymarket" or "Albanach" (both satisfy all constraints).

PART_A_PLAIN_CORRECT    = True
PART_A_XML_CORRECT      = True
PART_A_SANDWICH_CORRECT = True

# Explain what you observed. Minimum 30 words.

PART_A_EXPLANATION = """
All three formatting conditions produced correct answers with the 70B model on the baseline data.
The PLAIN condition chose The Haymarket Vaults, while XML and SANDWICH both chose The Albanach.
This suggests that structured formatting (XML tags or sandwich priority markers) may influence which
valid venue the model selects, even when the underlying data is the same. However, all answers
were correct — both venues meet the 160-guest capacity and vegan requirements.
"""

# ── Part B ─────────────────────────────────────────────────────────────────

PART_B_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_B_XML_ANSWER      = "The Albanach"
PART_B_SANDWICH_ANSWER = "The Albanach"

PART_B_PLAIN_CORRECT    = True
PART_B_XML_CORRECT      = True
PART_B_SANDWICH_CORRECT = True

# Did adding near-miss distractors change any results? True or False.
PART_B_CHANGED_RESULTS = False

# Which distractor was more likely to cause a wrong answer, and why?
# Minimum 20 words.
PART_B_HARDEST_DISTRACTOR = """
A near-miss distractor with high capacity but missing vegan options (like The Guilford Arms at 200 capacity
but no vegan menu) would be the hardest, because the model must resist selecting a venue that looks good
on the most salient dimension (size) while failing on a secondary constraint (dietary). The 70B model
handled both distractors correctly in all conditions.
"""

# ── Part C ─────────────────────────────────────────────────────────────────

# Did the exercise run Part C (small model)?
# Check outputs/ex1_results.json → "part_c_was_run"
PART_C_WAS_RUN = True

PART_C_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_C_XML_ANSWER      = "The Haymarket Vaults"
PART_C_SANDWICH_ANSWER = "The Haymarket Vaults"

# Explain what Part C showed, or why it wasn't needed. Minimum 30 words.
PART_C_EXPLANATION = """
Part C ran because Parts A and B were all correct, triggering the small 8B model test with distractors.
The 8B model also answered all three conditions correctly, choosing The Haymarket Vaults every time.
Unlike the 70B model which varied between Haymarket Vaults and The Albanach depending on formatting,
the 8B model consistently picked the same venue regardless of context structure. This suggests that
for this particular task, even the smaller model was capable enough that formatting differences did
not cause failures — though the 8B model showed less sensitivity to formatting cues overall.
"""

# ── Core lesson ────────────────────────────────────────────────────────────

# Complete this sentence. Minimum 40 words.
# "Context formatting matters most when..."

CORE_LESSON = """
Context formatting matters most when the model is operating near its capability limits — with
a harder task, more distractors, ambiguous constraints, or a smaller model. In this experiment,
both the 70B and 8B models answered correctly across all formatting conditions, but the formatting
still influenced which correct venue was selected. In production, where tasks are more complex and
context windows are larger, structured formatting with XML tags or sandwich prioritization becomes
critical for ensuring the model attends to the right constraints and does not lose important
information buried in the middle of a long context.
"""
