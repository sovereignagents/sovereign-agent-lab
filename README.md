# Edinburgh Agent — Week 1 Assignment
**AI Performance Engineering · Module 1 · Nebius Academy**

---

## TL;DR — the commands you will use most

```bash
make install        # set up the project (run once)
make install-rasa   # set up the Rasa environment (run once)
make smoke          # verify your API key works
make ex1            # run Exercise 1
make ex2            # run Exercise 2
make ex3-train      # train Rasa (Exercise 3, run once)
make ex3-actions    # Terminal 1 — Rasa action server
make ex3-chat       # Terminal 2 — chat with the agent
make ex4            # run Exercise 4
make grade          # check everything before submitting
make help           # show all available commands
```

If you are on Windows, see the Windows note in the Setup section.

---

## What you are building

Rod fires off a WhatsApp and puts his phone away for three hours:

> *"Sort the pub for tonight. 160 people, vegan options, quiet corner for a
> webinar. Confirm by 5 PM."*

Two things need to happen, and they are genuinely different problems:

**Problem A — Research.** Search venues, cross-check requirements, pull the
weather, estimate costs. Nobody knows the exact steps in advance. The agent
must reason its way through unknowns, pivot when a venue is full, and surface
the best option without Rod guiding it step by step.

**Problem B — Confirmation.** The pub manager calls back. Handle that call —
confirm headcount, agree deposit terms, stay strictly within what Rod
authorised. Every word could cost money or create a legal commitment. The agent
must not improvise.

You will build both of these this week, using two different architectures.
Over the five weeks of this course you will keep extending them until, by
Week 5, they work together as a single system: one agent researches and plans
while the other handles high-stakes human interaction. Then you apply that same
combined architecture to a problem from your own work.

The guiding question for this week:

> *Which architecture handles the research?
> Which one takes the call from the manager?
> Why does the same agent doing both feel wrong?*

---

## The two architectures you will build

### The Headless Automator (`sovereign_agent/`)
A LangGraph agent that reasons and acts autonomously. It receives a task,
decides its own sequence of steps, calls tools, handles failures, and returns
a result — without human guidance at each turn. This is the right tool for
open-ended problems where the path cannot be predetermined.

### The Digital Employee (`exercise3_rasa/`)
A Rasa Pro CALM agent that handles structured interactions with real people.
Its behaviour is defined as explicit flows with deterministic business rules
enforced in Python. This is the right tool for high-stakes conversations where
every decision must be auditable and every constraint must be guaranteed.

Neither is universally better. They are designed for different problems. The
skill of an agent engineer is knowing which to reach for — and how to connect
them into a system that is both powerful and reliable.

By Week 5 you will have built both, connected them through a shared tool layer
(MCP), and adapted the combined architecture to a scenario from your own work.

---

## Tools

### uv — install this first, manually, one time

`uv` is a Python package manager made by Astral. It replaces `pip`, `venv`, and
`python -m`. After installing uv, everything else is handled by `make`.

```bash
# Mac or Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell):
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart your terminal, then verify:
```bash
uv --version
```

### make — may already be installed

`make` is a command runner. It reads the `Makefile` in this project and turns
`make ex1` into the correct `uv run python ...` command so you don't have to
remember anything.

**Mac:** already installed. **Linux:** already installed. **Windows:** run one of:
```bash
winget install GnuWin32.Make   # Windows Package Manager
choco install make             # Chocolatey
```
Or use Git Bash, which includes `make`.

---

## Project structure

```
sovereign-agent-lab/
│
├── Makefile                   ← all commands live here — type `make help`
├── pyproject.toml             ← project config and dependencies
├── .python-version            ← Python 3.14 for the main project
├── .env                       ← your API keys (create from .env.example)
│
├── sovereign_agent/           ← THE HEADLESS AUTOMATOR
│   │                             grows every week: tools → planning → memory → production
│   ├── tools/
│   │   ├── venue_tools.py     ← Exercise 2: implement generate_event_flyer here
│   │   └── mcp_venue_server.py ← shared tool server (used by both agents)
│   ├── agents/
│   │   └── research_agent.py  ← the core autonomous loop
│   └── tests/
│       └── test_week1.py
│
├── week1/
│   ├── exercise1_context.py
│   ├── exercise2_langgraph.py
│   ├── exercise4_mcp_client.py
│   ├── grade.py
│   ├── answers/               ← YOU FILL THESE IN
│   └── outputs/               ← auto-generated when you run exercises
│
└── exercise3_rasa/            ← THE DIGITAL EMPLOYEE
    │                             grows every week: flows → voice → RAG → production
    ├── pyproject.toml         ← Rasa Pro needs Python 3.10
    ├── .python-version
    ├── data/
    │   └── flows.yml          ← the CALM flows defining what the agent can do
    └── actions/
        └── actions.py         ← deterministic business rules in Python
