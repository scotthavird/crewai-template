"""Unit tests for the custom tools — call `_run` directly with mocked I/O."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

from crewai_template.tools import (
    DataAnalyzerTool,
    WebScraperTool,
)
from crewai_template.tools.custom_tool import (
    _character_count,
    _word_count,
)


def test_word_count_basic():
    assert _word_count("the quick brown fox") == 4
    assert _word_count("") == 0


def test_character_count_basic():
    assert _character_count("hello") == 5
    assert _character_count("") == 0


def test_web_scraper_extracts_text():
    fake_html = b"<html><body><p>Hello world</p><script>x=1</script></body></html>"
    fake_response = MagicMock(content=fake_html, raise_for_status=lambda: None)

    with (
        patch("crewai_template.tools.web_scraper.requests.get", return_value=fake_response),
        patch("crewai_template.tools.web_scraper.time.sleep"),
    ):
        result = WebScraperTool()._run(url="https://example.com", max_content_length=1000)

    assert "Hello world" in result
    assert "x=1" not in result


def test_web_scraper_handles_request_failure():
    import requests

    with (
        patch(
            "crewai_template.tools.web_scraper.requests.get",
            side_effect=requests.RequestException("boom"),
        ),
        patch("crewai_template.tools.web_scraper.time.sleep"),
    ):
        result = WebScraperTool()._run(url="https://example.com")

    assert "Failed to scrape" in result


def test_data_analyzer_summary_on_text():
    result = DataAnalyzerTool()._run(data="Hello world. This is a test.", analysis_type="summary")
    assert "Word Count" in result
    assert "Summary" in result
