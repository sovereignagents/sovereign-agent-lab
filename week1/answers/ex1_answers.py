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
All three conditions were answered correctly by Llama 3.3 70B. Notably, PLAIN
picked The Haymarket Vaults while XML and SANDWICH both returned The Albanach —
which is also valid but appears first in the list. Structured formatting seems
to trigger a mild primacy bias, causing the model to latch onto the first item
that satisfies all constraints rather than scanning through to Haymarket Vaults.
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
The Holyrood Arms is the most dangerous distractor — capacity=160, vegan=yes,
but status=full. It satisfies two of the three constraints and sits immediately
before the correct answer. A model skimming rather than evaluating all three
constraints simultaneously would likely select it, since it looks almost right.
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
Part C ran because Parts A and B were all-correct, requiring the 8B model to
stress-test format sensitivity. The 8B model also got all three conditions right,
but unlike the 70B model it returned The Haymarket Vaults consistently across
formats — no primacy bias toward The Albanach. This suggests the dataset is still
too short and clean to expose format-driven failures even in smaller models;
the signal-to-noise ratio is simply too high.
"""

# ── Core lesson ────────────────────────────────────────────────────────────

# Complete this sentence. Minimum 40 words.
# "Context formatting matters most when..."

CORE_LESSON = """
Context formatting matters most when the signal-to-noise ratio is low: when
distractors are numerous and plausible, when the critical information is buried
in the middle of a long context, or when using a smaller model whose attention
mechanism struggles to discriminate between similar candidates. On short, clean
datasets, even lightweight models can find the correct answer regardless of
presentation — so format becomes the decisive variable only when the task is
genuinely hard.
"""
