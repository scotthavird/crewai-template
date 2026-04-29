from typing import Tuple

from pydantic import BaseModel, Field


class KeyFinding(BaseModel):
    title: str = Field(..., description="Headline of the finding.")
    evidence: str = Field(..., description="Supporting evidence or citation.")
    confidence: float = Field(ge=0, le=1, description="0.0–1.0 confidence score.")


class AnalysisReport(BaseModel):
    topic: str
    findings: list[KeyFinding]
    recommendations: list[str]


def ensure_markdown_report(result) -> Tuple[bool, str]:
    text = (getattr(result, "raw", None) or str(result)) or ""
    if "# " not in text:
        return False, "Report must include at least one '# ' markdown heading."
    if len(text) < 200:
        return False, f"Report is too short ({len(text)} chars). Expand to ≥200 chars."
    return True, text
