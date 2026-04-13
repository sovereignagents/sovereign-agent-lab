# Where This Is Going
## Week 1 → Final Assignment: PyNanoClaw

---

## The Arc

By the end of the module you will have built **PyNanoClaw**: a hybrid
agent system that combines an autonomous research loop with a structured,
auditable conversational agent, connected through a shared tool layer.

The same problem runs through the whole module so you can watch it get
more powerful as each piece is added:

> *Rod fires off a WhatsApp — "sort the pub for tonight, 160 people, vegan
> options, confirm by 5pm" — and puts his phone away. Three hours later the
> pub is booked, the manager has confirmed the deposit on a phone call, the
> flyer is rendered, and a confirmation email is in Rod's inbox.*

That scenario has two genuinely different sub-problems. Research — "which
pub, given these constraints, right now" — is open-ended, requires
reasoning across tool calls, and cannot be scripted in advance. Confirmation
— "the pub manager called back, now commit to a deposit on Rod's behalf" —
is high-stakes, must be auditable, and cannot improvise. PyNanoClaw solves
both by using the right technology for each half and wiring them together.

> **Note on course structure (2026-04-13).** This module was originally
> planned as three homeworks across five weeks and two separate "tracks"
> (an OpenClaw Automator track and a Rasa Digital Employee track). It has
> been consolidated: two homeworks total, one hybrid system everyone
> builds. The Week 1 assignment (due 2026-04-13) establishes the
> foundations for both halves. The final assignment (releases 2026-04-18)
> merges them into PyNanoClaw. See `CHANGELOG.md` §Added for the reasoning.

---

## The PyNanoClaw Architecture

PyNanoClaw is one system with two halves. Each half uses the tooling that
fits its half of the problem, and both halves talk to a shared tool server.

```
                      ┌─────────────────────────────┐
                      │    Shared MCP Tool Server    │
                      │    (venue lookups, web       │
                      │     search, calendar, ...)   │
                      └──────────────┬──────────────┘
                                     │
                  ┌──────────────────┴──────────────────┐
                  │                                     │
         ┌────────▼─────────┐                 ┌─────────▼─────────┐
         │  Autonomous Loop │                 │  Structured Agent │
         │  (LangGraph)     │                 │  (Rasa Pro CALM)  │
         │                  │                 │                   │
         │  Plans its own   │                 │  Explicit flows,  │
         │  steps, reasons  │                 │  deterministic    │
         │  across tools,   │                 │  business rules,  │
         │  handles the     │                 │  handles the      │
         │  research        │                 │  pub manager call │
         └──────────────────┘                 └───────────────────┘
```

You are building both halves this week. In Week 1, each half is a small
independent exercise (Exercise 2 builds the loop, Exercise 3 builds the
structured agent, Exercise 4 wires them to the same tool server). In the
final assignment they become components of PyNanoClaw: the loop hands off
to the structured agent when a human conversation is needed, the structured
agent hands back to the loop when research is needed, and both draw from
the same tool server.

This is the core lesson of the module: knowing which technology belongs
where, and how to compose them. Not "pick the one you like best."

---

## What You're Building Each Phase

```
Week 1 (now) — foundations for both halves
│
├── sovereign_agent/tools/venue_tools.py       ← tool layer foundation
├── sovereign_agent/tools/mcp_venue_server.py  ← shared tool server
├── sovereign_agent/agents/research_agent.py   ← the autonomous loop
└── exercise3_rasa/                            ← the structured agent
         │
         │  Week 2 session: tools & MCP in depth
         │  (no separate homework — feeds into the final assignment)
         ▼
├── sovereign_agent/tools/web_search.py        ← live web search
├── sovereign_agent/tools/file_ops.py          ← file read/write
└── research_agent.py extended with real tools
         │
         │  Final assignment (2026-04-18) — PyNanoClaw
         │  Merges both halves into one hybrid system
         ▼
├── pynanoclaw/agents/planner.py               ← thinking model upstream of the loop
├── pynanoclaw/agents/executor.py              ← fast worker inside the loop
├── pynanoclaw/memory/persistent_store.py      ← filesystem-backed memory
├── pynanoclaw/memory/vector_store.py          ← RAG for the structured agent
├── pynanoclaw/bridge/handoff.py               ← loop ⇄ structured-agent bridge
├── pynanoclaw/observability/                  ← tracing, cost tracking, guardrails
└── (optional) voice pipeline                  ← microphone → structured agent → speaker
         │
         ▼
    PyNanoClaw — live end-to-end demo against your own scenario
```

