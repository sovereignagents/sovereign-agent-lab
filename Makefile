# ==============================================================================
# 🎨 Terminal Colors
# ==============================================================================
GREEN   := $(shell tput -Txterm setaf 2 2>/dev/null || echo '')
YELLOW  := $(shell tput -Txterm setaf 3 2>/dev/null || echo '')
BLUE    := $(shell tput -Txterm setaf 4 2>/dev/null || echo '')
MAGENTA := $(shell tput -Txterm setaf 5 2>/dev/null || echo '')
RED     := $(shell tput -Txterm setaf 1 2>/dev/null || echo '')
RESET   := $(shell tput -Txterm sgr0  2>/dev/null || echo '')

# ==============================================================================
# ⚙️  Configuration
# ==============================================================================
UV       := uv
RASA_DIR := exercise3_rasa

# Load .env so targets that need NEBIUS_KEY can access it directly.
# If .env doesn't exist yet, nothing is loaded (no error).
ifneq (,$(wildcard .env))
    include .env
    export
endif

.DEFAULT_GOAL := help

# ==============================================================================
# 📖 Help  (shown when you run `make` with no arguments)
# ==============================================================================
.PHONY: help
help:
	@echo ''
	@echo '$(MAGENTA)🤖 Sovereign Agent Lab — Week 1$(RESET)'
	@echo ''
	@echo '$(YELLOW)First-time setup (run these once, in order):$(RESET)'
	@echo '  $(GREEN)make install$(RESET)            Set up main environment  (Python 3.14)'
	@echo '  $(GREEN)make install-rasa$(RESET)       Set up Rasa Pro env     (Python 3.10, needs licence)'
	@echo '  $(GREEN)make smoke$(RESET)              Verify your API key works'
	@echo ''
	@echo '$(YELLOW)If something is broken and you are stuck:$(RESET)'
	@echo '  $(GREEN)make doctor$(RESET)             Diagnose common setup problems'
	@echo ''
	@echo '$(YELLOW)Self-check (no API calls needed):$(RESET)'
	@echo '  $(GREEN)make test$(RESET)               Run tool unit tests — fix failures before exercises'
	@echo ''
	@echo '$(YELLOW)Exercise 1 — Context Engineering:$(RESET)'
	@echo '  $(GREEN)make ex1$(RESET)                Run the benchmark and save results'
	@echo ''
	@echo '$(YELLOW)Exercise 2 — LangGraph Research Agent:$(RESET)'
	@echo '  $(GREEN)make ex2$(RESET)                Run all tasks'
	@echo '  $(GREEN)make ex2-a$(RESET)              Task A — main Edinburgh brief'
	@echo '  $(GREEN)make ex2-b$(RESET)              Task B — flyer tool (graceful fallback observation)'
	@echo '  $(GREEN)make ex2-c$(RESET)              Task C — failure modes'
	@echo '  $(GREEN)make ex2-d$(RESET)              Task D — agent graph structure'
	@echo ''
	@echo '$(YELLOW)Exercise 3 — Rasa Confirmation Agent  (needs 2 terminals):$(RESET)'
	@echo '  $(GREEN)make ex3-train$(RESET)           Train the Rasa model  (first time + after changes)'
	@echo '  $(GREEN)make ex3-actions$(RESET)         Terminal 1 — action server  (keep running)'
	@echo '  $(GREEN)make ex3-chat$(RESET)            Terminal 2 — chat with the agent'
	@echo ''
	@echo '$(YELLOW)Exercise 4 — Shared MCP Server:$(RESET)'
	@echo '  $(GREEN)make ex4$(RESET)                Run the MCP client (server starts automatically)'
	@echo ''
	@echo '$(YELLOW)Grading:$(RESET)'
	@echo '  $(GREEN)make grade$(RESET)              Run mechanical checks before submitting'
	@echo '  $(GREEN)make grade-ex1$(RESET)          Check Exercise 1 only'
	@echo '  $(GREEN)make grade-ex2$(RESET)          Check Exercise 2 only'
	@echo '  $(GREEN)make grade-ex3$(RESET)          Check Exercise 3 only'
	@echo '  $(GREEN)make grade-ex4$(RESET)          Check Exercise 4 only'
	@echo ''
	@echo '$(YELLOW)Utilities:$(RESET)'
	@echo '  $(GREEN)make lint$(RESET)               Check your code for style issues (ruff)'
	@echo '  $(GREEN)make clean$(RESET)              Remove generated files and caches'
	@echo '  $(GREEN)make clean-rasa$(RESET)         Remove Rasa trained models (not the code)'
	@echo ''
	@echo '$(YELLOW)Windows users:$(RESET)'
	@echo '  Install make via: winget install GnuWin32.Make'
	@echo '  Or use Git Bash, which includes make.'
	@echo ''

