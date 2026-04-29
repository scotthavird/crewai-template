# crewAI Template

An opinionated, modern starter for **crewAI 1.14+**. Clone, set an API key,
run one command — and you get every canonical pattern an engineer needs to
ship a real multi-agent app.

## What you get

A 3-agent crew, a sibling Flow example, and 3 custom tools — wired together
with the patterns you'd otherwise spend a week stitching from the docs:

|  | Pattern | Where |
|---|---|---|
| 🧩 | `@CrewBase` + YAML config + `@before_kickoff` / `@after_kickoff` | `src/crewai_template/crew.py` |
| 🛣️ | **Flow** with `Flow[State]`, `@start`, `@listen`, `@router` | `examples/flow/article_flow.py` |
| 🛠️ | Custom `BaseTool` subclass **and** `@tool` decorator | `src/crewai_template/tools/` |
| 🔎 | `SerperDevTool` web search wired into the researcher | `crew.py:researcher` |
| 📚 | `TextFileKnowledgeSource` from `knowledge/` with explicit embedder | `crew.py:crew` |
| 🧠 | Crew memory (short-term + long-term + entity + contextual) | `crew.py:crew` |
| 🎯 | **Per-agent LLM right-sizing** — Gemini Flash / Sonnet 4.6 / Opus 4.7 | `crew.py:agents` |
| 🧱 | `output_pydantic=AnalysisReport` structured output | `crew.py:analysis_task` |
| 🛡️ | Function `guardrail=` with retries on the report task | `crew.py:report_task` |
| ⚡ | `async_execution=True` for intra-crew parallelism | `crew.py:research_task` |
| 📡 | Console `EventListener` printing task start/complete | `src/crewai_template/observability.py` |
| 🔌 | Commented MCP block (stdio transport, ready to enable) | `crew.py` (bottom) |
| ✅ | `pytest` suite (tools, guardrails, gated smoke test) | `tests/` |

Everything runs inside Docker so the experience is identical on any machine.

## Quick start

```bash
git clone https://github.com/scotthavird/crewai-template
cd crewai-template
cp .env.example .env
# edit .env — at minimum set OPENAI_API_KEY
docker compose build
docker compose run --rm crew crewai run
```

The first kickoff researches "OpenCV" by default. Pass a topic:

```bash
docker compose run --rm crew crewai run -- "Edge AI in 2026"
```

When it finishes you'll have a `report.md` written by the editor agent, a
`db/` directory holding the long-term memory store, and (if you set
`SERPER_API_KEY`) genuine web-sourced findings.

## The crew

```
   research_task            analysis_task                report_task
  ┌────────────┐  context   ┌────────────┐   context    ┌────────────┐
  │ researcher │ ─────────▶ │  analyst   │ ───────────▶ │   editor   │
  └────────────┘            └────────────┘              └────────────┘
   gemini-2.5-flash         claude-sonnet-4-6            claude-opus-4-7
   SerperDev + scraper      DataAnalyzer (BaseTool)      reasoning=True
   word_count (@tool)       reasoning_effort=medium      output_file
   async_execution=True     output_pydantic=Report       guardrail + retries
```

Each agent's model is **right-sized to its workload**:

- **researcher** — `gemini/gemini-2.5-flash` (cheap, fast, tool-call-heavy).
  Falls back to the env `MODEL` if `GEMINI_API_KEY` is unset.
- **analyst** — `anthropic/claude-sonnet-4-6` with `reasoning_effort="medium"`,
  best-in-class for the `output_pydantic=AnalysisReport` schema-fidelity work.
  Falls back to the env `MODEL` if `ANTHROPIC_API_KEY` is unset.
- **editor** — `anthropic/claude-opus-4-7` (1M context handles the full
  upstream research dump without truncation), `reasoning=True` for a planning
  pass, and a `guardrail=` that retries up to 2× on too-short/unstructured
  output. Falls back to the env `MODEL` if `ANTHROPIC_API_KEY` is unset.

