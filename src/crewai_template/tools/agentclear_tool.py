"""
AgentClear tool for CrewAI — dynamic API discovery and execution.

Lets your agents find and call external APIs by describing what they need.
Install: pip install agentclear crewai-tools
Docs: https://agentclear.dev/docs
"""
import os
from typing import Optional, Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

try:
    from agentclear import AgentClear
    _AVAILABLE = True
except ImportError:
    _AVAILABLE = False


class AgentClearDiscoverInput(BaseModel):
    """Input schema for the AgentClear discovery tool."""
    query: str = Field(
        ...,
        description="Natural language description of the API service you need "
                    "(e.g., 'extract tables from a PDF', 'translate text to Spanish')"
    )
    payload: dict = Field(
        default_factory=dict,
        description="Data to send to the discovered service"
    )


class AgentClearDiscoverTool(BaseTool):
    """
    Discover and call external API services using AgentClear.

    Use this when you need an external API but don't have a specific tool for it.
    Describe what you need in natural language and this tool will find and call
    the best matching service from 60+ available APIs.
    """
    name: str = "agentclear_discover"
    description: str = (
        "Find and call external API services by describing what you need. "
        "Supports PDF extraction, image generation, web scraping, data enrichment, "
        "translation, and 60+ other services. Automatic micropayment billing."
    )
    args_schema: Type[BaseModel] = AgentClearDiscoverInput

    def _run(self, query: str, payload: dict = None) -> str:
        if not _AVAILABLE:
            return "Error: agentclear not installed. Run: pip install agentclear"

        api_key = os.getenv("AGENTCLEAR_API_KEY")
        if not api_key:
            return "Error: AGENTCLEAR_API_KEY not set in environment"

        client = AgentClear(api_key=api_key)

        # Discover matching services
        results = client.discover(query=query, max_results=3, min_trust_tier="basic")
        if not results:
            return f"No services found matching: {query}"

        # Call the best match
        best = results[0]
        response = client.proxy(service_id=best.id, body=payload or {})

        return (
            f"Service: {best.name} (trust: {best.trust_tier})\n"
            f"Cost: ${response.cost}\n"
            f"Result: {response.data}"
        )
