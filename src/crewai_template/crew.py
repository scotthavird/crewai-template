"""The crew. Three agents collaborate to research, analyse, and report on a topic.

Showcased patterns (top-to-bottom):
- @CrewBase + YAML config
- @before_kickoff input transformation
- Per-agent LLM override (Anthropic on the analyst)
- BaseTool subclass (WebScraperTool, DataAnalyzerTool) and @tool decorator (word_count)
- SerperDevTool web search wired into the researcher
- async_execution=True on the research task (intra-crew parallelism)
- output_pydantic structured output on the analysis task
- Function guardrail with retries on the report task
- Crew-level memory + knowledge_sources with explicit embedder
- Commented MCP block at the bottom
"""
from __future__ import annotations

import os
import uuid
from datetime import datetime

from crewai import LLM, Agent, Crew, Process, Task
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai.project import CrewBase, after_kickoff, agent, before_kickoff, crew, task
from crewai_tools import SerperDevTool

from crewai_template.schemas import AnalysisReport, ensure_markdown_report
from crewai_template.tools import (
    DataAnalyzerTool,
    WebScraperTool,
    word_count,
)


@CrewBase
class CrewaiTemplate:
    """Research → Analysis → Report crew."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # ── lifecycle ───────────────────────────────────────────────────────
    @before_kickoff
    def _prep(self, inputs: dict) -> dict:
        inputs.setdefault("current_year", str(datetime.now().year))
        inputs.setdefault("run_id", uuid.uuid4().hex[:8])
        return inputs

    @after_kickoff
    def _summarise(self, output):
        print(f"\n— crew finished — wrote {len(getattr(output, 'raw', '') or '')} chars to report.md\n")
        return output

    # ── agents ──────────────────────────────────────────────────────────
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],  # type: ignore[index]
            tools=[SerperDevTool(), WebScraperTool(), word_count],
            verbose=True,
        )

    @agent
    def analyst(self) -> Agent:
        # Per-agent LLM override demonstrates LiteLLM provider routing.
        # Set ANTHROPIC_API_KEY to enable, or swap for `openai/gpt-4o` to fall back.
        analyst_llm = (
            LLM(model="anthropic/claude-sonnet-4-5", temperature=0.3)
            if os.getenv("ANTHROPIC_API_KEY")
            else None  # falls back to MODEL env var (default openai/gpt-4o-mini)
        )
        return Agent(
            config=self.agents_config["analyst"],  # type: ignore[index]
            tools=[DataAnalyzerTool()],
            llm=analyst_llm,
            verbose=True,
        )

    @agent
    def editor(self) -> Agent:
        # No tools — the editor's `report_task` writes to disk via `output_file`.
        # `reasoning=True` adds a planning pass before execution.
        return Agent(
            config=self.agents_config["editor"],  # type: ignore[index]
            reasoning=True,
            verbose=True,
        )

    # ── tasks ───────────────────────────────────────────────────────────
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],  # type: ignore[index]
            async_execution=True,
        )

    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["analysis_task"],  # type: ignore[index]
            context=[self.research_task()],
            output_pydantic=AnalysisReport,
        )

    @task
    def report_task(self) -> Task:
        return Task(
            config=self.tasks_config["report_task"],  # type: ignore[index]
            context=[self.analysis_task()],
            guardrail=ensure_markdown_report,
            guardrail_max_retries=2,  # type: ignore[call-arg] — accepted by crewai 1.14 runtime; type stubs lag
            output_file="report.md",
            markdown=True,
        )

    # ── crew ────────────────────────────────────────────────────────────
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # type: ignore[attr-defined] — populated by @CrewBase
            tasks=self.tasks,    # type: ignore[attr-defined] — populated by @CrewBase
            process=Process.sequential,
            # process=Process.hierarchical,  # requires manager_llm; costs +1 LLM call per delegation
            memory=True,
            embedder={
                "provider": "openai",
                "config": {"model": "text-embedding-3-small"},
            },
            knowledge_sources=[
                TextFileKnowledgeSource(file_paths=["company_brief.txt"]),
            ],
            verbose=True,
        )


# ── MCP integration (uncomment to enable) ────────────────────────────────
# Pull tools from any MCP server (stdio, SSE, or streamable HTTP) and pass
# them into an agent. Three transports, same adapter:
#
# from crewai_tools import MCPServerAdapter
# from mcp import StdioServerParameters
#
# server_params = StdioServerParameters(
#     command="uvx",
#     args=["pubmedmcp@0.1.3"],
#     env={**os.environ},
# )
# with MCPServerAdapter(server_params) as mcp_tools:
#     researcher = Agent(role="…", goal="…", backstory="…", tools=mcp_tools)
#
# See https://docs.crewai.com/mcp/overview for SSE / streamable-HTTP examples
# and the `mcp_server_params = [...]` class attribute for declarative wiring.
