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

- [Install Docker](https://www.docker.com/get-started/)
- Python 3.9+

## Quick Start

1. Clone this repository
2. Run the Docker container:
```sh
docker-compose up --build
```

## Project Structure
```
crewai-template/
├── agents/         # Define your AI agents here
├── tasks/          # Define tasks for your agents
├── tools/          # Custom tools for agents
└── workflows/      # Orchestrate your agent workflows
```

## Key Features
- 🤖 Easy agent creation and configuration
- 🔄 Flexible workflow management
- 🛠️ Extensible tool integration
- 🧠 Built-in memory and context management
- 🐳 Dockerized environment for easy deployment

## Resources
- [CrewAI Documentation](https://docs.crewai.com/)
- [CrewAI GitHub Repository](https://github.com/joaomdmoura/crewAI)