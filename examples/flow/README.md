# Flow example

A **Flow** is the deterministic, event-driven outer skeleton for production
crewAI apps. It pairs Pydantic-typed state with `@start` / `@listen` /
`@router` decorators so you can express branching, retries, and HITL gates
that a single Crew can't.

`article_flow.py` shows:

- `Flow[ArticleState]` — typed state via a Pydantic `BaseModel`.
- `@start()` — the entry method; runs the existing `CrewaiTemplate` crew
  inside the flow step.
- `@router(start_method)` — branches to one of N labels based on state.
- `@listen("label")` — fires when an upstream method emits the matching label.

**Why this matters:** the official guidance is "start with a Flow, use a Crew
within a Flow step when a specific complex task requires autonomous agents."
This file demonstrates exactly that shape.

## Run

```bash
docker compose run --rm crew python examples/flow/article_flow.py
```

## Plot

Render the flow as an interactive HTML graph:

```bash
docker compose run --rm crew crewai flow plot
```

## Going further

- **Parallel branches**: `@listen(and_(a, b))` joins; `@listen(or_(a, b))` first-wins.
- **HITL inside flows**: `@human_feedback(message=…, emit=["approved", "rejected"])`.
- **Streaming**: `flow.kickoff_async()` returns an awaitable streaming object.
- **Persistence**: 1.14 ships flow checkpointing — see `crewai checkpoint --help`.

Docs: <https://docs.crewai.com/concepts/flows>
