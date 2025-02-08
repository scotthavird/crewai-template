# CrewAI Template

A production-ready template for building AI crews using CrewAI.

## Quick Start

1. Clone the template:
```bash
git clone https://github.com/yourusername/crewai-template.git
cd crewai-template
```

2. Set up your project:
```bash
./setup.sh your_project_name
# Example: ./setup.sh research_crew
```

3. Configure and start:
```bash
docker compose up --build
```

4. After making changes:
   - Changes to `src/`: Run `docker compose up`
   - Changes to dependencies: Run `docker compose up --build`

## Configuration

- Research topic configuration: Edit `src/your_project_name/main.py` in the `run()` function
- Output: Results are written to `report.md`

## Project Structure

```
src/your_project_name/  # Main package directory
├── main.py             # Application entry point and research configuration
├── crew.py            # Crew definitions
├── config/            # YAML configurations for agents and tasks
└── tools/             # Custom tools
```

## Development

- Agent configurations: `src/your_project_name/config/agents.yaml`
- Task configurations: `src/your_project_name/config/tasks.yaml`
- Environment variables: `.env`
