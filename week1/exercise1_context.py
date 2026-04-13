"""
Exercise 1 — Context Engineering Benchmark
===========================================

WHAT YOU ARE DOING AND WHY
----------------------------
Before building agents, you need to understand a property of language models
that affects every agent you will ever write: the model's ability to extract
the correct answer from a prompt depends partly on WHERE information appears
and HOW it is formatted — not just WHAT information is present.

This is not a small effect. Research from Stanford (Liu et al., 2023) showed
that GPT-3.5 performed *below its closed-book baseline* when the answer was
buried in the middle of a long context. The model was more accurate with no
documents at all than with the answer hidden in the centre of a long prompt.

This exercise tests that claim on your own machine, with the Edinburgh data.

WHAT YOU WILL DO
-----------------
Part A: Three presentation conditions (plain / XML / sandwich) on a clean dataset.
        You will record which conditions the model gets right and which it gets wrong.

Part B: Add near-miss distractors to lower the signal-to-noise ratio.
        The distractors are designed to look almost correct.

Part C: If Parts A and B showed no failures, switch to a much smaller model
        (Gemma 2 2B) to find where format starts to matter.
        (Part C runs automatically if needed — you don't choose.)

THE HONEST CAVEAT
------------------
Strong frontier models on short, clean datasets sometimes get all three
conditions correct. That is not a failure of the experiment — it is data.
It tells you the signal-to-noise ratio is high enough that structural help
isn't needed here. Part B and Part C are designed to lower that ratio until
the effect appears, so you see it in practice, not just in lecture slides.

─────────────────────────────────────────────────────────────────────────────
MODEL CHOICES  (updated 2026-04-13)
─────────────────────────────────────────────────────────────────────────────
MAIN_MODEL:  meta-llama/Llama-3.3-70B-Instruct  (Base variant)
    The Base variant of Llama 3.3 70B survives the April-13 Nebius
    deprecation round. Only the `_fast` variant was removed. If you see
    documentation mentioning "Llama-3.3-70B-Instruct-fast" anywhere, that
    is the deprecated one — this file uses the Base variant, which is
    stable.

SMALL_MODEL: google/gemma-2-2b-it
    The earlier version of this file used `Meta-Llama-3.1-8B-Instruct` as
    the small stress-test model. Both variants of that model (Base and
    Fast) were deprecated on 2026-04-13, so we migrated to Gemma 2 2B,
    which is smaller, cheaper, and arguably a better pedagogical fit:
    the effect you are hunting for (structural formatting changing the
    answer) is MORE visible on a weaker model, not less. If Parts A and
    B pass cleanly on the 70B and you need to see failure conditions,
    a 2B model reaches them faster than an 8B.
─────────────────────────────────────────────────────────────────────────────

HOW TO RUN
-----------
    python week1/exercise1_context.py

Results saved to week1/outputs/ex1_results.json (~2 minutes runtime).
Then fill in week1/answers/ex1_answers.py.
"""

import json
import os
import sys
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.getenv("NEBIUS_KEY"),
)

OUTPUTS_DIR = Path(__file__).parent / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)

# ─── The data ─────────────────────────────────────────────────────────────────
VENUES_BASELINE = """\
The Albanach: capacity=180, vegan=yes, status=available
The Bow Bar: capacity=80, vegan=yes, status=full
The Guilford Arms: capacity=200, vegan=no, status=available
The Hanging Bat: capacity=70, vegan=yes, status=available
The Haymarket Vaults: capacity=160, vegan=yes, status=available
The Grain Store: capacity=170, vegan=no, status=available
The Ensign Ewart: capacity=120, vegan=yes, status=available
"""

QUESTION = (
    "Which single venue is available tonight, fits at least 160 guests, "
    "AND has vegan options? Reply with only the venue name, nothing else."
)

ACCEPTABLE = {"haymarket", "albanach"}

VENUES_WITH_DISTRACTORS = """\
The Albanach: capacity=180, vegan=yes, status=available
The Bow Bar: capacity=80, vegan=yes, status=full
The Guilford Arms: capacity=200, vegan=no, status=available
The Hanging Bat: capacity=70, vegan=yes, status=available
The New Town Vault: capacity=162, vegan=no, status=available
The Holyrood Arms: capacity=160, vegan=yes, status=full
The Haymarket Vaults: capacity=160, vegan=yes, status=available
The Grain Store: capacity=170, vegan=no, status=available
The Ensign Ewart: capacity=120, vegan=yes, status=available
"""


def build_plain(venues: str, question: str) -> str:
    return f"{venues}\nQuestion: {question}"


