"""
sovereign_agent/tools/venue_tools.py
=====================================
The venue tool layer for your Sovereign Agent.

────────────────────────────────────────────────────────────────────────────
NOTE ON generate_event_flyer  (updated 2026-04-09)
────────────────────────────────────────────────────────────────────────────
The original version of this exercise asked you to call Nebius's FLUX
image-generation endpoint. Nebius has since announced the deprecation of
all text-to-image models on their Token Factory (removed 2026-04-13 — the
same day this assignment is due). See:

    https://docs.tokenfactory.nebius.com/other-capabilities/deprecation-info

So we have changed what this tool teaches.

The new version of the tool shows you a pattern that matters more in
production than "call an API": graceful degradation. The tool tries to
generate a real image if a provider is available, and if it is not, it
returns a well-structured "flyer brief" with a deterministic placeholder
URL. Either way the tool contract is satisfied: the agent gets back a
`success=True` dict with a `prompt_used` and an `image_url`, and the
downstream flow keeps working.

This is a more honest lesson. Real agent tools fail, providers deprecate
models, networks flake. A tool that raises on failure takes the whole
loop down. A tool that returns a structured "degraded-but-usable" result
keeps the agent moving.

Task B, revised:
    Read through the implementation below and understand how the fallback
    works. Then, in ex2_answers.py, record:
      - whether your flyer call hit the real provider or the fallback
      - what URL was returned
      - one sentence on why the agent did not need to change behaviour
        when the provider disappeared.

If you implemented Task B the old way — with a direct client.images.generate
call — your implementation is still valid for grading. Add a try/except
around it so it survives the April-13 deprecation and you are done.
────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import hashlib
import json
import os
import requests
from langchain_core.tools import tool
from openai import OpenAI

# ─── Venue database ───────────────────────────────────────────────────────────
# In Week 2 this gets replaced with a real web search.
# For now, it's a small hardcoded database so we can focus on the agent loop.
#
# Key design note: The Bow Bar has status="full". This is intentional —
# it creates a realistic failure case for the agent to navigate.

VENUES = {
    "The Albanach": {
        "capacity": 180,
        "vegan": True,
        "status": "available",
        "address": "2 Hunter Square, Edinburgh",
    },
    "The Haymarket Vaults": {
        "capacity": 160,
        "vegan": True,
        "status": "available",
        "address": "1 Dalry Road, Edinburgh",
    },
    "The Guilford Arms": {
        "capacity": 200,
        "vegan": False,
        "status": "available",
        "address": "1 West Register Street, Edinburgh",
    },
    "The Bow Bar": {
        "capacity": 80,
        "vegan": True,
        "status": "full",
        "address": "80 West Bow, Edinburgh",
    },
}


def _get_nebius_client() -> OpenAI:
    return OpenAI(
        base_url="https://api.tokenfactory.nebius.com/v1/",
        api_key=os.getenv("NEBIUS_KEY"),
    )


@tool
def check_pub_availability(
    pub_name: str,
    required_capacity: int,
    requires_vegan: bool,
) -> str:
    """
    Check if a named Edinburgh pub meets capacity and dietary requirements.
    Returns whether ALL constraints are met, plus full venue details.
    Use this after you already have a specific venue name to evaluate.
    Do NOT use this to browse or search — you must already know the pub name.
    Known venues: The Albanach, The Haymarket Vaults, The Guilford Arms, The Bow Bar.
    """
    venue = VENUES.get(pub_name)
    if not venue:
        return json.dumps(
            {
                "success": False,
                "error": f"Venue not found: '{pub_name}'",
                "known_venues": list(VENUES.keys()),
            }
        )

    meets_all = (
        venue["capacity"] >= required_capacity
        and (not requires_vegan or venue["vegan"])
        and venue["status"] == "available"
    )

    return json.dumps(
        {
            "success": True,
            "pub_name": pub_name,
            "address": venue["address"],
            "capacity": venue["capacity"],
            "vegan": venue["vegan"],
            "status": venue["status"],
            "meets_all_constraints": meets_all,
        }
    )


@tool
def get_edinburgh_weather() -> str:
    """
    Get current weather in Edinburgh (55.95N, 3.19W) from Open-Meteo.
    No API key required. Returns temperature, description, and outdoor_ok.
    outdoor_ok is True only when conditions are clear or mainly clear.
    Use this to advise whether an outdoor area at the venue is suitable.
    """
    try:
        resp = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": 55.95,
                "longitude": -3.19,
                "current": "temperature_2m,weather_code,precipitation",
                "forecast_days": 1,
            },
            timeout=8,
        )
        resp.raise_for_status()
        data = resp.json().get("current", {})
        code = data.get("weather_code", -1)
        descriptions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            61: "Light rain",
            63: "Moderate rain",
            65: "Heavy rain",
            80: "Rain showers",
            95: "Thunderstorm",
        }
        return json.dumps(
            {
                "success": True,
                "temp_c": data.get("temperature_2m"),
                "description": descriptions.get(code, f"Code {code}"),
                "precipitation_mm": data.get("precipitation"),
                "outdoor_ok": code in {0, 1, 2},
            }
        )
    except requests.exceptions.Timeout:
        return json.dumps({"success": False, "error": "Weather API timed out"})
    except Exception as exc:
        return json.dumps({"success": False, "error": str(exc)})


@tool
def calculate_catering_cost(guests: int, price_per_head_gbp: float) -> str:
    """
    Estimate total catering cost in GBP for the Edinburgh event.
    Use AFTER confirming a venue. Do NOT call before a venue is confirmed.
    Returns total_cost_gbp, guests, and price_per_head_gbp.
    """
    if guests <= 0 or price_per_head_gbp < 0:
        return json.dumps(
            {
                "success": False,
                "error": "guests must be > 0 and price_per_head_gbp must be >= 0",
            }
        )
    return json.dumps(
        {
            "success": True,
            "guests": guests,
            "price_per_head_gbp": price_per_head_gbp,
            "total_cost_gbp": round(guests * price_per_head_gbp, 2),
        }
    )


# ─── Flyer generation with graceful fallback ────────────────────────────────
# Implementation notes for students reading this file:
#
#   1. We build the prompt first. The prompt is deterministic — the same
#      (venue, guests, theme) always produces the same prompt string. That
#      gives us a stable hash for the placeholder URL in the fallback path.
#
#   2. We *try* to hit a real image-generation endpoint if one is configured
#      via FLYER_IMAGE_MODEL. If it works, great. If it fails for any reason
#      (deprecation, rate limit, network, wrong key), we catch the exception
#      and fall through to the placeholder path. We DO NOT raise.
#
#   3. The placeholder path returns a deterministic URL from a free
#      placeholder service, plus the full prompt so the human reviewing the
#      trace knows what the flyer would have looked like. This matters for
#      auditing: "agent said it generated a flyer" should be inspectable.
#
# Why is this the right shape for an agent tool?
#   Because the agent loop cannot recover from exceptions inside tools. If
#   this function raised, the whole ReAct loop would halt mid-task. By
#   always returning a structured success dict, we keep the agent's control
#   flow intact regardless of what is happening at the provider.

def _build_flyer_prompt(venue_name: str, guest_count: int, event_theme: str) -> str:
    return (
        f"Professional event flyer for {event_theme} at {venue_name}, "
        f"Edinburgh. {guest_count} guests tonight. Warm lighting, "
        f"Scottish architecture background, clean modern typography."
    )


def _attempt_real_image_generation(prompt: str) -> str | None:
    """
    Try to generate a real image. Return the URL on success, or None on
    any failure — we never raise from this helper.

    Enable this path by setting FLYER_IMAGE_MODEL in your .env to the name
    of an image-generation model your provider still supports. As of the
    2026-04-13 FLUX deprecation on Nebius, there is no default image model
    configured — the tool will transparently use the placeholder path.
    """
    model = os.getenv("FLYER_IMAGE_MODEL", "").strip()
    if not model:
        return None
    try:
        from openai import OpenAI

        client = OpenAI(
            base_url=os.getenv(
                "FLYER_IMAGE_BASE_URL",
                "https://api.tokenfactory.nebius.com/v1/",
            ),
            api_key=os.getenv("NEBIUS_KEY"),
        )
        response = client.images.generate(model=model, prompt=prompt, n=1)
        return response.data[0].url
    except Exception:
        return None


@tool
def generate_event_flyer(venue_name: str, guest_count: int, event_theme: str) -> str:
    """
    Generate a promotional event flyer image for the confirmed Edinburgh venue.
    Call this AFTER a venue is confirmed, as the final output step.
    Returns a URL to the generated image.
    venue_name: the confirmed pub name
    guest_count: confirmed number of attendees
    event_theme: short description, e.g. 'AI Meetup, professional, Scottish'
    """
    prompt = (
        f"Professional event flyer for {event_theme} at {venue_name}, "
        f"Edinburgh. {guest_count} guests tonight. Warm lighting, "
        f"Scottish architecture background, clean modern typography."
    )
    try:
        client = _get_nebius_client()
        response = client.images.generate(
            model="black-forest-labs/flux-schnell",
            prompt=prompt,
            n=1,
        )
        url = response.data[0].url if response.data else ""
        return json.dumps({
            "success": True,
            "prompt_used": prompt,
            "image_url": url,
        })
    except Exception as exc:
        return json.dumps({
            "success": False,
            "error": str(exc),
            "prompt_used": prompt,
            "image_url": "",
        })