```

---

## Setup — run once

### 1. Fork and clone the repo

You work in your own fork — not directly in the shared repo. This matters
for two reasons: your submission lives in your fork, and when we push updates
or fixes to the assignment (which happens), you can pull them into your fork
without losing your own work.

**Step 1 — Fork on GitHub**

Go to https://github.com/sovereignagents/sovereign-agent-lab and click
**Fork** (top right). Accept all defaults. This creates your own copy at
`github.com/YOUR-USERNAME/sovereign-agent-lab`.

**Step 2 — Clone your fork**

```bash
git clone https://github.com/YOUR-USERNAME/sovereign-agent-lab.git
cd sovereign-agent-lab
```

**Step 3 — Add the upstream remote**

This links your local clone back to the original repo so you can pull
instructor updates:

```bash
git remote add upstream https://github.com/sovereignagents/sovereign-agent-lab.git
git remote -v
```

You should see two remotes: `origin` (your fork) and `upstream` (ours).

#### Pulling an update from the instructor

When we announce an update, run:

```bash
git fetch upstream
git merge upstream/main
```

This brings in new scaffold files or fixes without overwriting your work.
Your answers live in `week1/answers/`, your implementations in
`sovereign_agent/` and `exercise3_rasa/actions/actions.py` — we never push
changes to those paths, so merges are almost always clean.

### 2. API key

```bash
cp .env.example .env
```

Open `.env` and replace the placeholders with your real keys. The only key
you need right now is `NEBIUS_KEY`. Everything else can wait until the week
it becomes relevant — the `.env.example` file explains each one.

```
NEBIUS_KEY=sk-abc123yourrealkey
```

No quotes. No spaces around the `=` sign.

### 3. Main environment

```bash
make install
```

Creates the virtual environment, downloads Python 3.14 if needed, installs
all packages. Takes 30–60 seconds the first time.

### 4. Verify

```bash
make smoke
```

You should see `✅  API connection OK`. If not, check your `.env` file.

### 5. Set up the Rasa Pro environment (Exercise 3 only)

Exercise 3 uses **Rasa Pro CALM** — a commercial product with a free
Developer Edition licence.

#### Get your free licence (2 minutes)

1. Go to **https://rasa.com/rasa-pro-developer-edition-license-key-request**
2. Enter your email address and accept the licence terms
3. Rasa will email you a licence key — check your inbox and spam folder
4. Open your `.env` file and paste the key:
   ```
   RASA_PRO_LICENSE=the-long-key-rasa-emailed-you
   ```

The Developer Edition is completely free and allows up to 1,000 conversations
per month running locally. No credit card required.

#### Install the Rasa environment

Once your licence key is in `.env`, run:

```bash
make install-rasa
```

uv will download Python 3.10 if needed and install Rasa Pro into
`exercise3_rasa/.venv/`. This takes 3–5 minutes the first time.

Verify it worked:
```bash
cd exercise3_rasa && uv run rasa --version
```

You should see `Rasa Version : 3.9.x`.

---

## Running the exercises

### Before every exercise

```bash
make test
```

Runs quick unit tests on your tool implementations. No API calls, no waiting.
Fix any failures before starting the exercise.

---

### Exercise 1 — Context Engineering

Foundational. Both agents depend on how you present information to models.

```bash
make ex1
```

Fill in `week1/answers/ex1_answers.py`.

---

### Exercise 2 — LangGraph Research Agent (the Automator)

You build the autonomous research loop. This becomes the core of the Headless
Automator that grows through Week 5.

**Before running Task B**, implement `generate_event_flyer` in
`sovereign_agent/tools/venue_tools.py`. Find the `# ── TODO` block.

```bash
make ex2        # run everything
make ex2-a      # Task A: main brief
make ex2-b      # Task B: flyer tool (implement TODO first)
make ex2-c      # Task C: failure modes
make ex2-d      # Task D: graph — paste output into mermaid.live
```

Fill in `week1/answers/ex2_answers.py`.

---

### Exercise 3 — Rasa Pro CALM Agent (the Digital Employee)

You build the structured confirmation agent. This becomes the core of the
Digital Employee that grows through Week 5.

Requires **two terminals** open at the same time.

**First time only — compile the CALM model:**
```bash
make ex3-train
```

**Then, in two separate terminals:**

