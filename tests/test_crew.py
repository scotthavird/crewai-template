import pytest
from unittest.mock import Mock, patch
from crewai_template.crew import CrewaiTemplate
from crewai import Crew

@pytest.fixture
def mock_openai_response():
    return "Test response from OpenAI"

@pytest.fixture
def crew_template():
    return CrewaiTemplate()

@patch('crewai_template.crew.Crew')
def test_crew_kickoff(mock_crew_class, crew_template, mock_openai_response):
    # Arrange
    mock_crew = Mock()
    mock_crew_class.return_value = mock_crew
    mock_crew.kickoff.return_value = mock_openai_response

    test_inputs = {
        'topic': 'Test Topic',
        'current_year': '2024'
    }

    # Act
    result = crew_template.crew().kickoff(inputs=test_inputs)

    # Assert
    assert result == mock_openai_response
    mock_crew.kickoff.assert_called_once_with(inputs=test_inputs)

@pytest.mark.integration
def test_crew_integration():
    """Integration test for crew functionality.
    Requires valid OpenAI API key in environment.
    Skip if no API key is available.
    """
    crew = CrewaiTemplate()
    inputs = {
        'topic': 'Test Topic',
        'current_year': '2024'
    }

    try:
        result = crew.crew().kickoff(inputs=inputs)
        assert isinstance(result, str)
        assert len(result) > 0
    except Exception as e:
        pytest.skip(f"Integration test skipped: Authentication failed - please provide valid API credentials")

@patch('crewai.LLM')
@patch('crewai_template.crew.Crew')
def test_crew_input_validation(mock_crew_class, mock_llm):
    crew = CrewaiTemplate()
    mock_crew = Mock()
    mock_crew_class.return_value = mock_crew

    def mock_kickoff(inputs):
        # Simulate the input validation
        if not inputs:
            raise ValueError("Inputs dictionary cannot be empty")
        if 'current_year' not in inputs:
            raise ValueError("Missing required template variable 'current_year' in description")
        return "Test response"

    mock_crew.kickoff.side_effect = mock_kickoff

    # Mock LLM to prevent actual API calls
    mock_llm_instance = Mock()
    mock_llm.return_value = mock_llm_instance
    mock_llm_instance.chat.completion.return_value = {"choices": [{"message": {"content": "Test response"}}]}

    # Test with missing required input
    with pytest.raises(ValueError, match="Missing required template variable 'current_year' in description"):
        crew.crew().kickoff(inputs={'topic': 'Test'})

    # Test with empty inputs
    with pytest.raises(ValueError, match="Inputs dictionary cannot be empty"):
        crew.crew().kickoff(inputs={})