# ==============================================================================
# 🚀 Setup checks  (used as prerequisites by other targets)
# ==============================================================================

.PHONY: check-uv
check-uv:
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "$(RED)✗ uv not found.$(RESET)"; \
		echo ""; \
		echo "  $(YELLOW)What to do:$(RESET)"; \
		echo "    Mac/Linux:  $(GREEN)curl -LsSf https://astral.sh/uv/install.sh | sh$(RESET)"; \
		echo "    Windows:    $(GREEN)powershell -c \"irm https://astral.sh/uv/install.ps1 | iex\"$(RESET)"; \
		echo ""; \
		echo "  Then $(YELLOW)restart your terminal$(RESET) and try again."; \
		echo "  If uv is installed but still not found, run: $(GREEN)make doctor$(RESET)"; \
		exit 1; \
	fi
	@echo "$(GREEN)✓ uv found: $(shell uv --version 2>/dev/null || echo unknown)$(RESET)"

# ──────────────────────────────────────────────────────────────────────────────
# check-env — validates the .env file without false positives.
#
# We had a bug in the earlier Makefile: `grep -q "sk-your-key-here" .env`
# would match that placeholder ANYWHERE in the file (e.g. inside an old
# comment), so students with a real key could still fail this check.
# See CHANGELOG.md [1.1.0] §Fixed for the story.
#
# This version:
#   1. Confirms .env exists
#   2. Extracts the VALUE of the NEBIUS_KEY line specifically (the first
#      uncommented `NEBIUS_KEY=…` assignment wins)
#   3. Rejects the literal placeholder, empty values, quoted values, and
#      the common "extra space around =" mistake
#   4. Emits one specific fix hint per failure mode, not a generic error
#
# The regex-ish shell logic is written in plain POSIX sh so it runs
# identically on Mac, Linux, and Windows Git Bash.
# ──────────────────────────────────────────────────────────────────────────────
.PHONY: check-env
check-env:
	@if [ ! -f .env ]; then \
		echo "$(RED)✗ .env file not found.$(RESET)"; \
		echo ""; \
		echo "  $(YELLOW)What to do:$(RESET)"; \
		echo "    $(GREEN)cp .env.example .env$(RESET)"; \
		echo "    then open .env and paste your real Nebius key"; \
		echo "    where it says $(YELLOW)NEBIUS_KEY=sk-your-key-here$(RESET)"; \
		exit 1; \
	fi
	@# Strip BOM if present (Windows Notepad adds one and it breaks parsing)
	@if head -c 3 .env 2>/dev/null | od -c 2>/dev/null | head -1 | grep -q '357 273 277'; then \
		echo "$(RED)✗ .env has a UTF-8 BOM marker at the start of the file.$(RESET)"; \
		echo "  This happens when you edit .env with Windows Notepad."; \
		echo ""; \
		echo "  $(YELLOW)Fix:$(RESET) open .env in VS Code (or any code editor)"; \
		echo "  and save it with encoding 'UTF-8' (not 'UTF-8 with BOM')."; \
		exit 1; \
	fi
	@if ! grep -Eq '^NEBIUS_KEY=' .env 2>/dev/null; then \
		echo "$(RED)✗ NEBIUS_KEY is missing from .env.$(RESET)"; \
		echo "  Add a line like: $(GREEN)NEBIUS_KEY=your-real-key$(RESET)"; \
		exit 1; \
	fi
	@if grep -Eq '^NEBIUS_KEY=(|sk-your-key-here)$$' .env 2>/dev/null; then \
		echo "$(RED)✗ NEBIUS_KEY is empty or still set to the placeholder.$(RESET)"; \
		echo "  Open .env and replace 'sk-your-key-here' with your real Nebius key."; \
		exit 1; \
	fi
	@echo "$(GREEN)✓ .env file looks valid (NEBIUS_KEY is set)$(RESET)"

