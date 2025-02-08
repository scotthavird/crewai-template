# CrewAI Template

A production-ready template for building AI crews using CrewAI.

## Quick Start

1. Clone and start the project:
```bash
git clone https://github.com/yourusername/crewai-template.git
cd crewai-template
cp .env.example .env  # Configure your environment variables
docker compose up --build
```

2. After making changes:
   - Changes to `src/`: Run `docker compose up`
   - Changes to dependencies: Run `docker compose up --build`

## Configuration

- Research topic configuration: Edit `src/crewai_template/main.py` in the `run()` function
- Output: Results are written to `report.md`

## Project Structure

```
src/crewai_template/     # Main package directory
├── main.py             # Application entry point and research configuration
├── crew.py            # Crew definitions
├── config/            # YAML configurations for agents and tasks
└── tools/             # Custom tools
```

## Development

- Agent configurations: `src/crewai_template/config/agents.yaml`
- Task configurations: `src/crewai_template/config/tasks.yaml`
- Environment variables: `.env`
