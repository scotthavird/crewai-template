# CrewAI Template

A powerful multi-agent AI system template powered by [crewAI](https://crewai.com), designed for building collaborative AI agent systems.

## Project Structure
```
.
├── src/
│   └── crewai_template/           # Main package
│       ├── main.py                # Entry point
│       ├── crew.py                # Crew definitions
│       ├── tools/                 # Custom tools
│       └── config/                # YAML configurations
├── tests/                         # Test files
├── knowledge/                     # Knowledge base
└── docker/                        # Container files
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
crewai install
```

3. Configure environment:
- Copy `.env.example` to `.env`
- Add your `OPENAI_API_KEY` to `.env`

4. Run the crew:
```bash
crewai run
```

## Development

### Local Setup
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -e ".[tools]"
```

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
- Modify `config/agents.yaml` for agent definitions
- Modify `config/tasks.yaml` for task definitions
- Modify `crew.py` for custom logic and tools
- Modify `main.py` for custom inputs

### Adding New Features

#### New Tool
1. Create tool in `src/crewai_template/tools/`
2. Register in `tools/__init__.py`

#### New Agent
1. Add configuration in `config/agents.yaml`
2. Update `crew.py` accordingly

## Best Practices
- Keep sensitive data in `.env`
- Write tests for new tools
- Follow PEP 8 and use type hints
- Document new features

## Support
- [Documentation](https://docs.crewai.com)
- [GitHub Repository](https://github.com/joaomdmoura/crewai)
- [Discord Community](https://discord.com/invite/X4JWnZnxPb)
- [Documentation Chat](https://chatg.pt/DWjSBZn)