# ──────────────────────────────────────────────────────────────────────────────
# doctor — diagnostic target for when things are broken and the student is lost.
#
# Run `make doctor` and it walks through every common failure mode and
# prints a one-line pass/fail for each. Designed to be the first thing you
# suggest when someone in Discord says "nothing works".
# ──────────────────────────────────────────────────────────────────────────────
.PHONY: doctor
doctor:
	@echo ''
	@echo '$(MAGENTA)🩺 Sovereign Agent Lab — Setup Doctor$(RESET)'
	@echo ''
	@echo '$(BLUE)Checking your environment...$(RESET)'
	@echo ''
	@# --- uv ---
	@if command -v uv >/dev/null 2>&1; then \
		echo "  $(GREEN)✓$(RESET) uv installed: $$(uv --version 2>/dev/null || echo unknown)"; \
	else \
		echo "  $(RED)✗$(RESET) uv not found"; \
		echo "     Install: $(GREEN)curl -LsSf https://astral.sh/uv/install.sh | sh$(RESET) (Mac/Linux)"; \
		echo "     or:      $(GREEN)powershell -c \"irm https://astral.sh/uv/install.ps1 | iex\"$(RESET) (Windows)"; \
		echo "     Then restart your terminal."; \
	fi
	@# --- make ---
	@if command -v make >/dev/null 2>&1; then \
		echo "  $(GREEN)✓$(RESET) make installed"; \
	else \
		echo "  $(RED)✗$(RESET) make not found (but how are you reading this?)"; \
	fi
	@# --- Git remote ---
	@if git remote get-url upstream >/dev/null 2>&1; then \
		echo "  $(GREEN)✓$(RESET) upstream remote configured ($$(git remote get-url upstream))"; \
	else \
		echo "  $(YELLOW)⚠$(RESET)  upstream remote not configured (needed to pull instructor updates)"; \
		echo "     Add with: $(GREEN)git remote add upstream https://github.com/sovereignagents/sovereign-agent-lab.git$(RESET)"; \
	fi
	@# --- .env ---
	@if [ -f .env ]; then \
		echo "  $(GREEN)✓$(RESET) .env file exists"; \
	else \
		echo "  $(RED)✗$(RESET) .env file is missing"; \
		echo "     Create it with: $(GREEN)cp .env.example .env$(RESET)"; \
	fi
	@# --- .env BOM check ---
	@if [ -f .env ] && head -c 3 .env 2>/dev/null | od -c 2>/dev/null | head -1 | grep -q '357 273 277'; then \
		echo "  $(RED)✗$(RESET) .env has a UTF-8 BOM marker (Windows Notepad artefact)"; \
		echo "     Open .env in VS Code and save as 'UTF-8' (not 'UTF-8 with BOM')"; \
	fi
	@# --- NEBIUS_KEY ---
	@if [ -f .env ]; then \
		key_line=$$(grep -v '^[[:space:]]*#' .env | grep '^[[:space:]]*NEBIUS_KEY[[:space:]]*=' | head -1); \
		if [ -z "$$key_line" ]; then \
			echo "  $(RED)✗$(RESET) NEBIUS_KEY not found in .env"; \
			echo "     Add a line: $(GREEN)NEBIUS_KEY=sk-yourrealkey$(RESET)"; \
		else \
			value=$$(echo "$$key_line" | sed -e 's/^[[:space:]]*NEBIUS_KEY[[:space:]]*=//'); \
			if [ "$$value" = "sk-your-key-here" ]; then \
				echo "  $(RED)✗$(RESET) NEBIUS_KEY is still the placeholder 'sk-your-key-here'"; \
				echo "     Replace it with your real key"; \
			elif echo "$$value" | grep -q '^["'"'"']'; then \
				echo "  $(RED)✗$(RESET) NEBIUS_KEY has quotes around it — remove them"; \
			elif [ -z "$$value" ]; then \
				echo "  $(RED)✗$(RESET) NEBIUS_KEY is empty"; \
			else \
				echo "  $(GREEN)✓$(RESET) NEBIUS_KEY is set (length $$(printf '%s' "$$value" | wc -c | tr -d ' '))"; \
			fi; \
		fi; \
	fi
	@# --- RASA_PRO_LICENSE (warning only) ---
	@if [ -f .env ]; then \
		rasa_line=$$(grep -v '^[[:space:]]*#' .env | grep '^[[:space:]]*RASA_PRO_LICENSE[[:space:]]*=' | head -1); \
		if [ -z "$$rasa_line" ] || echo "$$rasa_line" | grep -q 'your-rasa-pro-licence-key-here'; then \
			echo "  $(YELLOW)⚠$(RESET)  RASA_PRO_LICENSE not set (only needed for Exercise 3)"; \
			echo "     Get a free key: https://rasa.com/rasa-pro-developer-edition-license-key-request"; \
		else \
			echo "  $(GREEN)✓$(RESET) RASA_PRO_LICENSE is set"; \
		fi; \
	fi
	@# --- Main venv ---
	@if [ -d .venv ]; then \
		echo "  $(GREEN)✓$(RESET) Main venv exists (.venv/)"; \
	else \
		echo "  $(YELLOW)⚠$(RESET)  Main venv missing — run: $(GREEN)make install$(RESET)"; \
	fi
	@# --- Rasa venv ---
	@if [ -d $(RASA_DIR)/.venv ]; then \
		echo "  $(GREEN)✓$(RESET) Rasa venv exists ($(RASA_DIR)/.venv/)"; \
	else \
		echo "  $(YELLOW)⚠$(RESET)  Rasa venv missing — run: $(GREEN)make install-rasa$(RESET) (only needed for Ex3)"; \
	fi
	@# --- Python modules importable (only if venv exists) ---
	@if [ -d .venv ]; then \
		if $(UV) run python -c "import sovereign_agent.tools.venue_tools" >/dev/null 2>&1; then \
			echo "  $(GREEN)✓$(RESET) sovereign_agent.tools.venue_tools imports"; \
		else \
			echo "  $(RED)✗$(RESET) sovereign_agent.tools.venue_tools fails to import"; \
			echo "     Try: $(GREEN)make install$(RESET)"; \
		fi; \
		if $(UV) run python -c "import sovereign_agent.agents.research_agent" >/dev/null 2>&1; then \
			echo "  $(GREEN)✓$(RESET) sovereign_agent.agents.research_agent imports"; \
		else \
			echo "  $(RED)✗$(RESET) sovereign_agent.agents.research_agent fails to import"; \
			echo "     Try: $(GREEN)make install$(RESET)"; \
		fi; \
	fi
	@echo ''
	@echo '$(BLUE)Done.$(RESET) If everything above is green, run $(GREEN)make smoke$(RESET) next.'
	@echo 'If something is red, fix it and re-run $(GREEN)make doctor$(RESET).'
	@echo ''
	@echo 'Still stuck? Open a GitHub issue with the full output of this command:'
	@echo '  $(GREEN)https://github.com/sovereignagents/sovereign-agent-lab/issues$(RESET)'
	@echo ''

