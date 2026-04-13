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

You will build both of these this week, using two different architectures
that are genuinely better at their respective halves of the problem. In
the final assignment (releases 2026-04-18) they get merged into one
hybrid system called **PyNanoClaw**, plus a handoff bridge, memory, and
observability. Everyone builds both halves — there are no tracks. See
`PROGRESS.md` for the full architecture diagram.

The guiding question for this week:

> *Which architecture handles the research?
> Which one takes the call from the manager?
> Why does the same agent doing both feel wrong?*

---

## The two halves of PyNanoClaw you will build this week

### The autonomous loop (`sovereign_agent/`)
A LangGraph agent that reasons and acts autonomously. It receives a task,
decides its own sequence of steps, calls tools, handles failures, and returns
a result — without human guidance at each turn. This is the right tool for
open-ended problems where the path cannot be predetermined. In PyNanoClaw
this becomes the half that handles the research: searching venues, checking
weather, estimating costs.

### The structured agent (`exercise3_rasa/`)
A Rasa Pro CALM agent that handles structured interactions with real people.
Its behaviour is defined as explicit flows with deterministic business rules
enforced in Python. This is the right tool for high-stakes conversations where
every decision must be auditable and every constraint must be guaranteed. In
PyNanoClaw this becomes the half that handles the pub-manager call:
confirming headcount, agreeing deposit terms, enforcing Rod's limits.

Neither is universally better. They are designed for different problems. The
skill of an agent engineer is knowing which to reach for — and how to connect
them into a system that is both powerful and reliable.

By the end of the module you will have built both and connected them
through a shared tool layer (MCP) into PyNanoClaw, then adapted the
combined system to a scenario from your own work.

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
├── CHANGELOG.md               ← read this if you pulled updates
│
├── sovereign_agent/           ← THE AUTONOMOUS LOOP (half 1 of PyNanoClaw)
│   │                             grows into: tools → planning → memory → production
│   ├── tools/
│   │   ├── venue_tools.py     ← Exercise 2: the four venue tools, already implemented
│   │   └── mcp_venue_server.py ← shared tool server (used by both halves)
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
└── exercise3_rasa/            ← THE STRUCTURED AGENT (half 2 of PyNanoClaw)
    │                             grows into: flows → voice → RAG → production
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

### Exercise 2 — LangGraph Research Agent (the autonomous loop)

You run the autonomous research loop and observe what it does. This becomes
the research half of PyNanoClaw in the final assignment.

**About Task B — the flyer tool.** The scaffold now ships with a working
`generate_event_flyer` implementation that uses a graceful fallback pattern.
The original version of this task asked you to write a direct call to the
Nebius FLUX image endpoint, but Nebius removed FLUX from the Token Factory
on 2026-04-13 — the same day this assignment is due. See `CHANGELOG.md`
§Changed for the full story.

The new Task B is about *reading* the implementation and *observing* what it
does. The tool tries a live image provider if `FLYER_IMAGE_MODEL` is set in
your `.env`, and otherwise returns a deterministic `placehold.co` URL with
`mode: "placeholder"`. Both paths are valid. You record which one your run
took in `ex2_answers.py` → `TASK_B_MODE`. If you want to wire in a
non-Nebius image provider (OpenAI, Replicate, local SDXL), just set
`FLYER_IMAGE_MODEL` in `.env` and the tool will use it — no code changes.

```bash
make ex2        # run everything
make ex2-a      # Task A: main brief
make ex2-b      # Task B: flyer tool (runs the fallback or live path)
make ex2-c      # Task C: failure modes
make ex2-d      # Task D: graph — paste output into mermaid.live
```

Fill in `week1/answers/ex2_answers.py`.

---

### Exercise 3 — Rasa Pro CALM Agent (the structured agent)

You build the structured confirmation agent. This becomes the structured
half of PyNanoClaw in the final assignment.

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

You connect both halves to the same tool server. This is the bridge that
lets the autonomous loop and the structured agent share capabilities —
and, in the final assignment, makes PyNanoClaw possible.

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

Week 1 lays both foundations. Week 2's session adds real tools and
deepens MCP. The final assignment (releases 2026-04-18) merges everything
into PyNanoClaw.

| Phase | What lands |
|------|------------|
| **Week 1 (now)** | Autonomous loop + venue tools; CALM confirmation flow + business rules; shared MCP server. Both halves exist, neither knows about the other yet. |
| **Week 2 session** | Real web search, file operations, deeper MCP. Both halves learn to pull tools from the same server. No separate homework. |
| **Final assignment** | PyNanoClaw: planner/executor split, memory (filesystem + RAG), handoff bridge between the two halves, observability, optional voice pipeline. You apply it to a scenario from your own work. |

By the end of the module PyNanoClaw is production-grade and connected
through a shared MCP tool layer. You then spend the final session adapting
it to a scenario from your own work — replacing Edinburgh pubs with
whatever your job actually needs automated.

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

**"No tool calls were made" in Exercise 2 or 4**
This was the Llama-on-Nebius tool-calling bug — fixed in the 2026-04-13
release. Pull the latest main (`git fetch upstream && git merge upstream/main`),
then re-run. The default model is now `Qwen/Qwen3-32B`, which emits native
tool calls correctly. See `CHANGELOG.md` §Fixed for the full story.

**Exercise 3: `Connection refused` when running `make ex3-chat`**
`make ex3-actions` is not running. Start it in another terminal and wait for
`Action endpoint is up and running` before proceeding.

**Exercise 3: `make ex3-train` hangs**
Rasa downloads embedding models on first train (~300–500 MB). Check internet
connection and disk space, then try again.

**Exercise 3: `Provider List: https://docs.litellm.ai/docs/providers`**
This was the litellm provider routing bug — fixed in the 2026-04-13 release.
Pull the latest main AND re-run `make ex3-train` (the model group is baked
into the trained model at train time, so you must retrain after pulling).

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

Your fork IS your submission. Commit and push to `main` — the grader reads
directly from `github.com/YOUR-USERNAME/sovereign-agent-lab` at the deadline
timestamp. There is no separate portal upload, no form, no file attachment.

```bash
git checkout main
git merge <your-branch>          # if you worked on a branch
make check-submit                # last sanity pass
git push origin main
```

**Deadline:** 2026-04-13 23:59 UTC−12 (equivalently **2026-04-14 12:00 noon
London time**). Commits on `main` after that timestamp are not graded.
Feature branches are not graded.

The grader checks:
- `week1/outputs/*.json` — proof you ran the exercises
- `week1/answers/*.py` — your filled-in answers
- `sovereign_agent/tools/venue_tools.py` — the flyer tool returns a valid
  success dict (either live-provider mode or placeholder fallback)
- `exercise3_rasa/actions/actions.py` — your Task B cutoff guard is
  uncommented

Run `make check-submit` before pushing — it tells you exactly what is
missing. See `GRADING_OVERVIEW.md` for the full 30/40/30 point breakdown
and `CHANGELOG.md` for the list of fixes landed since the initial release.