The model names and file layouts above are illustrative, not fixed. The
final assignment will specify the exact models based on what is still
available on Nebius Token Factory at release time — the 2026-04-13
deprecation round removed several models that earlier drafts of this
document referenced. See `CHANGELOG.md` §Fixed for the full list.

---

## How Week 1 Code Gets Extended (Not Replaced)

Every file you write this week becomes a component of PyNanoClaw.
Nothing gets thrown away.

### `sovereign_agent/agents/research_agent.py`

**Week 1:** Basic ReAct loop with 4 venue tools.

**In PyNanoClaw (final assignment):** this file becomes the *executor*
inside the autonomous-loop half of the system. A planner runs upstream of
it, a memory layer runs alongside it, and a handoff bridge routes
human-conversation tasks to the structured-agent half instead of handling
them itself. The tool list grows, but the core loop stays.

```python
# Roughly what the final assignment will have you do.
# Your Week 1 research_agent.py keeps working as-is — you add on top.
from sovereign_agent.tools.web_search import search_web
from sovereign_agent.tools.file_ops import read_file, write_file

agent = create_react_agent(llm, [
    check_pub_availability,   # ← from Week 1
    get_edinburgh_weather,    # ← from Week 1
    calculate_catering_cost,  # ← from Week 1
    generate_event_flyer,     # ← from Week 1
    search_web,               # ← new
    write_file,               # ← new
    handoff_to_structured,    # ← new — delegates to the Rasa half
])
```

### `sovereign_agent/tools/mcp_venue_server.py`

**Week 1:** Two MCP tools (search + detail fetch); both halves can connect.

**In PyNanoClaw:** the same server grows to cover every capability both
halves need — web search, booking confirmation, calendar access, email.
Neither half of PyNanoClaw cares where a tool came from; they both discover
tools dynamically from the server. That is exactly why MCP is the layer
that lets a hybrid system hang together.

### `exercise3_rasa/`

**Week 1:** A CALM confirmation agent with three business-rule guards.

**In PyNanoClaw:** this becomes the *structured-agent half*. The final
assignment will have you:

- Wire it to the shared MCP server, so it can look up live venue data.
- Add a RAG knowledge base for questions the `flows.yml` doesn't cover.
- Add a handoff tool so it can delegate research back to the loop.
- Optionally add a voice pipeline (Speechmatics STT/TTS) wrapping the
  whole thing. This is optional because the core lesson — structured,
  auditable business logic — is complete without it.

---

## The Edinburgh Thread

The Edinburgh pub problem runs through the whole module as a constant
reference point. This is deliberate: you can see exactly how the same
problem gets more powerful as each piece is added.

| Phase | What the Edinburgh agent can do |
|---|---|
| Week 1 | Look up venues from a local database, check weather, estimate costs, generate a flyer. Handle a simulated pub-manager call with structured business rules. Both halves exist, neither knows about the other yet. |
| Week 2 session | Add real web search and file operations to the loop. Teach both halves to pull tools from the same MCP server. |
| Final assignment | Merge into PyNanoClaw. The loop hands off to the structured agent when a human call is needed. The structured agent hands back to the loop when it needs research. Memory, observability, and the optional voice pipeline land. You apply the whole thing to a scenario from your own work. |

By the end of the module, Rod fires off the WhatsApp and wakes up to a
confirmed booking, a generated flyer, and a confirmation email — done by
PyNanoClaw while he slept.