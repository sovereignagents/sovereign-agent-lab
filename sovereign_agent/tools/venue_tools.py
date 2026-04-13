"""
sovereign_agent/tools/venue_tools.py
=====================================
The venue tool layer for your Sovereign Agent.

This file is part of the persistent sovereign_agent/ project.
It will be imported by your research agent in Exercise 2,
and the same tools will be exposed via MCP in Exercise 4.

In Week 2 you will ADD more tools to this file (web_search, file_ops).
The interface you establish here — each tool as a @tool decorated function
returning a JSON string — stays the same throughout the course.

WHY TOOLS RETURN JSON STRINGS
------------------------------
The LangGraph agent feeds tool results back into the model's context as text.
JSON strings are:
  - Human-readable (the model can parse them)
  - Consistent (always the same shape, success or failure)
  - Type-preserving (integers stay integers, booleans stay booleans)

Never return a plain string like "The pub is full." — the model can't
reliably extract structured data from that. Never raise an exception —
that crashes the agent loop. Always return a structured dict as a JSON string.

WEEK 1 TASK
-----------
These functions are provided as working stubs. Your task in Exercise 2
is to use them inside a LangGraph agent, not to modify them here.

The one thing you WILL do here: make sure you understand what each function
returns and when it returns an error — because the agent's ability to reason
about failures depends entirely on what these functions return.
"""

import json
import requests
from langchain_core.tools import tool
import os
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
        return json.dumps({
            "success": False,
            "error": f"Venue not found: '{pub_name}'",
            "known_venues": list(VENUES.keys()),
        })

    meets_all = (
        venue["capacity"] >= required_capacity
        and (not requires_vegan or venue["vegan"])
        and venue["status"] == "available"
    )

    return json.dumps({
        "success": True,
        "pub_name": pub_name,
        "address": venue["address"],
        "capacity": venue["capacity"],
        "vegan": venue["vegan"],
        "status": venue["status"],
        "meets_all_constraints": meets_all,
    })


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
            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy",
            3: "Overcast", 45: "Fog", 61: "Light rain", 63: "Moderate rain",
            65: "Heavy rain", 80: "Rain showers", 95: "Thunderstorm",
        }
        return json.dumps({
            "success": True,
            "temp_c": data.get("temperature_2m"),
            "description": descriptions.get(code, f"Code {code}"),
            "precipitation_mm": data.get("precipitation"),
            "outdoor_ok": code in {0, 1, 2},
        })
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
        return json.dumps({
            "success": False,
            "error": "guests must be > 0 and price_per_head_gbp must be >= 0",
        })
    return json.dumps({
        "success": True,
        "guests": guests,
        "price_per_head_gbp": price_per_head_gbp,
        "total_cost_gbp": round(guests * price_per_head_gbp, 2),
    })


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
    # ── TODO: Replace this stub with a real images.generate() call ───────────
    #
    # 1. Import OpenAI at the top of this file:
    #      from openai import OpenAI
    #      import os
    #
    # 2. Create the client:
    #      client = OpenAI(
    #          base_url="https://api.tokenfactory.nebius.com/v1/",
    #          api_key=os.getenv("NEBIUS_KEY"),
    #      )
    #
    # 3. Build the prompt — include venue name, guest count, event theme:
    #      prompt = (
    #          f"Professional event flyer for {event_theme} at {venue_name}, "
    #          f"Edinburgh. {guest_count} guests tonight. Warm lighting, "
    #          f"Scottish architecture background, clean modern typography."
    #      )
    #
    # 4. Call the image API:
    #      response = client.images.generate(
    #          model="black-forest-labs/flux-schnell",
    #          prompt=prompt,
    #          n=1,
    #      )
    #      url = response.data[0].url
    #
    # 5. Return a dict with at minimum: success, prompt_used, image_url
    #    On failure, return: success=False, error=str(e), prompt_used, image_url=""
    #
    # When implemented, the mechanical check in grade.py will pass automatically.
    # ──────────────────────────────────────────────────────────────────────────



    client = OpenAI(
         base_url="https://api.tokenfactory.nebius.com/v1/",
         api_key=os.getenv("NEBIUS_KEY"),
     )


    prompt = (
         f"Professional event flyer for {event_theme} at {venue_name}, "
         f"Edinburgh. {guest_count} guests tonight. Warm lighting, "
         f"Scottish architecture background, clean modern typography."
     )

    response = client.images.generate(
         model="black-forest-labs/flux-schnell",
         prompt=prompt,
         n=1,
     )
    url = response.data[0].url

    return json.dumps({
        "success": True,
        "error": "STUB — see TODO in sovereign_agent/tools/venue_tools.py",
        "prompt_used": prompt,
        "image_url": url,
    })
