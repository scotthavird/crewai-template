#!/usr/bin/env python
"""Entry points for the crewAI CLI.

CLI cheatsheet (run inside the container — `docker compose run --rm crew …`):
    crewai install              # uv sync the project's deps
    crewai run                  # invokes run() below; default topic = OpenCV
    crewai train -n 5 -f t.pkl  # HITL training loop
    crewai test -n 3 -m gpt-4o  # LLM-judge evaluation across N runs
    crewai replay -t <task_id>  # re-run starting from a stored task
    crewai reset-memories --all # wipe short/long/entity memory
    crewai chat                 # interactive REPL with the crew

Don't add business logic here — that belongs in `crew.py`.
"""
from __future__ import annotations

import logging
import sys
import warnings
from datetime import datetime

# Importing this module auto-registers the ConsoleListener event listener.
from crewai_template import observability  # noqa: F401
from crewai_template.crew import CrewaiTemplate

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run() -> object:
    """Run one kickoff. Topic defaults to 'OpenCV', or pass `crewai run -- <topic>`."""
    topic = sys.argv[1] if len(sys.argv) > 1 else "OpenCV"
    inputs = {"topic": topic, "current_year": str(datetime.now().year)}
    logger.info("kickoff inputs: %s", inputs)
    # Alternatives:
    #   await CrewaiTemplate().crew().kickoff_async(inputs=inputs)
    #   CrewaiTemplate().crew().kickoff_for_each([{"topic": t} for t in topics])
    return CrewaiTemplate().crew().kickoff(inputs=inputs)


def train() -> None:
    """`crewai train -n <n> -f <pickle>` — HITL training loop."""
    inputs = {"topic": "AI LLMs"}
    CrewaiTemplate().crew().train(
        n_iterations=int(sys.argv[1]),
        filename=sys.argv[2],
        inputs=inputs,
    )


def replay() -> None:
    """`crewai replay -t <task_id>` — re-run from a stored task. Find IDs with `crewai log-tasks-outputs`."""
    CrewaiTemplate().crew().replay(task_id=sys.argv[1])


def test() -> None:
    """`crewai test -n <n> -m <model>` — LLM-judge eval; prints per-task and avg scores."""
    inputs = {"topic": "AI LLMs"}
    CrewaiTemplate().crew().test(
        n_iterations=int(sys.argv[1]),
        eval_llm=sys.argv[2],
        inputs=inputs,
    )


if __name__ == "__main__":
    run()
