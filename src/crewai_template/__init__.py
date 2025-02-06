"""
CrewAI Template - A template for building AI crews using CrewAI framework.

This package provides a template for creating AI crews that can perform research
and generate reports on AI-related topics.
"""

from crewai_template.crew import CrewaiTemplate
from crewai_template.main import replay, run, test, train

__version__ = "0.1.0"
__author__ = "John Doe"
__all__ = ["CrewaiTemplate", "run", "train", "replay", "test"]
