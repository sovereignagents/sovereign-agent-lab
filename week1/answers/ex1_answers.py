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

PART_A_PLAIN_CORRECT    = True  # True or False
PART_A_XML_CORRECT      = True
PART_A_SANDWICH_CORRECT = True

# Explain what you observed. Minimum 30 words.

PART_A_EXPLANATION = """
In this example we see all formats see me to perform equally.However we should consider the pros and cons of each. \
The Plain formatting is  normally more user friendly. However for a longer list of venues there is the risk that \
the mode wont be able to infer boundaries properly.This is solved with XML formatting. LLMs are normally trained in \
structures data in form (<query>, <response>) so if the prompts is structured in this way the model is more easily guided\
for pattern recoginition and hyierachy. This is ony reason we see once the model find the top correct answer returns just that.\
WE also observe the the XML uses more tokens due to the special characters of the formatting.
The  Sandwisch approach is more model intuitive because the model attends to tokesn as they appear.This means that late tokes \
receive more attention and by adding the query reminder at the end we push the instruction of the query on focus\
with less logical errors.

With the distractors we see that we still get correct answers probably because of the simplicity of the task but\
since the distractors are close together and in similar format that may be a problem as they are likely to get similar attention\
We also observe that in
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
With the distractors we see that we still get correct answers probably because of the simplicity of the task but\
since the distractors are close together [The Holyrood Arms]  and in similar format as well satisfying 2/3 conditions,
 \that may be a problem as they are likely to get similar attention\
"""

# ── Part C ─────────────────────────────────────────────────────────────────

# Did the exercise run Part C (small model)?
# Check outputs/ex1_results.json → "part_c_was_run"
PART_C_WAS_RUN = True   # True or False

PART_C_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_C_XML_ANSWER      = "The Haymarket Vaults"
PART_C_SANDWICH_ANSWER = "The Haymarket Vaults"

# Explain what Part C showed, or why it wasn't needed. Minimum 30 words.
PART_C_EXPLANATION = """
in part 3 we switch to a smaller model, with less parameters we expect more basic reasoning and less pattern identification\
The smaller model is likely to be affected more by unstructured prompts especially is the prompt requires multi level resoning.\
In this example we see the model performed as well as the larger models probably because the request was very simple
"""

# ── Core lesson ────────────────────────────────────────────────────────────

# Complete this sentence. Minimum 40 words.
# "Context formatting matters most when..."

CORE_LESSON = """
Context formatting matters most when we use small model that need clearer strucutre and instructions to infer logically.\
The formatting also matter when we have multi level reasoning and clearer formatting/instruction  with repetition is likely to\
give better attention and better inference results/.Context window als matters when we have  difficutl tasks that re likely to\
push the  context window capabilities. In this case the model will be more prone to hallucination, so clear formatting, and clear instructions\
will help with that.
"""
