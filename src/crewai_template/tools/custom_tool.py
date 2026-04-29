"""Lightweight `@tool` decorator examples.

Two custom-tool patterns ship with this template:

1. **`@tool` decorator** (this file) — tiny, function-style. Pick this when
   the tool is a one-liner with no shared state.
2. **`BaseTool` subclass** — see `web_scraper.py` and `data_analyzer.py`.
   Pick this when you want a Pydantic `args_schema`, instance state, or
   reusable helper methods.

The plain `_word_count` / `_character_count` callables are kept exported so
unit tests can call them directly without the decorator wrapper in the way.
"""
from crewai.tools import tool


def _word_count(text: str) -> int:
    return len(text.split())


def _character_count(text: str) -> int:
    return len(text)


@tool("Word Count")
def word_count(text: str) -> int:
    """Count whitespace-separated words in `text`."""
    return _word_count(text)


@tool("Character Count")
def character_count(text: str) -> int:
    """Count characters (including whitespace) in `text`."""
    return _character_count(text)
