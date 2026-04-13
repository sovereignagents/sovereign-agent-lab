"""
sovereign_agent/tests/test_week1.py
=====================================
Self-check tests for Week 1.

Run these before submitting:
    python -m pytest sovereign_agent/tests/test_week1.py -v

These tests check your tool implementations directly, without running the
full agent loop. They're faster than grade.py and give more specific
error messages when something is wrong.

If these pass, your code is likely to pass the mechanical and
behavioural grading checks too. If they fail, fix the issue before
running the full exercises.

These tests use only the standard library and pytest — no API calls.
They're safe to run offline.
"""

import json
import pytest
import sys
from pathlib import Path

# Add the student_pack root to path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sovereign_agent.tools.venue_tools import (
    check_pub_availability,
    get_edinburgh_weather,
    calculate_catering_cost,
    generate_event_flyer,
)

def _call(tool_fn, **kwargs) -> dict:
    """Call a @tool decorated function and parse its JSON result."""
    raw_fn = tool_fn.func if hasattr(tool_fn, "func") else tool_fn
    result = raw_fn(**kwargs)
    return json.loads(result) if isinstance(result, str) else result

# ─── check_pub_availability ───────────────────────────────────────────────────

class TestCheckPubAvailability:

    def test_available_venue_meets_all(self):
        """A venue with capacity 160, vegan=True, and status=available should pass."""
        result = _call(check_pub_availability,
                       pub_name="The Haymarket Vaults",
                       required_capacity=160,
                       requires_vegan=True)
        assert result["success"] is True
        assert result["meets_all_constraints"] is True

    def test_full_venue_fails_constraints(self):
        """The Bow Bar is full — meets_all_constraints must be False."""
        result = _call(check_pub_availability,
                       pub_name="The Bow Bar",
                       required_capacity=160,
                       requires_vegan=True)
        assert result["success"] is True
        assert result["meets_all_constraints"] is False
        assert result["status"] == "full"

    def test_insufficient_capacity_fails(self):
        """The Bow Bar has capacity 80, which is less than 160."""
        result = _call(check_pub_availability,
                       pub_name="The Bow Bar",
                       required_capacity=160,
                       requires_vegan=False)
        assert result["success"] is True
        assert result["meets_all_constraints"] is False

    def test_no_vegan_fails_when_required(self):
        """The Guilford Arms has vegan=False. Should fail when vegan is required."""
        result = _call(check_pub_availability,
                       pub_name="The Guilford Arms",
                       required_capacity=100,
                       requires_vegan=True)
        assert result["success"] is True
        assert result["meets_all_constraints"] is False

    def test_unknown_venue_returns_error(self):
        """A venue not in VENUES should return success=False with known_venues list."""
        result = _call(check_pub_availability,
                       pub_name="The Imaginary Pub",
                       required_capacity=100,
                       requires_vegan=False)
        assert result["success"] is False
        assert "error" in result
        assert "known_venues" in result
        assert isinstance(result["known_venues"], list)
        assert len(result["known_venues"]) > 0

    def test_returns_address(self):
        """A successful lookup should include the address."""
        result = _call(check_pub_availability,
                       pub_name="The Albanach",
                       required_capacity=100,
                       requires_vegan=False)
        assert result["success"] is True
        assert "address" in result
        assert len(result["address"]) > 0

    def test_returns_json_string(self):
        """The raw return value must be a valid JSON string."""
        raw_fn = check_pub_availability.func if hasattr(check_pub_availability, "func") else check_pub_availability
        raw = raw_fn(pub_name="The Albanach", required_capacity=100, requires_vegan=False)
        assert isinstance(raw, str), "Tool must return a string, not a dict"
        parsed = json.loads(raw)
        assert isinstance(parsed, dict)

# ─── calculate_catering_cost ──────────────────────────────────────────────────

class TestCalculateCateringCost:

    def test_correct_calculation(self):
        result = _call(calculate_catering_cost, guests=160, price_per_head_gbp=35.0)
        assert result["success"] is True
        assert result["total_cost_gbp"] == 5600.0
        assert result["guests"] == 160

    def test_zero_guests_fails(self):
        result = _call(calculate_catering_cost, guests=0, price_per_head_gbp=35.0)
        assert result["success"] is False

    def test_negative_price_fails(self):
        result = _call(calculate_catering_cost, guests=160, price_per_head_gbp=-5.0)
        assert result["success"] is False

    def test_rounding(self):
        """Check that totals are rounded to 2 decimal places."""
        result = _call(calculate_catering_cost, guests=3, price_per_head_gbp=33.333)
        assert result["success"] is True
        # 3 × 33.333 = 99.999 → should round to 100.0
        assert abs(result["total_cost_gbp"] - 100.0) < 0.01

# ─── generate_event_flyer ─────────────────────────────────────────────────────
#
# Note on the changed contract (2026-04-13): the flyer tool used to be a stub
# that students had to replace with a real FLUX image call. Nebius removed
# FLUX from the Token Factory on the same day this assignment is due, so the
# tool now ships with a working graceful-fallback implementation that returns
# success=True in both live and placeholder modes. The tests below assert the
# new contract: (1) the function accepts venue_name/guest_count/event_theme,
# (2) the prompt contains the venue name, (3) it returns a non-empty image URL,
# (4) it never returns the legacy STUB error shape.

class TestGenerateEventFlyer:

    def test_returns_required_keys(self):
        """The function must return a dict with success, prompt_used, image_url."""
        result = _call(generate_event_flyer,
                       venue_name="The Haymarket Vaults",
                       guest_count=160,
                       event_theme="AI Meetup")
        assert "success" in result, "Must have 'success' key"
        assert "prompt_used" in result, "Must have 'prompt_used' key"
        assert "image_url" in result, "Must have 'image_url' key"

    def test_prompt_includes_venue_name(self):
        """The prompt should mention the venue."""
        result = _call(generate_event_flyer,
                       venue_name="The Haymarket Vaults",
                       guest_count=160,
                       event_theme="AI Meetup")
        assert "Haymarket" in result["prompt_used"], \
            "prompt_used should mention the venue name"

    def test_fallback_returns_success(self):
        """
        The graceful-fallback path must return success=True with mode='placeholder'
        and a non-empty image_url. This replaces the old "stub detection" test.
        If this fails, either the scaffold has been reverted to a broken stub
        or something is raising inside the tool — check CHANGELOG.md §Changed
        and the implementation in sovereign_agent/tools/venue_tools.py.
        """
        result = _call(generate_event_flyer,
                       venue_name="The Haymarket Vaults",
                       guest_count=160,
                       event_theme="AI Meetup")
        assert result.get("success") is True, \
            ("generate_event_flyer must return success=True. "
             "See CHANGELOG.md §Changed for the graceful-fallback contract.")
        assert "STUB" not in str(result.get("error", "")).upper(), \
            "generate_event_flyer must not return the legacy stub error."

    def test_image_url_is_non_empty_string(self):
        """image_url must always be a non-empty string when success=True."""
        result = _call(generate_event_flyer,
                       venue_name="The Haymarket Vaults",
                       guest_count=160,
                       event_theme="AI Meetup")
        assert result.get("success") is True
        assert isinstance(result["image_url"], str)
        assert len(result["image_url"]) > 0, \
            "image_url should not be empty when success=True"