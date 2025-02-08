#!/usr/bin/env python
import logging
import sys
import warnings
from datetime import datetime

from crewai_template.crew import CrewaiTemplate

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """Run the crew."""
    logger.info("Starting CrewAI Template execution...")
    inputs = {
        'topic': 'openai',
        'current_year': str(datetime.now().year)
    }
    logger.info(f"Running with inputs: {inputs}")
    try:
        result = CrewaiTemplate().crew().kickoff(inputs=inputs)
        logger.info(f"Execution completed with result: {result}")
        return result
    except Exception as e:
        logger.error(f"Execution failed: {e}")
        raise

def train():
    """Train the crew."""
    try:
        CrewaiTemplate().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs={"topic": "AI LLMs"}
        )
    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise

def replay():
    """Replay crew execution."""
    try:
        CrewaiTemplate().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        logger.error(f"Replay failed: {e}")
        raise

def test():
    """Test crew execution."""
    try:
        CrewaiTemplate().crew().test(
            n_iterations=int(sys.argv[1]),
            openai_model_name=sys.argv[2],
            inputs={"topic": "AI LLMs"}
        )
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise

if __name__ == "__main__":
    run()
