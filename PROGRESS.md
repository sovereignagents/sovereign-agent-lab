# Where This Is Going
## Week 1 → Week 5: Your Sovereign Agent

---

## The Five-Week Arc

By Week 5 you will have one of two things running on your machine:

**Track A — The OpenClaw Automator**
An always-on, headless agent that receives a task (via WhatsApp, file watch,
or API call), plans autonomously, executes tools, stores results in memory,
and sends a summary — all while you sleep.

**Track B — The Rasa Digital Employee**
A voice-capable conversational agent that handles structured interactions
— booking confirmations, customer queries, HR requests — with auditable
business logic, proper fallbacks, and a voice pipeline connecting a
microphone to a speaker.

Both start here, in Week 1.

---

## What You're Building Each Week

```
Week 1 (now)
│
├── sovereign_agent/tools/venue_tools.py      ← tool layer foundation
├── sovereign_agent/tools/mcp_venue_server.py ← shared tool server
├── sovereign_agent/agents/research_agent.py  ← basic ReAct loop
└── exercise3_rasa/                           ← Rasa confirmation agent
         │
         │  Week 2: real tools
         ▼
├── sovereign_agent/tools/web_search.py       ← live web search
├── sovereign_agent/tools/file_ops.py         ← file read/write
└── research_agent.py extended with real tools
         │
         │  Week 3: planning
         ▼
├── sovereign_agent/agents/planner.py         ← thinking model (DeepSeek R1)
└── sovereign_agent/agents/executor.py        ← fast worker (Llama 70B)
         │
         │  Week 4: memory
         ▼
├── sovereign_agent/memory/claude_md.py       ← CLAUDE.md persistent memory
└── sovereign_agent/memory/vector_store.py    ← RAG for Rasa
         │
         │  Week 5: production
         ▼
└── Your complete Sovereign Agent (live demo)
```

---

## How Week 1 Code Gets Extended (Not Replaced)

Every file you write this week will be *imported* in future weeks.
Nothing gets thrown away.

### `sovereign_agent/agents/research_agent.py`

**Week 1:** Basic ReAct loop with 3 venue tools.

**Week 2 extension you'll make:**
```python
# You'll add this import and wire in real tools
from sovereign_agent.tools.web_search import search_web
from sovereign_agent.tools.file_ops import read_file, write_file

# Your existing agent gets new capabilities by adding tools to this list
agent = create_react_agent(llm, [
    check_pub_availability,   # ← from Week 1
    get_edinburgh_weather,    # ← from Week 1
    calculate_catering_cost,  # ← from Week 1
    search_web,               # ← new in Week 2
    write_file,               # ← new in Week 2
])
```

**Week 3 extension:** You'll split this into planner.py and executor.py.
The single agent becomes two specialised components. The tools stay the same.

### `sovereign_agent/tools/mcp_venue_server.py`

**Week 2 extension:** You'll add more tools to this server (web search, booking confirmation).
The server grows. The clients (LangGraph agent, Rasa action) don't change.

### `exercise3_rasa/`

**Week 2 extension:** You'll add MCP tool access to the Rasa action server,
so the confirmation agent can look up live venue data instead of using the hardcoded test.

**Week 4 extension:** You'll add a RAG knowledge base that the agent queries
when the manager asks questions the domain.yml doesn't explicitly handle.

---

## Track Selection

You must choose your track by the end of Week 2. Both tracks complete all exercises in
Weeks 1 and 2. From Week 3, the tracks diverge:

**Track A (OpenClaw)** goes deep on:
- Planner-Executor with DeepSeek R1 as the thinking model
- CLAUDE.md style filesystem memory
- Async event loop and heartbeat scheduling
- Security sandboxing and cost guardrails

**Track B (Rasa)** goes deep on:
- Voice pipeline: Whisper STT → Rasa CALM → LLM → TTS
- Advanced CALM flows with conditional branching
- Custom actions calling real APIs
- The Rasa Studio interface for non-technical stakeholders

The choice should be based on what you want to build in the real world,
not on which you think is easier. Both are equally viable for the final demo.

---

## The Edinburgh Thread

The Edinburgh pub problem runs through all five weeks as a constant reference point.
This is deliberate: you can see exactly how the same problem gets more powerful as your
agent gains new capabilities.

| Week | What the Edinburgh agent can do |
|---|---|
| 1 | Look up venues from a local database, check weather, estimate costs |
| 2 | Actually search the web for Edinburgh pubs, read venue websites |
| 3 | Plan autonomously: search → filter → verify → book → generate flyer |
| 4 | Remember previous searches across sessions, learn from past bookings |
| 5 | Handle the full scenario end-to-end in a live demo, with observability |

By Week 5, Rod fires off the WhatsApp and wakes up to a confirmed booking,
a generated flyer, and a confirmation email — all done while he slept.
