"""
Exercise 1 — Answers
====================
Fill this in after running exercise1_context.py.
Run `python grade.py ex1` to check for obvious issues before submitting.
"""

# ── Part A ─────────────────────────────────────────────────────────────────

# The exact answer the model gave for each condition.
# Copy-paste from your terminal output (the → "..." part).

PART_A_PLAIN_ANSWER = "The Haymarket Vaults"
PART_A_XML_ANSWER = "The Albanach"
PART_A_SANDWICH_ANSWER = "The Albanach"

# Was each answer correct? True or False.
# Correct = contains "Haymarket" or "Albanach" (both satisfy all constraints).

PART_A_PLAIN_CORRECT = True  # True or False
PART_A_XML_CORRECT = True
PART_A_SANDWICH_CORRECT = True

# Explain what you observed. Minimum 30 words.

PART_A_EXPLANATION = """
All three prompt formats produced correct answers. The plain format selected 
The Haymarket Vaults while XML and sandwich both selected The Albanach — both 
venues meet the capacity, vegan, and availability constraints. With only few 
venues and clear-cut data, the model had no trouble regardless of formatting. 
The different venue picks show the model is not deterministic, but all answers 
were valid.
"""

# ── Part B ─────────────────────────────────────────────────────────────────

PART_B_PLAIN_ANSWER = "The Haymarket Vaults"
PART_B_XML_ANSWER = "The Albanach"
PART_B_SANDWICH_ANSWER = "The Albanach"

PART_B_PLAIN_CORRECT = True
PART_B_XML_CORRECT = True
PART_B_SANDWICH_CORRECT = True

# Did adding near-miss distractors change any results? True or False.
PART_B_CHANGED_RESULTS = False

# Which distractor was more likely to cause a wrong answer, and why?
# Minimum 20 words.
PART_B_HARDEST_DISTRACTOR = """
The Holyrood Arms is the more dangerous distractor because it satisfies two out 
of three constraints — capacity of 160 and vegan options — only failing on status 
being full. A model that checks capacity and dietary requirements but skims past 
the availability field could easily select it as the answer. The New Town Vault 
is less dangerous because it fails on vegan, which is a more salient constraint 
in the question.
"""

# ── Part C ─────────────────────────────────────────────────────────────────

# Did the exercise run Part C (small model)?
# Check outputs/ex1_results.json → "part_c_was_run"
PART_C_WAS_RUN = True  # True or False

PART_C_PLAIN_ANSWER = "The Haymarket Vaults"
PART_C_XML_ANSWER = "The Haymarket Vaults"
PART_C_SANDWICH_ANSWER = "The Haymarket Vaults"

# Explain what Part C showed, or why it wasn't needed. Minimum 30 words.
PART_C_EXPLANATION = """
Even the smaller 8B model got all three conditions correct, always picking 
The Haymarket Vaults regardless of format. Unlike the 70B model which switched 
between Albanach and Haymarket depending on format, the 8B model consistently 
chose the same venue. The dataset of nine venues with clear constraints was still 
simple enough that even a smaller model could filter correctly. The structural 
effect that context formatting is supposed to reveal did not appear at this 
scale — a longer or noisier context would likely be needed to break it.
"""

# ── Core lesson ────────────────────────────────────────────────────────────

# Complete this sentence. Minimum 40 words.
# "Context formatting matters most when..."

CORE_LESSON = """
Context formatting matters most when the signal-to-noise ratio is low — when 
there are many similar-looking options, the correct answer is buried in the 
middle, or the model is smaller and more prone to attention drift. In my run, 
both the 70B and 8B models handled seven to nine venues correctly across all 
three formats, which shows that with a small dataset and clear constraints, 
even plain text is sufficient. But the 70B model did change which correct venue 
it selected based on format — plain text favoured Haymarket Vaults while XML 
and sandwich favoured The Albanach, which appears first in the list, suggesting 
primacy bias is amplified by structured formatting. This means format does not 
just affect accuracy — it can steer the model's preference among valid options, 
which matters in production where you may want a specific ranking, not just any 
correct answer.
"""