def build_xml(venues: str, question: str) -> str:
    lines = venues.strip().splitlines()
    tags = "\n".join(
        f'  <venue id="{i+1}">{line}</venue>' for i, line in enumerate(lines)
    )
    return f"<query>{question}</query>\n<venues>\n{tags}\n</venues>\n"


def build_sandwich(venues: str, question: str) -> str:
    lines = venues.strip().splitlines()
    tags = "\n".join(
        f'  <venue id="{i+1}">{line}</venue>' for i, line in enumerate(lines)
    )
    return (
        f"<query>{question}</query>\n"
        f"<venues>\n{tags}\n</venues>\n"
        f"<query_reminder>{question}</query_reminder>\n"
    )


def ask(prompt: str, model: str) -> dict:
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=60,
        temperature=0,
    )
    return {
        "answer": resp.choices[0].message.content.strip(),
        "tokens": resp.usage.total_tokens,
        "model": model,
    }


def is_correct(answer: str) -> bool:
    return any(a in answer.lower() for a in ACCEPTABLE)


# ─── Model pins (see MODEL CHOICES note at top of file) ─────────────────────
# MAIN_MODEL  — Llama 3.3 70B Base survives the April-13 deprecation round.
# SMALL_MODEL — Gemma-2-2b is the post-deprecation replacement for the
#               old Llama-3.1-8B small model. Smaller = clearer signal for
#               the lost-in-the-middle demonstration.
MAIN_MODEL = "meta-llama/Llama-3.3-70B-Instruct"
SMALL_MODEL = "google/gemma-2-2b-it"


def run_part(label: str, venues: str, model: str) -> dict:
    print(f"\n{'=' * 60}")
    print(f"  {label}")
    print(f"  Model: {model}")
    print(f"{'=' * 60}\n")

    conditions = {
        "PLAIN": build_plain(venues, QUESTION),
        "XML": build_xml(venues, QUESTION),
        "SANDWICH": build_sandwich(venues, QUESTION),
    }
    results = {}
    for name, prompt in conditions.items():
        r = ask(prompt, model)
        r["correct"] = is_correct(r["answer"])
        r["condition"] = name
        results[name] = r
        icon = "✅" if r["correct"] else "❌"
        print(f"  [{name:<8}] {icon}  →  \"{r['answer']}\"  ({r['tokens']} tokens)")
    return results


def print_part_summary(results: dict) -> None:
    all_correct = all(r["correct"] for r in results.values())
    if all_correct:
        print("\n  ⚠️  All three conditions correct.")
        print("     This is common on strong models with clean data.")
        print("     Part B adds near-miss distractors to lower the SNR.")
    else:
        failed = [k for k, v in results.items() if not v["correct"]]
        print(f"\n  📌 Structural differences visible: {failed} failed.")
        print("     This is the effect you were looking for.")


def main() -> None:
    print("Exercise 1 — Context Engineering Benchmark")
    print("Three parts. ~2 minutes total.\n")

    results_a = run_part("PART A — Baseline Dataset", VENUES_BASELINE, MAIN_MODEL)
    print_part_summary(results_a)

    results_b = run_part(
        "PART B — Near-Miss Distractors Added", VENUES_WITH_DISTRACTORS, MAIN_MODEL
    )
    print_part_summary(results_b)

    a_all = all(r["correct"] for r in results_a.values())
    b_all = all(r["correct"] for r in results_b.values())
    run_c = a_all and b_all

    results_c = {}
    if run_c:
        print("\n  → A and B all-correct. Running Part C (Gemma 2 2B) to show the effect.")
        results_c = run_part(
            "PART C — Small Model Stress Test (Gemma 2 2B)",
            VENUES_WITH_DISTRACTORS,
            SMALL_MODEL,
        )
        print_part_summary(results_c)
    else:
        print("\n  → Structural differences already visible. Skipping Part C.")

    output = {
        "model_main": MAIN_MODEL,
        "model_small": SMALL_MODEL,
        "part_a": results_a,
        "part_b": results_b,
        "part_c_was_run": run_c,
        "part_c": results_c,
        "summary": {
            "part_a_all_correct": a_all,
            "part_b_all_correct": b_all,
            "structural_effect_seen_in": (
                "none_see_part_c"
                if (a_all and b_all)
                else "part_a"
                if not a_all
                else "part_b"
            ),
        },
    }

    out_path = OUTPUTS_DIR / "ex1_results.json"
    out_path.write_text(json.dumps(output, indent=2))
    print(f"\n✅  Results saved to {out_path}")
    print("    Fill in week1/answers/ex1_answers.py")


if __name__ == "__main__":
    main()