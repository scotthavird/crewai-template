import pytest
import os
from pathlib import Path

@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment variables."""
    os.environ['MODEL_NAME'] = 'gpt-4'
    yield
    # Cleanup after tests
    os.environ.pop('MODEL_NAME', None)

@pytest.fixture
def test_knowledge_dir():
    """Fixture to provide test knowledge directory."""
    return Path(__file__).parent / 'test_knowledge'

@pytest.fixture(autouse=True)
def setup_test_knowledge_dir(test_knowledge_dir):
    """Create and cleanup test knowledge directory."""
    test_knowledge_dir.mkdir(exist_ok=True)
    yield
    # Cleanup test files after tests
    if test_knowledge_dir.exists():
        for file in test_knowledge_dir.glob('*'):
            file.unlink()
        test_knowledge_dir.rmdir()