```bash
# Terminal 1 — keep running
make ex3-actions

# Terminal 2 — chat
make ex3-chat
```

Wait for `Action endpoint is up and running` in Terminal 1 before starting
Terminal 2.

**Task B:** open `exercise3_rasa/actions/actions.py`, find the `# ── TASK B`
block, uncomment the four lines, then retrain:

```bash
make ex3-retrain
```

Fill in `week1/answers/ex3_answers.py`.

---

### Exercise 4 — Shared MCP Server

You connect both agents to the same tool server. This is the bridge that will
let the Automator and the Digital Employee share capabilities in Week 5.

```bash
make ex4
```

Do not skip the required experiment at the end of the output.

Fill in `week1/answers/ex4_answers.py`.

---

### Before you submit

```bash
make check-submit
```

Runs all checks and shows a final checklist. Fix every ✗ before submitting.

---

## Where this is going

Each week adds a new layer to both agents simultaneously:

| Week | Headless Automator | Digital Employee |
|------|--------------------|-----------------|
| **1** | Basic ReAct loop + venue tools | CALM confirmation flow + business rules |
| **2** | Real web search + file operations | MCP tool access + live venue data |
| **3** | Planner-Executor split (DeepSeek R1 + Llama 70B) | Advanced CALM flows + conditional branching |
| **4** | CLAUDE.md memory + vector store | RAG knowledge base |
| **5** | Observability + safety guardrails | Voice pipeline (Whisper → Rasa → TTS) |

By Week 5 both agents are production-grade and connected through a shared MCP
tool layer. You will then spend the final session adapting the combined system
to a scenario from your own work — replacing Edinburgh pubs with whatever your
job actually needs automated.

---

## Getting help

**Open a GitHub issue — this is the right place for all questions and problems.**

👉 **https://github.com/sovereignagents/sovereign-agent-lab/issues**

Click **New issue**, describe what you were trying to do, what command you ran,
and paste the full error output. Using issues keeps everything visible to the
whole cohort — if you hit a problem, someone else probably has too, and the
fix helps everyone at once. It also means the instructor can see patterns across
the group and fix things in the repo when needed.

**What to include in your issue:**

- Which exercise and which task (`make ex2-b`, `make ex3-train`, etc.)
- Your operating system and `uv --version`
- The full terminal output, including the error message
- What you have already tried

**Please search open and closed issues before posting**, your question may
already have an answer.

For anything that is genuinely private (grade queries, personal circumstances), email the instructor directly or reach out on LinkedIn. Everything else belongs in issues.

---

## Troubleshooting

**`make: command not found`**
Install make — see the Windows note in the Tools section above.

**`uv: command not found`**
Restart your terminal. If that fails: `source ~/.zshrc` (Mac) or
`source ~/.bashrc` (Linux).

**`No Python 3.14 found`**
```bash
uv python install 3.14 && make install
```

**`No Python 3.10 found`** (Rasa setup)
```bash
uv python install 3.10 && make install-rasa
```

**`.env still has the placeholder key`**
Open `.env` and replace the placeholder with your actual key. No quotes.

**`ModuleNotFoundError: No module named 'sovereign_agent'`**
Run `make install` from the project root (where the `Makefile` is).

**Exercise 3: `Connection refused` when running `make ex3-chat`**
`make ex3-actions` is not running. Start it in another terminal and wait for
`Action endpoint is up and running` before proceeding.

**Exercise 3: `make ex3-train` hangs**
Rasa downloads embedding models on first train (~300–500 MB). Check internet
connection and disk space, then try again.

**Exercise 3: licence key error**
Check `.env` has `RASA_PRO_LICENSE=your-key` with no quotes and no spaces.

**Any `make` command gives an unclear error**
Run the underlying command directly for the full stack trace:
```bash
uv run python week1/exercise1_context.py   # instead of make ex1
cd exercise3_rasa && uv run rasa train     # instead of make ex3-train
```

---

## Adding a package

```bash
uv add package-name     # adds to pyproject.toml and installs
uv remove package-name  # removes it
```

Do not use `pip install` directly — it bypasses the lock file.

---

## Submitting

Submit your fork URL in the course portal. The grader checks:
- `week1/outputs/*.json` — proof you ran the exercises
- `week1/answers/*.py` — your filled-in answers
- `sovereign_agent/tools/venue_tools.py` — your `generate_event_flyer`
- `exercise3_rasa/actions/actions.py` — your Task B cutoff guard

Run `make check-submit` before submitting — it tells you exactly what is
missing. See `GRADING_OVERVIEW.md` for the full 30/40/30 point breakdown.