"""Sibling Flow example: when you outgrow a single Crew.

Flows give you deterministic, event-driven topology with structured state.
Crews live *inside* flow steps when you need autonomous multi-agent behavior
on a chunk of work.

Official guidance: "For any production-ready application, start with a Flow
to define the overall structure, state, and logic. Use a Crew within a Flow
step when a specific complex task requires autonomous agents."
— https://docs.crewai.com/concepts/flows

Run inside Docker:
    docker compose run --rm crew python examples/flow/article_flow.py
"""
from __future__ import annotations

from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, router, start

from crewai_template.crew import CrewaiTemplate


class ArticleState(BaseModel):
    topic: str = "Edge AI"
    research: str = ""
    decision: str = ""


class ArticleFlow(Flow[ArticleState]):
    """Run the crew, gate on output length, branch to publish or expand."""

    @start()
    def run_research(self) -> None:
        print(f"→ researching: {self.state.topic}")
        result = CrewaiTemplate().crew().kickoff(inputs={"topic": self.state.topic})
        self.state.research = getattr(result, "raw", "") or str(result)

    @router(run_research)
    def gate(self) -> str:
        return "publish" if len(self.state.research) > 1000 else "expand"

    @listen("publish")
    def publish(self) -> None:
        self.state.decision = "PUBLISHED"
        print(f"✓ {self.state.decision} — see report.md ({len(self.state.research)} chars)")

    @listen("expand")
    def expand(self) -> None:
        self.state.decision = "NEEDS MORE RESEARCH"
        print(f"⚠ {self.state.decision} — only {len(self.state.research)} chars from research")


def kickoff() -> ArticleFlow:
    flow = ArticleFlow()
    flow.kickoff()
    return flow


def plot() -> None:
    """`crewai flow plot` calls this — renders the flow as an HTML graph."""
    ArticleFlow().plot()


if __name__ == "__main__":
    kickoff()
