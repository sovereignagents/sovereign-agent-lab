"""
Exercise 3 — Rasa Pro CALM Custom Actions
==========================================

WHY THIS FILE IS SIMPLER THAN OLD RASA TUTORIALS
-------------------------------------------------
In old Rasa (open source 3.x), you needed two classes:

  1. ValidateBookingConfirmationForm
     A FormValidationAction subclass with validate_guest_count(),
     validate_vegan_count(), etc. Each method used regex to parse
     "about 160 people" → 160.0 from raw text.

  2. ActionValidateBooking
     The post-form business rule checker.

In Rasa Pro CALM, the LLM handles slot extraction via `from_llm` mappings
in domain.yml. "About 160 people", "one-sixty", and "we're expecting 160"
all become 160.0 without any Python code on our side.

This means: we only need ONE action class here.

The architecture is cleaner:
  LLM handles language understanding  →  from_llm slot mappings in domain.yml
  Python enforces business rules      →  ActionValidateBooking below

This separation is the key lesson of Exercise 3.
The LLM decides what the user means.
Python decides whether that satisfies Rod's requirements.
One is probabilistic. The other is deterministic.
For legally and financially binding decisions, you want the second kind.

TASK B — CUTOFF GUARD
----------------------
Your task is to uncomment the four-line block marked "TASK B" below.

It adds a time-based guard: if it is past 16:45, escalate immediately —
there isn't enough time to process the booking before Rod's 5 PM deadline.

Steps:
  1. Uncomment the block (remove the # from each of the four lines inside it)
  2. Save this file
  3. Retrain: cd exercise3_rasa && uv run rasa train
  4. Restart the action server: uv run rasa run actions
  5. Test by temporarily making the condition always True:
         if True:   ← change just for testing
     Run a conversation, verify it escalates, then revert.
  6. Set TASK_B_DONE = True in week1/answers/ex3_answers.py
"""

import datetime
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

# ── Business constraints ──────────────────────────────────────────────────────
# Written as Python constants, not prompts.
# Change them here; they take effect on the next restart.
# The LLM cannot talk its way around these — the Python check always runs.

MAX_GUESTS      = 170    # venue hard capacity ceiling
MAX_DEPOSIT_GBP = 300    # Rod's maximum authorised deposit
MAX_VEGAN_RATIO = 0.80   # flag if more than 80% of guests need vegan meals


class ActionValidateBooking(Action):
    """
    Applies Rod's constraints after CALM has collected all three slots.

    In CALM, the LLM fills slots via from_llm mappings. This action
    runs after guest_count, vegan_count, and deposit_amount_gbp are all
    collected and runs the deterministic business rule checks.

    Each "Guard" is a separate Python check. The first that fails causes
    the agent to escalate — ask the manager to hold while it calls Rod.
    If all pass, the booking is confirmed.

    WHY NOT IN A PROMPT?
    If you wrote "only confirm if deposit is under £300" in a prompt,
    the LLM might reason: "the manager said it's a £250 fee plus £100
    insurance, so technically it's under £300 each." Python doesn't negotiate.
    """

    def name(self) -> Text:
        return "action_validate_booking"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # In CALM, from_llm slots are already the right type (float).
        # No parsing needed — the LLM did that work.
        guests  = float(tracker.get_slot("guest_count")       or 0)
        vegans  = float(tracker.get_slot("vegan_count")       or 0)
        deposit = float(tracker.get_slot("deposit_amount_gbp") or 0)

        def escalate(reason: str) -> List[Dict]:
            dispatcher.utter_message(
                text=(
                    "I need to check one thing with the organiser before I can confirm. "
                    f"The issue is: {reason}. "
                    "Can I call you back within 15 minutes?"
                )
            )
            return [
                SlotSet("booking_valid", False),
                SlotSet("rejection_reason", reason),
            ]

        # ── TASK B: Cutoff Guard ──────────────────────────────────────────────
        # Uncomment these four lines to add the time-based escalation guard.
        #
        now = datetime.datetime.now()
        if now.hour > 16 or (now.hour == 16 and now.minute >= 45):
            return escalate(
                "it is past 16:45 — insufficient time to process the confirmation"
                " before the 5 PM deadline"
            )

        # ── Guard 1: Venue capacity ───────────────────────────────────────────
        if guests > MAX_GUESTS:
            return escalate(
                f"the guest count ({int(guests)}) exceeds the venue's "
                f"maximum capacity of {MAX_GUESTS}"
            )

        # ── Guard 2: Deposit authorisation limit ──────────────────────────────
        if deposit > MAX_DEPOSIT_GBP:
            return escalate(
                f"a deposit of £{deposit:.0f} exceeds the organiser's "
                f"authorised limit of £{MAX_DEPOSIT_GBP}"
            )

        # ── Guard 3: Unusually high vegan ratio ───────────────────────────────
        vegan_ratio = vegans / guests if guests > 0 else 0
        if vegan_ratio > MAX_VEGAN_RATIO:
            return escalate(
                f"{int(vegans)} of {int(guests)} guests requiring vegan meals "
                f"({vegan_ratio:.0%}) is unusually high — needs organiser confirmation"
            )

        # ── All guards passed: confirm ────────────────────────────────────────
        dispatcher.utter_message(
            text=(
                f"Thank you — booking confirmed. "
                f"{int(guests)} guests, {int(vegans)} requiring vegan meals, "
                f"£{deposit:.0f} deposit accepted. "
                f"I'll send written confirmation to the organiser shortly."
            )
        )
        return [SlotSet("booking_valid", True)]
