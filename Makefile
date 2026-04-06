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
	@echo '$(YELLOW)Self-check (no API calls needed):$(RESET)'
	@echo '  $(GREEN)make test$(RESET)               Run tool unit tests — fix failures before exercises'
	@echo ''
	@echo '$(YELLOW)Exercise 1 — Context Engineering:$(RESET)'
	@echo '  $(GREEN)make ex1$(RESET)                Run the benchmark and save results'
	@echo ''
	@echo '$(YELLOW)Exercise 2 — LangGraph Research Agent:$(RESET)'
	@echo '  $(GREEN)make ex2$(RESET)                Run all tasks'
	@echo '  $(GREEN)make ex2-a$(RESET)              Task A — main Edinburgh brief'
	@echo '  $(GREEN)make ex2-b$(RESET)              Task B — flyer tool (implement TODO first)'
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
# 🚀 Setup
# ==============================================================================
.PHONY: check-uv
check-uv:
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "$(RED)✗ uv not found.$(RESET)"; \
		echo "  Install it with:"; \
		echo "    $(GREEN)curl -LsSf https://astral.sh/uv/install.sh | sh$(RESET)  (Mac/Linux)"; \
		echo "    $(GREEN)powershell -c \"irm https://astral.sh/uv/install.ps1 | iex\"$(RESET)  (Windows)"; \
		echo "  Then restart your terminal and try again."; \
		exit 1; \
	fi
	@echo "$(GREEN)✓ uv found: $(shell uv --version)$(RESET)"

.PHONY: check-env
check-env:
	@if [ ! -f .env ]; then \
		echo "$(RED)✗ .env file not found.$(RESET)"; \
		echo "  Run: $(GREEN)cp .env.example .env$(RESET)"; \
		echo "  Then open .env and paste your NEBIUS_KEY."; \
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
	@echo "$(GREEN)✓ .env file found$(RESET)"

.PHONY: install
install: check-uv check-env ## Set up main environment (Python 3.14, exercises 1/2/4)
	@echo "$(BLUE)Setting up main environment...$(RESET)"
	$(UV) sync
	@echo "$(GREEN)✓ Main environment ready.$(RESET)"
	@echo "  Python: $(shell uv run python --version)"
	@echo "  Run '$(GREEN)make smoke$(RESET)' to verify your API key."

.PHONY: install-rasa
install-rasa: check-uv ## Set up Rasa Pro environment (Python 3.10, Exercise 3 only)
	@echo "$(BLUE)Setting up Rasa Pro environment (Python 3.10 + CALM)...$(RESET)"
	@echo "$(YELLOW)Note: This takes 3–5 minutes the first time — Rasa has many dependencies.$(RESET)"
	cd $(RASA_DIR) && $(UV) sync
	@echo "$(GREEN)✓ Rasa environment ready.$(RESET)"
	@echo "  Rasa version: $(shell cd $(RASA_DIR) && uv run rasa --version | head -1)"
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
ex2-b: check-env ## Task B — flyer tool (implement the TODO in venue_tools.py first)
	@echo "$(MAGENTA)Exercise 2 — Task B: Flyer Tool$(RESET)"
	@echo ""
	@echo "$(YELLOW)Have you implemented generate_event_flyer in sovereign_agent/tools/venue_tools.py?$(RESET)"
	@echo "$(YELLOW)Look for the '# ── TODO' block and replace the stub.$(RESET)"
	@echo ""
	$(UV) run python week1/exercise2_langgraph.py task_b

.PHONY: ex2-c
ex2-c: check-env ## Task C — failure mode scenarios
	@echo "$(MAGENTA)Exercise 2 — Task C: Failure Modes$(RESET)"
	@echo ""
	$(UV) run python week1/exercise2_langgraph.py task_c

.PHONY: ex2-d
ex2-d: ## Task D — agent graph structure (paste output into mermaid.live)
	@echo "$(MAGENTA)Exercise 2 — Task D: Agent Graph$(RESET)"
	@echo ""
	$(UV) run python week1/exercise2_langgraph.py task_d
	@echo ""
	@echo "$(YELLOW)Paste the Mermaid output above into: https://mermaid.live$(RESET)"

# ==============================================================================
# 🎙️ Exercise 3 — Rasa Confirmation Agent
# ==============================================================================
.PHONY: ex3-train
ex3-train: ## Train the Rasa Pro CALM model (run once, or after changing .yml files)
	@echo "$(MAGENTA)Exercise 3 — Training Rasa Pro CALM model...$(RESET)"
	@if [ -z "$(RASA_PRO_LICENSE)" ]; then \
		echo "$(RED)✗ RASA_PRO_LICENSE not set.$(RESET)"; \
		echo "  Add it to your .env file. Your instructor will provide the licence key."; \
		exit 1; \
	fi
	@echo "$(YELLOW)This takes about 2 minutes (embedding model download on first run).$(RESET)"
	@echo "$(BLUE)Note: CALM trains much faster than old Rasa — no NLU examples to learn.$(RESET)"
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
ex3-retrain: ex3-train ## Alias: retrain after Task B changes (same as ex3-train)

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
	@echo "$(YELLOW)If all checks pass, you are ready to submit.$(RESET)"
