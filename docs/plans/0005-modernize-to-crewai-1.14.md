# Modernize crewai-template for an Amazing Engineer Onboarding

## Context

This template (last touched July 2025) pins `crewai[tools]>=0.134.0,<1.0.0` and ships a stripped-down onboarding: 2 agents, 2 tasks, 3 hand-rolled tools that **aren't even wired into the agents**, no knowledge sources, no memory, no Flows, no MCP, no guardrails, no observability, no tests. CrewAI hit `1.0` in late 2025 and is now at **`1.14.3` (Apr 24, 2026)** — the entire 1.x feature surface (Flows, knowledge, memory, MCP, EventListeners, guardrails, async, per-agent LLM routing) is missing.

The user wants a template a new engineer can clone on day one and immediately see the canonical, production-shaped patterns of modern crewAI — not a hello-world. Decisions confirmed:
- **Full 15-item showcase** (every must-show feature from the inventory)
- **Sibling Flow example** under `examples/flow/`
- **Multi-provider visible** — default `openai/gpt-4o-mini`, but actively use `anthropic/claude-sonnet-4-5` on one agent so engineers see LiteLLM routing on first read
- **Keep Docker-first**, modernize the existing custom tools, update `.cursorrules` to use `crewai run`

The project is a public template — others fork it via `setup.sh`. So everything needs to be self-contained, parameterized, and not require any cloud accounts beyond `OPENAI_API_KEY` (with `ANTHROPIC_API_KEY` and `SERPER_API_KEY` documented as "set this to enable X").

---

## Final design

### 1. Bump dependencies (`pyproject.toml`)

Replace `crewai[tools]>=0.134.0,<1.0.0` with:

```toml
[project]
requires-python = ">=3.10,<3.14"
dependencies = [
    "crewai[tools]>=1.14,<2",
    "pydantic>=2.11",
    "requests>=2.31.0",
    "beautifulsoup4>=4.12.0",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "pytest-asyncio>=0.24"]

[tool.crewai]
type = "crew"
```

Keep existing entry-point scripts (`run_crew`, `train`, `replay`, `test`) — they're correct; just point at the modernized `main.py`.

### 2. New `crew.py` — the core showcase

Rewrite `src/crewai_template/crew.py` as a **3-agent, 3-task crew** that demonstrates every must-show feature in ~120 lines. Critical files: `src/crewai_template/crew.py`, `src/crewai_template/config/agents.yaml`, `src/crewai_template/config/tasks.yaml`.

What it must contain:

- `@CrewBase` class with `agents_config` / `tasks_config`
- `@before_kickoff` hook that injects `current_year` and a run UUID into inputs
- `@after_kickoff` hook that prints a summary
- 3 `@agent` methods:
  - `researcher` — uses `SerperDevTool()` from `crewai_tools` + custom `WebScraperTool`. Default LLM (env-driven `MODEL`).
  - `analyst` — uses custom `DataAnalyzerTool`. **Per-agent LLM override**: `llm=LLM(model="anthropic/claude-sonnet-4-5", temperature=0.3)` (with a comment: "set ANTHROPIC_API_KEY, or change this line to fall back to OpenAI").
  - `editor` — uses `FileWriteTool()`. `reasoning=True` to demo the planning pass.
- 3 `@task` methods:
  - `research_task` — `async_execution=True` (parallel intra-crew demo)
  - `analysis_task` — `context=[research_task]`, `output_pydantic=AnalysisReport` (Pydantic schema for structured output)
  - `report_task` — `context=[analysis_task]`, `guardrail=ensure_markdown_report` (function guardrail), `guardrail_max_retries=2`, `output_file='report.md'`, `markdown=True`
- `@crew` method:
  - `process=Process.sequential` (with one-line `# Process.hierarchical` comment)
  - `memory=True` with explicit `embedder={"provider":"openai","config":{"model":"text-embedding-3-small"}}`
  - `knowledge_sources=[TextFileKnowledgeSource(file_paths=["company_brief.txt"])]`
  - `verbose=True`
