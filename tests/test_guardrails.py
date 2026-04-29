"""Unit tests for the guardrail — pure function, no LLM needed."""
from __future__ import annotations

from types import SimpleNamespace

from crewai_template.schemas import ensure_markdown_report


def _output(raw: str):
    return SimpleNamespace(raw=raw)


def test_passes_when_heading_and_long_enough():
    body = "# Title\n" + ("body text " * 30)
    ok, payload = ensure_markdown_report(_output(body))
    assert ok is True
    assert isinstance(payload, str)


def test_fails_without_heading():
    ok, msg = ensure_markdown_report(_output("plain text " * 50))
    assert ok is False
    assert "heading" in msg.lower()


def test_fails_when_too_short():
    ok, msg = ensure_markdown_report(_output("# Tiny"))
    assert ok is False
    assert "too short" in msg.lower()


def test_handles_empty_input():
    ok, msg = ensure_markdown_report(_output(""))
    assert ok is False
    assert "heading" in msg.lower()
