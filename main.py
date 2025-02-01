from crewai import Agent, Task, Crew
import os
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()

    # Define your agents
    researcher = Agent(
        role='Research Analyst',
        goal='Conduct thorough analysis on given topics',
        backstory='Expert at gathering and analyzing information',
        verbose=True
    )

    writer = Agent(
        role='Content Writer',
        goal='Create engaging and informative content',
        backstory='Experienced writer with expertise in creating clear, compelling content',
        verbose=True
    )

    # Define your tasks
    research_task = Task(
        description="Research the latest developments in AI and automation",
        agent=researcher
    )

    writing_task = Task(
        description="Write a comprehensive summary of the research findings",
        agent=writer
    )

    # Create your crew
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        verbose=2
    )

    # Start the crew
    result = crew.kickoff()
    print("Crew's work result:")
    print(result)

if __name__ == "__main__":
    main()
