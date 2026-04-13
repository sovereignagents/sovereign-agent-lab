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
        """The prompt sent to the image model should mention the venue."""
        result = _call(generate_event_flyer,
                       venue_name="The Haymarket Vaults",
                       guest_count=160,
                       event_theme="AI Meetup")
        assert "Haymarket" in result["prompt_used"], \
            "prompt_used should mention the venue name"

    def test_not_stub_when_implemented(self):
        """
        If you've implemented the tool (removed the stub), this test should pass.
        If it fails with 'STUB', go back and complete the TODO in venue_tools.py.
        """
        result = _call(generate_event_flyer,
                       venue_name="The Haymarket Vaults",
                       guest_count=160,
                       event_theme="AI Meetup")
        # This test will FAIL until you implement the tool.
        # That's expected — it's the signal that the task is incomplete.
        assert "STUB" not in str(result.get("error", "")), \
            ("generate_event_flyer still returns the stub. "
             "Complete the TODO in sovereign_agent/tools/venue_tools.py "
             "to replace it with a real images.generate() call.")

    def test_image_url_is_string_when_successful(self):
        """When success=True, image_url must be a non-empty string."""
        result = _call(generate_event_flyer,
                       venue_name="The Haymarket Vaults",
                       guest_count=160,
                       event_theme="AI Meetup")
        if result.get("success"):
            assert isinstance(result["image_url"], str)
            assert len(result["image_url"]) > 0, "image_url should not be empty when success=True"
