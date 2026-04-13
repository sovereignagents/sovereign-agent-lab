"""
sovereign_agent/tools/mcp_venue_server.py
==========================================
The shared MCP venue server for your Sovereign Agent.

This server exposes venue search as a standard MCP tool that any
MCP-compatible client can connect to. In Week 1, two clients use it:
  - The LangGraph research agent (Exercise 4)
  - The Rasa confirmation action (Exercise 4 optional extension)

In Week 2, you will add more tools to this server.
The clients don't need to change — they discover tools dynamically.

HOW TO RUN
----------
This server is started automatically via stdio when clients connect.
You don't need to run it manually.

To inspect it in isolation:
    python sovereign_agent/tools/mcp_venue_server.py
"""

import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("EdinburghVenueServer")

# Same venue database as venue_tools.py.
# In Week 2 both will be replaced with real web search results.
# For now, keeping them in sync here is intentional — it lets you compare
# the direct function call (LangGraph tools) vs the MCP call (Exercise 4)
# and verify they return the same data.

VENUES = {
    "The Albanach": {
        "capacity": 180,
        "vegan": True,
        "status": "full",
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


@mcp.tool()
def search_venues(min_capacity: int, requires_vegan: bool) -> str:
    """
    Search Edinburgh venues by minimum capacity and dietary requirements.
    Returns only venues that are currently available (status = available).
    Use this to find candidates before fetching individual details.
    min_capacity: minimum number of guests the venue must hold
    requires_vegan: if True, only venues with a vegan menu are returned
    """
    matches = [
        {"name": name, **info}
        for name, info in VENUES.items()
        if info["capacity"] >= min_capacity
        and (not requires_vegan or info["vegan"])
        and info["status"] == "available"
    ]
    return json.dumps({"matches": matches, "count": len(matches)})


@mcp.tool()
def get_venue_details(pub_name: str) -> str:
    """
    Get full details for a specific Edinburgh venue by its exact name.
    Returns capacity, vegan availability, status, and address.
    pub_name must match exactly a name returned by search_venues.
    """
    venue = VENUES.get(pub_name)
    if not venue:
        return json.dumps({
            "success": False,
            "error": f"Venue not found: '{pub_name}'",
            "known_venues": list(VENUES.keys()),
        })
    return json.dumps({"success": True, "name": pub_name, **venue})


if __name__ == "__main__":
    print(f"Edinburgh Venue MCP Server | {len(VENUES)} venues | stdio transport")
    mcp.run()
