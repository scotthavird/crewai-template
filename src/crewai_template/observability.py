"""Console event listener — prints task start/complete to stdout.

This is the minimal observability hook so engineers see the EventListener
pattern on day one. For production, swap or stack with OpenTelemetry,
Phoenix, Langfuse, or AgentOps (see .env.example for the env vars).
"""
from __future__ import annotations


def _register_listener() -> object | None:
    try:
        from crewai.utilities.events import (
            TaskCompletedEvent,
            TaskStartedEvent,
            crewai_event_bus,
        )
        from crewai.utilities.events.base_event_listener import BaseEventListener
    except ImportError:
        return None

    class ConsoleListener(BaseEventListener):
        def setup_listeners(self, crewai_event_bus) -> None:  # noqa: ARG002 — name fixed by parent class
            @crewai_event_bus.on(TaskStartedEvent)
            def _on_start(_source, event: TaskStartedEvent) -> None:
                desc = getattr(event, "task", None)
                label = (getattr(desc, "description", "") or "")[:60]
                print(f"▶  {label}…", flush=True)

            @crewai_event_bus.on(TaskCompletedEvent)
            def _on_done(_source, event: TaskCompletedEvent) -> None:
                desc = getattr(event, "task", None)
                label = (getattr(desc, "description", "") or "")[:60]
                output = getattr(event, "output", None)
                size = len(getattr(output, "raw", "") or "")
                print(f"✓  {label}  ({size} chars)", flush=True)

    return ConsoleListener()


console_listener = _register_listener()
