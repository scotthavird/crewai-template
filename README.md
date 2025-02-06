# CrewAI Template

A powerful multi-agent AI system template powered by [crewAI](https://crewai.com), designed for building collaborative AI agent systems.

## Using This Template

1. Click "Use this template" button at the top of this repository
2. Clone your new repository
3. Rename the template to your project name:
   ```bash
   # Replace 'your_project_name' with your desired name
   find . -type f -not -path '*/\.*' -exec sed -i '' 's/crewai_template/your_project_name/g' {} +
   find . -type f -not -path '*/\.*' -exec sed -i '' 's/CrewaiTemplate/YourProjectName/g' {} +
   mv src/crewai_template src/your_project_name
   ```
4. Update project details in `pyproject.toml`
5. Update this README.md with your project's details

## Project Structure
```
.
├── src/
│   └── your_project_name/        # Main package
│       ├── main.py              # Entry point
│       ├── crew.py             # Crew definitions
│       ├── config/             # Configuration files
│       │   ├── agents.yaml     # Agent definitions
│       │   └── tasks.yaml      # Task definitions
│       └── tools/              # Custom tools
├── tests/                      # Test files
├── Dockerfile                  # Docker container definition
└── docker-compose.yml         # Docker compose configuration
```

## Requirements
- Python >=3.10 <3.13
- [UV](https://docs.astral.sh/uv/) for dependency management

## Quick Start

1. Install UV:
```bash
pip install uv
```

2. Install dependencies:
```bash
uv pip install -e ".[dev]"
```

3. Configure environment:
- Copy `.env.example` to `.env`
- Add your `OPENAI_API_KEY` to `.env`

4. Run the crew:
```bash
python -m your_project_name.main
```

## Development

### Docker Setup
```bash
# Build and start the containers
docker compose up --build

# Run in detached mode
docker compose up -d

# View logs
docker compose logs -f

# Stop containers
docker compose down
```

The Docker setup includes:
- Hot reload for development
- All required dependencies pre-installed
- Isolated environment for consistent development

### Customization
1. Modify `config/agents.yaml` to define your agents
2. Modify `config/tasks.yaml` to define your tasks
3. Create new tools in `src/your_project_name/tools/`
4. Update crew behavior in `crew.py`
5. Modify main execution in `main.py`

## Best Practices
- Keep sensitive data in `.env`
- Write tests for new tools
- Follow PEP 8 and use type hints
- Document new features

## Support
- [CrewAI Documentation](https://docs.crewai.com)
- [CrewAI GitHub](https://github.com/joaomdmoura/crewai)
- [Discord Community](https://discord.com/invite/X4JWnZnxPb)