- **Commented MCP block** at the bottom showing `MCPServerAdapter(StdioServerParameters(...))` inside `@CrewBase` — see [MCP overview](https://github.com/crewAIInc/crewAI/blob/main/docs/en/mcp/overview.mdx).

### 3. Pydantic schema + guardrail (`src/crewai_template/schemas.py`, new file)

Small new module — keeps `crew.py` clean.

```python
from pydantic import BaseModel, Field
from crewai import TaskOutput

class KeyFinding(BaseModel):
    title: str
    evidence: str
    confidence: float = Field(ge=0, le=1)

class AnalysisReport(BaseModel):
    topic: str
    findings: list[KeyFinding]
    recommendations: list[str]

def ensure_markdown_report(result: TaskOutput) -> tuple[bool, object]:
    text = result.raw or ""
    if "# " not in text or len(text) < 200:
        return False, "Report must include at least one '# ' heading and be ≥200 chars."
    return True, text
```

### 4. Update YAML configs

`src/crewai_template/config/agents.yaml` — add `goal`/`backstory` for `analyst` and `editor`. Keep `{topic}` interpolation. **Do not** put tools/llm in YAML (those live in `crew.py` so the per-agent LLM override is visible at code level — better onboarding signal than buried YAML).

`src/crewai_template/config/tasks.yaml` — three tasks with `description`, `expected_output`, `agent` fields. Wire `context` and `async_execution` in `crew.py` rather than YAML (more discoverable for engineers reading code).

### 5. Knowledge directory (new)

Create `knowledge/company_brief.txt` with a short fictional company profile (~30 lines: mission, products, recent news). Wired via `TextFileKnowledgeSource(file_paths=["company_brief.txt"])` at the Crew level. Add a one-line README in `knowledge/` explaining the convention.

### 6. Modernize tools (`src/crewai_template/tools/`)

Keep both existing files but **modernize and wire them in**:

- `web_scraper.py` — keep the BeautifulSoup logic (it's good), update imports to `from crewai.tools import BaseTool` (instead of older paths if any), keep Pydantic `args_schema`. This stays as the **`BaseTool` subclass** example.
- `data_analyzer.py` — same treatment. Stays as the second `BaseTool` example.
- `custom_tool.py` — **rewrite as the `@tool` decorator example** (currently it's a stub). Make it a real, useful 5-line tool: `@tool("Word Count") def word_count(text: str) -> int: return len(text.split())`. This shows engineers both tool patterns side by side.
- `__init__.py` — re-export so YAML/code imports stay clean: `from .web_scraper import WebScraperTool`, etc.

Wire all three into `crew.py` agent definitions (`tools=[WebScraperTool(), word_count, SerperDevTool()]`).

### 7. Observability — `EventListener` printout

New file `src/crewai_template/observability.py`:

```python
from crewai.events.event_listener import EventListener
from crewai.events.types.task_events import TaskCompletedEvent, TaskStartedEvent

class ConsoleListener(EventListener):
    def on_task_started(self, e: TaskStartedEvent):
        print(f"▶  {e.task.description[:60]}…")
    def on_task_completed(self, e: TaskCompletedEvent):
        print(f"✓  {e.task.description[:60]}  ({len(e.output.raw)} chars)")

console_listener = ConsoleListener()  # auto-registers on import
```

`main.py` imports this module at top so the listener registers before any kickoff. Mention in `.env.example` that OTEL/Phoenix/Langfuse are commented add-ons.

### 8. Modernized `main.py`

Keep the four entry points (`run`, `train`, `replay`, `test`) — they're the canonical scaffold shape. Update:

- Import `from crewai_template import observability` first (auto-registers listener).
- `run()` — accept topic from `sys.argv[1]` if provided, else default to "OpenCV". Add a comment showing `kickoff_async` and `kickoff_for_each` as alternatives.
- Document `# crewai install / run / train / test / replay / reset-memories` at the top.

### 9. Sibling Flow example (`examples/flow/article_flow.py`, new file)

The "scale up" demo. ~80 lines:

```python
from pydantic import BaseModel
from crewai.flow.flow import Flow, start, listen, router
from crewai_template.crew import CrewaiTemplate

class ArticleState(BaseModel):
    topic: str = "Edge AI"
    research: str = ""
    decision: str = ""

class ArticleFlow(Flow[ArticleState]):
    @start()
    def kickoff(self):
        print(f"Researching: {self.state.topic}")
        result = CrewaiTemplate().crew().kickoff(inputs={"topic": self.state.topic})
        self.state.research = result.raw

    @router(kickoff)
    def gate(self):
        return "publish" if len(self.state.research) > 1000 else "expand"

    @listen("publish")
    def publish(self):
        self.state.decision = "PUBLISHED"
        print(f"✓ {self.state.decision}: report.md ready")

    @listen("expand")
    def expand(self):
        self.state.decision = "NEEDS MORE RESEARCH"
        print(f"⚠ {self.state.decision}")

if __name__ == "__main__":
    ArticleFlow().kickoff()
```

This is the single highest-leverage onboarding artifact: it shows `Flow[State]`, `@start`, `@listen`, `@router`, and **a Crew running inside a Flow step** — the official "production shape."

### 10. Tests (`tests/`, new directory)

Three pytest files (each <40 lines):

- `tests/test_tools.py` — instantiate `WebScraperTool` and `DataAnalyzerTool`, call `_run` directly with mocked `requests.get` (use `unittest.mock`). Tests `@tool`-decorated `word_count` by calling the function directly.
- `tests/test_guardrails.py` — call `ensure_markdown_report` with fake `TaskOutput` objects covering the pass/fail branches.
- `tests/test_crew_smoke.py` — gated by `@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"))`. Builds the crew, asserts agents/tasks count, optionally runs a kickoff if `RUN_INTEGRATION=1`.

Add `pytest` to optional `dev` dependencies (already in step 1).

### 11. Update `examples/business_analysis_example.py`

Already exists and uses the same `CrewaiTemplate` class — it'll work as-is once the new fields land. **One change needed**: it passes inputs the new tasks don't reference (e.g. `industry`, `region`); since the new YAML uses `{topic}` only, those extra inputs are harmless (crewAI ignores unmapped keys), but add a comment in the example saying so.

### 12. `.env.example`

```env
# Required
OPENAI_API_KEY=sk-...
MODEL=openai/gpt-4o-mini

# Recommended (enables web search via SerperDevTool)
SERPER_API_KEY=

# Optional — enables the per-agent Anthropic override on the analyst agent
ANTHROPIC_API_KEY=

# Optional observability (uncomment to enable)
# OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
# PHOENIX_API_KEY=
# LANGFUSE_PUBLIC_KEY=
```

### 13. README rewrite

Top-to-bottom rewrite. Sections:

1. **What you get** (one paragraph: "3 agents, 3 tasks, 1 Flow, 3 tools, knowledge, memory, guardrails, observability — everything in one repo")
2. **Quick start** — 3 commands: `cp .env.example .env && edit`, `docker compose build`, `docker compose run --rm crew crewai run`
3. **The Crew** — diagram of 3 agents → 3 tasks, callouts for the LLM override, knowledge, memory, guardrail
4. **The Flow** — when/why, link to `examples/flow/article_flow.py`
5. **CLI cheatsheet** — `crewai install / run / train / test / replay / reset-memories` (all under `docker compose run --rm crew …`)
6. **Customizing** — point to `setup.sh` and the YAML configs
7. **Production add-ons** — short list pointing at MCP comments, observability env vars, vector knowledge
8. **Learning path** — 4 bullets

### 14. `.cursorrules` update

Replace the older `python -m crewai_template.main` examples with `crewai run`. Add a section "Use the crewAI CLI inside the container — never on the host." Keep the Docker-first ethos. ~20-line edit, not a rewrite.

### 15. `Dockerfile`

One change: add `RUN pip install --no-cache-dir uv` and use `uv sync` is overkill — instead, just keep `pip install -e .` but bump `python:3.12.8-slim` → `python:3.13-slim` and update `CMD` to `["crewai", "run"]` instead of `["python", "-m", "crewai_template.main"]`. Smaller, faster, native CLI shape.

`docker-compose.yml` needs no change.

### 16. `setup.sh`

Two-line update: rename `class CrewaiTemplate` references continue to work, but the script's hardcoded class name pattern needs to also catch the new `ConsoleListener` and `AnalysisReport` references. Audit and update the `sed` patterns. Keep the interactive flow.

---

## Files touched (summary)

**Edit:**
- `pyproject.toml` — bump deps, add dev extras
- `src/crewai_template/crew.py` — full rewrite
- `src/crewai_template/main.py` — minor; import observability, add cli docstrings
- `src/crewai_template/config/agents.yaml` — add 3rd agent
- `src/crewai_template/config/tasks.yaml` — replace with 3 tasks
- `src/crewai_template/tools/custom_tool.py` — rewrite as `@tool` example
- `src/crewai_template/tools/web_scraper.py` — keep, ensure imports current
- `src/crewai_template/tools/data_analyzer.py` — keep, ensure imports current
- `src/crewai_template/tools/__init__.py` — add re-exports
- `Dockerfile` — Python 3.13, `crewai run` as CMD
- `.env.example` — Serper, Anthropic, OTEL keys
- `.cursorrules` — `crewai run` examples
- `README.md` — full rewrite per outline above
- `setup.sh` — audit sed patterns

**Create:**
- `src/crewai_template/schemas.py` — Pydantic models + guardrail
- `src/crewai_template/observability.py` — `ConsoleListener`
- `knowledge/company_brief.txt` — fictional company profile
- `knowledge/README.md` — one paragraph
- `examples/flow/article_flow.py` — sibling Flow example
- `examples/flow/README.md` — when to reach for Flows
- `tests/__init__.py` (empty)
- `tests/test_tools.py`
- `tests/test_guardrails.py`
- `tests/test_crew_smoke.py`

**Untouched:**
- `examples/business_analysis_example.py` (works as-is, comment-only edit)
- `examples/README.md`
- `LICENSE`, `.gitignore`, `.vscode/`, `docker-compose.yml`

---

## Reuse — existing primitives we keep

- `WebScraperTool` (`tools/web_scraper.py`) — solid implementation, just wire it into the `researcher` agent.
- `DataAnalyzerTool` (`tools/data_analyzer.py`) — solid, wire into the `analyst` agent.
- `setup.sh` interactive flow — keep, just audit the `sed` patterns.
- `demo.py` — keep as-is; it already calls `CrewaiTemplate().crew().kickoff(inputs={...})` which still works with the new crew.
- `examples/business_analysis_example.py` — already uses the right API surface.
- `Dockerfile` + `docker-compose.yml` mounting strategy — keep.

---

## Verification plan

After each phase:

1. **Build**: `docker compose build` — confirms `crewai[tools]>=1.14` installs cleanly on Python 3.13.
2. **Smoke**: `docker compose run --rm crew crewai run` with `OPENAI_API_KEY` set — should complete one kickoff, write `report.md`, print `▶`/`✓` lines from the listener.
3. **Knowledge**: temporarily prepend a unique sentinel to `knowledge/company_brief.txt`; the analyst agent's output should reference it (proves knowledge is wired).
4. **Guardrail**: temporarily make `ensure_markdown_report` return `False` always; the report task should retry up to 2× then fail loudly (proves guardrail wiring).
5. **Per-agent LLM**: unset `ANTHROPIC_API_KEY` and confirm a clear error from the analyst agent (proves the override is real, not silently ignored).
6. **Async**: with `verbose=True`, confirm the research task starts before the analysis task awaits it (look for interleaved logs).
7. **Flow**: `docker compose run --rm crew python examples/flow/article_flow.py` — should print the router decision plus the chosen branch.
8. **Tests**: `docker compose run --rm crew pytest -m "not integration"` (offline) and `RUN_INTEGRATION=1 docker compose run --rm crew pytest` (online).
9. **CLI parity**: confirm `docker compose run --rm crew crewai install`, `crewai test -n 1 -m gpt-4o-mini`, `crewai reset-memories --all`, `crewai replay -t <id>` all behave.
10. **Demo unchanged**: `docker compose run --rm crew python demo.py` still works (catches accidental API breakage for existing users forking from main).

---

## Out of scope (explicitly not doing)

- Hierarchical process (mentioned in comments only — extra LLM call per delegation hurts onboarding latency).
- `human_input=True` enabled by default (blocks CI; mention in README only).
- `allow_code_execution=True` (pulls Docker-in-Docker; surprises new users).
- `crewai deploy …` cloud commands (vendor-locked; document in README only).
- Vector-DB knowledge sources (Mem0, Qdrant, Mongo) — out of scope; commented one-liner in README.
- `crewai chat` integration (works automatically via the CLI; nothing to wire).
- Streaming (`stream=True`, `async for chunk`) — mention in README, don't wire.

---

## Source references (for the implementer)

- crewai 1.14.3 release: <https://pypi.org/project/crewai/>
- `@CrewBase` pattern: <https://github.com/crewAIInc/crewAI/blob/main/docs/en/concepts/crews.mdx>
- Flows: <https://github.com/crewAIInc/crewAI/blob/main/docs/en/concepts/flows.mdx>
- Knowledge: <https://github.com/crewAIInc/crewAI/blob/main/docs/en/concepts/knowledge.mdx>
- Memory: <https://github.com/crewAIInc/crewAI/blob/main/docs/en/concepts/memory.mdx>
- Tools: <https://github.com/crewAIInc/crewAI/blob/main/docs/en/concepts/tools.mdx>
- Guardrails (in tasks): <https://github.com/crewAIInc/crewAI/blob/main/docs/en/concepts/tasks.mdx>
- MCP: <https://github.com/crewAIInc/crewAI/blob/main/docs/en/mcp/overview.mdx>
- LLM/LiteLLM: <https://github.com/crewAIInc/crewAI/blob/main/docs/en/learn/llm-selection-guide.mdx>
- CLI: <https://docs.crewai.com/en/concepts/cli>
- Custom tools: <https://github.com/crewAIInc/crewAI/blob/main/docs/en/learn/create-custom-tools.mdx>