.PHONY: install
install: check-uv check-env ## Set up main environment (Python 3.14, exercises 1/2/4)
	@echo "$(BLUE)Setting up main environment...$(RESET)"
	$(UV) sync
	@echo "$(GREEN)✓ Main environment ready.$(RESET)"
	@echo "  Python: $(shell uv run python --version 2>/dev/null || echo unknown)"
	@echo "  Run '$(GREEN)make smoke$(RESET)' to verify your API key."

.PHONY: install-rasa
install-rasa: check-uv ## Set up Rasa Pro environment (Python 3.10, Exercise 3 only)
	@echo "$(BLUE)Setting up Rasa Pro environment (Python 3.10 + CALM)...$(RESET)"
	@echo "$(YELLOW)Note: This takes 3–5 minutes the first time — Rasa has many dependencies.$(RESET)"
	cd $(RASA_DIR) && $(UV) sync
	@echo "$(GREEN)✓ Rasa environment ready.$(RESET)"
	@echo "  Rasa version: $(shell cd $(RASA_DIR) && uv run rasa --version 2>/dev/null | head -1 || echo unknown)"
	@echo "  Run '$(GREEN)make ex3-train$(RESET)' to train the model."

# ==============================================================================
# 🔍 Verification
# ==============================================================================
.PHONY: smoke
smoke: check-env ## Verify API connection and key are working
	@echo "$(BLUE)Testing Nebius API connection...$(RESET)"
	$(UV) run python smoke_test.py

