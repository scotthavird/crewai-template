# Development Guide

This guide provides detailed information about developing with this CrewAI template.

## Project Structure Explained

```
.
├── src/
│   └── crewai_template/           # Main package directory
│       ├── __init__.py            # Package initialization
│       ├── main.py                # Application entry point
│       ├── crew.py                # Crew definitions
│       ├── tools/                 # Custom tools directory
│       │   ├── __init__.py        # Tools initialization
│       │   └── custom_tool.py     # Custom tool implementations
│       └── config/                # Configuration directory
│           ├── agents.yaml        # Agent definitions
│           └── tasks.yaml         # Task definitions
├── tests/                         # Test directory
│   ├── __init__.py               # Test initialization
│   ├── conftest.py               # Test configurations
│   └── test_*.py                 # Test files
├── knowledge/                     # Knowledge base directory
│   └── user_preference.txt       # User preferences and context
├── Dockerfile                     # Container definition
├── docker-compose.yml            # Local development setup
├── pyproject.toml                # Python package configuration
├── .env.example                  # Environment template
└── README.md                     # Project documentation
```

## Understanding the Structure

### 1. Source Code (`src/`)

The `src/` layout is a Python best practice that provides several benefits:

- **Import Safety**: Prevents accidental imports from the project root
- **Installation Clarity**: Makes it clear what should be included in the package
- **Development/Production Parity**: Ensures development environment matches production

### 2. Package Organization (`crewai_template/`)

The package is organized to support CrewAI's architecture:

- **main.py**: Entry point that sets up and runs the crew
- **crew.py**: Defines the crew structure and relationships
- **tools/**: Custom tools that agents can use
- **config/**: YAML-based configuration for flexibility

### 3. Development Workflow

#### Local Development

1. Set up your environment:
   ```bash
   # Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows

   # Install in editable mode
   pip install -e ".[tools]"
   ```

2. Running the crew:
   ```bash
   # Direct execution
   python -m crewai_template.main

   # Or using the CLI (defined in pyproject.toml)
   crewai_template
   ```

#### Docker Development

1. Build and run:
   ```bash
   docker compose up --build
   ```

2. Development with hot reload:
   ```bash
   # The volume mount in docker-compose.yml enables code changes
   # to be reflected immediately
   docker compose up
   ```

### 4. Adding New Features

#### Adding a New Tool

1. Create a new file in `src/crewai_template/tools/`:
   ```python
   # src/crewai_template/tools/my_tool.py
   from crewai.tools import BaseTool

   class MyTool(BaseTool):
       name: str = "my_tool"
       description: str = "Description of what my tool does"

       def _run(self, input_text: str) -> str:
           # Tool implementation
           return result
   ```

2. Register in `src/crewai_template/tools/__init__.py`:
   ```python
   from .my_tool import MyTool

   __all__ = ["MyTool"]
   ```

#### Adding a New Agent

1. Add agent configuration in `src/crewai_template/config/agents.yaml`:
   ```yaml
   my_agent:
     name: "My Agent"
     role: "Specific role description"
     goal: "Agent's primary goal"
     backstory: "Agent's context and background"
     tools:
       - my_tool
   ```

2. Update crew.py to use the new agent.

## Best Practices

1. **Configuration Management**:
   - Keep sensitive data in `.env`
   - Use YAML for configuration that needs to be human-readable
   - Version control `.env.example` but not `.env`

2. **Testing**:
   - Write tests for all new tools
   - Use pytest fixtures for common setup
   - Mock external API calls in tests

3. **Documentation**:
   - Document all new tools and agents
   - Keep configuration examples up to date
   - Update README.md with new features

4. **Code Style**:
   - Follow PEP 8
   - Use type hints
   - Keep functions and methods focused and small

## Troubleshooting

Common issues and solutions:

1. **Import Errors**:
   - Ensure you're using the correct package name in imports
   - Check that you've installed the package in editable mode
   - Verify PYTHONPATH in your environment

2. **Configuration Issues**:
   - Verify .env file exists and contains required variables
   - Check YAML syntax in configuration files
   - Ensure all referenced tools are properly registered

3. **Docker Issues**:
   - Ensure Docker daemon is running
   - Check volume mounts in docker-compose.yml
   - Verify environment variables are properly passed