The default `MODEL=openai/gpt-4.1-mini` is the cheap-fast fallback that
keeps the template runnable with only `OPENAI_API_KEY`. Setting
`ANTHROPIC_API_KEY` is the highest-impact upgrade — it activates two of
three agents.

The crew has `memory=True` and a `TextFileKnowledgeSource` pointing at
`knowledge/company_brief.txt` — drop your own docs in there.

## The flow

When a single Crew isn't enough, reach for a **Flow**: deterministic
event-driven topology with structured Pydantic state. The official guidance
is *"start with a Flow, use a Crew within a Flow step when a specific
complex task requires autonomous agents."*

`examples/flow/article_flow.py` shows exactly that — a `Flow[ArticleState]`
that runs the crew, gates on output length, then branches:

```bash
docker compose run --rm crew python examples/flow/article_flow.py
```

## CLI cheatsheet

All commands run **inside the container** (`docker compose run --rm crew …`):

| Command | What it does |
|---|---|
| `crewai install` | `uv sync` the project's deps |
| `crewai run` | Auto-detects crew vs flow from `pyproject.toml` and runs |
| `crewai test -n 3 -m gpt-4o-mini` | LLM-judge eval; prints per-task & avg scores |
| `crewai train -n 5 -f trained.pkl` | HITL training loop |
| `crewai replay -t <task_id>` | Re-run from a stored task |
| `crewai log-tasks-outputs` | Dump last kickoff's task outputs (for replay) |
| `crewai reset-memories --all` | Wipe short/long/entity memory |
| `crewai chat` | Interactive REPL with the crew |
| `crewai flow plot` | Render the flow as an HTML graph |

## Tests

```bash
docker compose run --rm crew pytest                    # tool + guardrail unit tests
RUN_INTEGRATION=1 docker compose run --rm crew pytest  # also hit a real LLM
```

## Customising

Forking this for a new project? Run:

```bash
./setup.sh my_project_name
```

It renames the package, updates imports, and prompts for author / description.
Then customise:

- **Agents & roles** — `src/crewai_template/config/agents.yaml`
- **Tasks & flow** — `src/crewai_template/config/tasks.yaml` (and `crew.py` for `context=`, `async_execution=`)
- **Tools** — drop new `BaseTool` subclasses in `src/crewai_template/tools/` and add to `__init__.py`
- **Knowledge** — drop docs in `knowledge/`, add a `*KnowledgeSource` in `crew.py`

## Production add-ons

These are commented out in the template — flip them on when you need them:

- **MCP servers** — `MCPServerAdapter` block in `crew.py` (stdio / SSE / streamable-HTTP)
- **OpenTelemetry** — uncomment `OTEL_*` in `.env.example`, `pip install openinference-instrumentation-crewai`, register in `observability.py`
- **Phoenix / Langfuse / AgentOps** — env vars listed in `.env.example`
- **External memory** — `Mem0` / `Qdrant Edge` via `crewai.memory.external.external_memory.ExternalMemory`
- **Hierarchical process** — set `process=Process.hierarchical` and `manager_llm=` in `crew.py`
- **`human_input=True`** — add to any `Task` to pause for stdin feedback (don't enable in CI)
- **Code execution** — `Agent(allow_code_execution=True)` (pulls Docker-in-Docker; off by default)

## Learning path

1. **Run it.** `crewai run` and read the console output — see how the listener prints task transitions.
2. **Open `crew.py`.** Every showcased pattern is one click away with a comment explaining why.
3. **Open `examples/flow/article_flow.py`.** This is what production crewAI looks like.
4. **Pin docs:** [Crews](https://docs.crewai.com/concepts/crews) · [Flows](https://docs.crewai.com/concepts/flows) · [Knowledge](https://docs.crewai.com/concepts/knowledge) · [Memory](https://docs.crewai.com/concepts/memory) · [Tools](https://docs.crewai.com/concepts/tools) · [MCP](https://docs.crewai.com/mcp/overview) · [CLI](https://docs.crewai.com/concepts/cli)

---

**License:** MIT (see `LICENSE`).