.PHONY: test
test: ## Run unit tests — checks your tool implementations (no API calls)
	@echo "$(BLUE)Running tool unit tests...$(RESET)"
	$(UV) run pytest sovereign_agent/tests/test_week1.py -v
	@echo ""
	@echo "$(YELLOW)Fix any failures above before running the exercises.$(RESET)"

# ==============================================================================
# 📝 Exercise 1 — Context Engineering
# ==============================================================================
.PHONY: ex1
ex1: check-env ## Run the context engineering benchmark
	@echo "$(MAGENTA)Exercise 1 — Context Engineering$(RESET)"
	@echo "$(YELLOW)Runs ~2 minutes. Results saved to week1/outputs/ex1_results.json$(RESET)"
	@echo ""
	$(UV) run python week1/exercise1_context.py
	@echo ""
	@echo "$(GREEN)✓ Done. Now fill in week1/answers/ex1_answers.py$(RESET)"

# ==============================================================================
# 🤖 Exercise 2 — LangGraph Research Agent
# ==============================================================================
.PHONY: ex2
ex2: check-env ## Run all Exercise 2 tasks (A, B, C, D)
	@echo "$(MAGENTA)Exercise 2 — LangGraph Research Agent (all tasks)$(RESET)"
	@echo ""
	$(UV) run python week1/exercise2_langgraph.py
	@echo ""
	@echo "$(GREEN)✓ Done. Now fill in week1/answers/ex2_answers.py$(RESET)"

.PHONY: ex2-a
ex2-a: check-env ## Task A — main Edinburgh brief
	@echo "$(MAGENTA)Exercise 2 — Task A: Main Edinburgh Brief$(RESET)"
	@echo ""
	$(UV) run python week1/exercise2_langgraph.py task_a

.PHONY: ex2-b
ex2-b: check-env ## Task B — flyer tool (observe the graceful fallback pattern)
	@echo "$(MAGENTA)Exercise 2 — Task B: Flyer Tool$(RESET)"
	@echo ""
	@echo "$(YELLOW)The flyer tool uses a graceful-fallback pattern (see CHANGELOG.md §Changed).$(RESET)"
	@echo "$(YELLOW)Look for the 'mode' field in the TOOL_RESULT output below — either 'live'$(RESET)"
	@echo "$(YELLOW)or 'placeholder' is a valid result. Record it in ex2_answers.py → TASK_B_MODE.$(RESET)"
	@echo ""
	$(UV) run python week1/exercise2_langgraph.py task_b

.PHONY: ex2-c
ex2-c: check-env ## Task C — failure mode scenarios
	@echo "$(MAGENTA)Exercise 2 — Task C: Failure Modes$(RESET)"
	@echo ""
	$(UV) run python week1/exercise2_langgraph.py task_c

.PHONY: ex2-d
ex2-d: check-env ## Task D — agent graph structure (paste output into mermaid.live)
	@echo "$(MAGENTA)Exercise 2 — Task D: Agent Graph$(RESET)"
	@echo ""
	$(UV) run python week1/exercise2_langgraph.py task_d
	@echo ""
	@echo "$(YELLOW)Paste the Mermaid output above into: https://mermaid.live$(RESET)"

