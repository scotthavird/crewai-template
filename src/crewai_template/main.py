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
    """
    Run the crew.
    """
    logger.info("Starting CrewAI Template execution...")
    inputs = {
        'topic': 'OpenCV',
        'current_year': str(datetime.now().year)
    }
    logger.info(f"Running with inputs: {inputs}")

    try:
        logger.info("Initializing crew...")
        result = CrewaiTemplate().crew().kickoff(inputs=inputs)
        logger.info("Crew execution completed successfully!")
        logger.info(f"Result: {result}")
        return result
    except Exception as e:
        logger.error(f"An error occurred while running the crew: {e}")
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CrewaiTemplate().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CrewaiTemplate().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CrewaiTemplate().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    logger.info("Starting main execution...")
    run()
