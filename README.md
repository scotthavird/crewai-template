# crewai-template
A template project for building AI agent workflows using CrewAI framework in a Docker container

## About CrewAI
CrewAI is a powerful framework for orchestrating role-playing AI agents. It enables you to create autonomous AI agents that can:
- Work together in a hierarchical structure
- Execute complex tasks through collaboration
- Handle sequential and parallel workflows
- Leverage tools and APIs effectively
- Maintain context and memory throughout tasks



## Pre-requisites

### CrewAI

- [Install CrewAI](https://docs.crewai.com/installation)
This is only needed for running `crewai create crew <project_name>` command
- [Install Cursor](https://www.cursor.com/)
Not required but recommended to use Cursor IDE
- [Install Docker](https://www.docker.com/get-started/)
- Python 3.9+

## Quick Start

1. Clone this repository
2. Run the Docker container:
```sh
docker-compose up --build
```

## Cursor Rules
Rules for AI
While using cursor, we should be using https://docs.cursor.com/context/rules-for-ai.
Learn how to customize AI behavior with global and project-specific rules

## References
- [CrewAI Documentation](https://docs.crewai.com/)
- [CrewAI GitHub Repository](https://github.com/joaomdmoura/crewAI)
- [CrewAI YouTube Channel](https://www.youtube.com/@crewai)
- [CrewAI Discord Community](https://discord.gg/crewai)
- [CrewAI Twitter](https://twitter.com/crewai)

### Github Repos
- [CrewAI GitHub Repository](https://github.com/joaomdmoura/crewAI)
- [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules)

### Youtube
- [CrewAI YouTube Channel](https://www.youtube.com/@crewAIInc)

I want to add this somewhere here. Pretty cool.
```sh
(base) ➜  crewai-template git:(adds-crewai) ✗ crewai create crew crewai_template
Creating folder crewai_template...
Cache expired or not found. Fetching provider data from the web...
Downloading  [####################################]  309058/15326
Select a provider to set up:
1. openai
2. anthropic
3. gemini
4. nvidia_nim
5. groq
6. ollama
7. watson
8. bedrock
9. azure
10. cerebras
11. sambanova
12. other
q. Quit
Enter the number of your choice or 'q' to quit: 1
Select a model to use for Openai:
1. gpt-4
2. gpt-4o
3. gpt-4o-mini
4. o1-mini
5. o1-preview
q. Quit
Enter the number of your choice or 'q' to quit: 3
Enter your OPENAI API key (press Enter to skip): <OPENAI_API_KEY_HERE>
API keys and model saved to .env file
Selected model: gpt-4o-mini
  - Created crewai_template/.gitignore
  - Created crewai_template/pyproject.toml
  - Created crewai_template/README.md
  - Created crewai_template/knowledge/user_preference.txt
  - Created crewai_template/src/crewai_template/__init__.py
  - Created crewai_template/src/crewai_template/main.py
  - Created crewai_template/src/crewai_template/crew.py
  - Created crewai_template/src/crewai_template/tools/custom_tool.py
  - Created crewai_template/src/crewai_template/tools/__init__.py
  - Created crewai_template/src/crewai_template/config/agents.yaml
  - Created crewai_template/src/crewai_template/config/tasks.yaml
Crew crewai_template created successfully!
(base) ➜  crewai-template git:(adds-crewai)
```
