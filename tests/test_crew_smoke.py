"""Smoke test — verifies the crew assembles. Hits a real LLM only with RUN_INTEGRATION=1."""
from __future__ import annotations

import os

import pytest


def test_crew_assembles():
    """Build the crew without kicking off — catches wiring/import regressions."""
    from crewai_template.crew import CrewaiTemplate

    instance = CrewaiTemplate()
    crew = instance.crew()

    assert len(crew.agents) == 3, f"expected 3 agents, got {len(crew.agents)}"
    assert len(crew.tasks) == 3, f"expected 3 tasks, got {len(crew.tasks)}"
    assert crew.memory is True


@pytest.mark.integration
@pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1" or not os.getenv("OPENAI_API_KEY"),
    reason="set RUN_INTEGRATION=1 and OPENAI_API_KEY to run this test",
)
def test_crew_kickoff_produces_report():
    from crewai_template.crew import CrewaiTemplate

    result = CrewaiTemplate().crew().kickoff(inputs={"topic": "OpenCV"})
    assert result is not None
    assert hasattr(result, "raw")
    assert len(result.raw) > 200