# ==============================================================================
# 🎙️ Exercise 3 — Rasa Confirmation Agent
# ==============================================================================
.PHONY: ex3-train
ex3-train: ## Train the Rasa Pro CALM model (run once, or after pulling fixes)
	@echo "$(MAGENTA)Exercise 3 — Training Rasa Pro CALM model...$(RESET)"
	@if [ -z "$(RASA_PRO_LICENSE)" ]; then \
		echo "$(RED)✗ RASA_PRO_LICENSE not set.$(RESET)"; \
		echo ""; \
		echo "  $(YELLOW)What to do:$(RESET)"; \
		echo "  1. Request a free licence:"; \
		echo "     $(GREEN)https://rasa.com/rasa-pro-developer-edition-license-key-request$(RESET)"; \
		echo "  2. Check your email (and spam folder) for the key"; \
		echo "  3. Add to .env: $(GREEN)RASA_PRO_LICENSE=your-long-key$(RESET)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)This takes about 2 minutes (embedding model download on first run).$(RESET)"
	@echo "$(BLUE)Note: CALM trains much faster than old Rasa — no NLU examples to learn.$(RESET)"
	@echo "$(BLUE)If you pulled the 2026-04-13 fixes, you MUST re-run this target$(RESET)"
	@echo "$(BLUE)to pick up the new endpoints.yml model group.$(RESET)"
	@echo ""
	cd $(RASA_DIR) && $(UV) run rasa train
	@echo ""
	@echo "$(GREEN)✓ Model trained.$(RESET)"
	@echo "  Now open $(GREEN)two$(RESET) terminals:"
	@echo "    Terminal 1: $(GREEN)make ex3-actions$(RESET)"
	@echo "    Terminal 2: $(GREEN)make ex3-chat$(RESET)"

.PHONY: ex3-actions
ex3-actions: ## Terminal 1 — start the action server (keep this running)
	@echo "$(MAGENTA)Exercise 3 — Action Server$(RESET)"
	@echo "$(YELLOW)Keep this terminal open. Start the chat in a second terminal with:$(RESET)"
	@echo "$(YELLOW)  make ex3-chat$(RESET)"
	@echo ""
	cd $(RASA_DIR) && $(UV) run rasa run actions

.PHONY: ex3-chat
ex3-chat: ## Terminal 2 — chat with the Rasa agent (run AFTER ex3-actions is running)
	@echo "$(MAGENTA)Exercise 3 — Rasa Chat$(RESET)"
	@echo "$(YELLOW)Make sure 'make ex3-actions' is running in another terminal first.$(RESET)"
	@echo ""
	@echo "$(BLUE)Conversation scripts to run:$(RESET)"
	@echo "  1. Happy path:     'calling to confirm a booking' → 160 guests → ~50 vegan → £200 deposit"
	@echo "  2. Deposit too high: same flow, but use a deposit above £300"
	@echo "  3. Out of scope:   mid-conversation ask about parking or AV equipment"
	@echo ""
	@echo "$(YELLOW)CALM note: the LLM understands 'about 160 people' or 'one-sixty' as 160.$(RESET)"
	@echo "$(YELLOW)No regex needed — that's the from_llm slot mapping at work.$(RESET)"
	@echo ""
	@echo "$(YELLOW)Copy-paste your terminal output into week1/answers/ex3_answers.py$(RESET)"
	@echo ""
	cd $(RASA_DIR) && $(UV) run rasa shell

.PHONY: ex3-retrain
ex3-retrain: ex3-train ## Alias: retrain after Task B changes or pulling fixes

# ==============================================================================
# 🔌 Exercise 4 — Shared MCP Server
# ==============================================================================
.PHONY: ex4
ex4: check-env ## Run the MCP client (server starts automatically)
	@echo "$(MAGENTA)Exercise 4 — Shared MCP Server$(RESET)"
	@echo ""
	$(UV) run python week1/exercise4_mcp_client.py
	@echo ""
	@echo "$(GREEN)✓ Done. Complete the required experiment, then fill in week1/answers/ex4_answers.py$(RESET)"

# ==============================================================================
# 📊 Grading
# ==============================================================================
.PHONY: grade
grade: ## Run all mechanical checks before submitting
	@echo "$(BLUE)Running mechanical grade checks...$(RESET)"
	@echo ""
	$(UV) run python week1/grade.py
	@echo ""
	@echo "$(YELLOW)Fix every ✗ before submitting.$(RESET)"
	@echo "Warnings (⚠) are advisory — worth reading but not blocking."

.PHONY: grade-ex1
grade-ex1: ## Check Exercise 1 only
	$(UV) run python week1/grade.py ex1

.PHONY: grade-ex2
grade-ex2: ## Check Exercise 2 only
	$(UV) run python week1/grade.py ex2

.PHONY: grade-ex3
grade-ex3: ## Check Exercise 3 only
	$(UV) run python week1/grade.py ex3

.PHONY: grade-ex4
grade-ex4: ## Check Exercise 4 only
	$(UV) run python week1/grade.py ex4

# ==============================================================================
# 🛠️ Development Utilities
# ==============================================================================
.PHONY: lint
lint: ## Check code style with ruff (does not change files)
	@echo "$(BLUE)Checking code style...$(RESET)"
	$(UV) run ruff check sovereign_agent/ week1/
	@echo "$(GREEN)✓ Lint complete.$(RESET)"

.PHONY: lint-fix
lint-fix: ## Auto-fix style issues with ruff
	@echo "$(BLUE)Fixing code style...$(RESET)"
	$(UV) run ruff check --fix sovereign_agent/ week1/
	$(UV) run ruff format sovereign_agent/ week1/

.PHONY: clean
clean: ## Remove build artefacts, caches, and generated output files
	@echo "$(YELLOW)Cleaning up...$(RESET)"
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.egg-info" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name ".ruff_cache" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✓ Clean complete.$(RESET)"

.PHONY: clean-rasa
clean-rasa: ## Remove trained Rasa models (keeps your code — just forces retrain)
	@echo "$(YELLOW)Removing Rasa trained models...$(RESET)"
	rm -rf $(RASA_DIR)/models $(RASA_DIR)/.rasa
	@echo "$(GREEN)✓ Done. Run 'make ex3-train' to retrain.$(RESET)"

.PHONY: clean-outputs
clean-outputs: ## Remove generated output JSON files from week1/outputs/
	@echo "$(YELLOW)Removing exercise output files...$(RESET)"
	rm -f week1/outputs/*.json
	@echo "$(GREEN)✓ Done. Re-run the exercises to regenerate them.$(RESET)"

# ==============================================================================
# 📋 Submission checklist
# ==============================================================================
.PHONY: check-submit
check-submit: test grade ## Run all checks needed before submitting
	@echo ""
	@echo "$(MAGENTA)Submission checklist:$(RESET)"
	@echo ""
	@test -f week1/outputs/ex1_results.json && echo "  $(GREEN)✓$(RESET) ex1_results.json exists" || echo "  $(RED)✗$(RESET) ex1_results.json missing — run: make ex1"
	@test -f week1/outputs/ex2_results.json && echo "  $(GREEN)✓$(RESET) ex2_results.json exists" || echo "  $(RED)✗$(RESET) ex2_results.json missing — run: make ex2"
	@test -f week1/outputs/ex4_results.json && echo "  $(GREEN)✓$(RESET) ex4_results.json exists" || echo "  $(RED)✗$(RESET) ex4_results.json missing — run: make ex4"
	@grep -q "TASK_B_DONE = True" week1/answers/ex3_answers.py 2>/dev/null && \
		echo "  $(GREEN)✓$(RESET) Task B marked done" || \
		echo "  $(RED)✗$(RESET) TASK_B_DONE not True in ex3_answers.py"
	@grep -q "TASK_B_IMPLEMENTED = True" week1/answers/ex2_answers.py 2>/dev/null && \
		echo "  $(GREEN)✓$(RESET) generate_event_flyer marked implemented" || \
		echo "  $(RED)✗$(RESET) TASK_B_IMPLEMENTED not True in ex2_answers.py"
	@echo ""
	@echo "$(YELLOW)If all checks pass, you are ready to submit. Then push to main:$(RESET)"
	@echo "  $(GREEN)git add -A && git commit -m 'week 1 submission' && git push origin main$(RESET)"