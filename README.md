# CrewAI Template

A powerful multi-agent AI system template powered by [crewAI](https://crewai.com), designed for building collaborative AI agent systems.

## Using This Template

1. Click "Use this template" button at the top of this repository
2. Clone your new repository
3. Run the setup script with your project name:
   ```bash
   ./setup_project.sh your_project_name
   ```

   For example:
   ```bash
   ./setup_project.sh my_awesome_project
   ```

   The setup script will:
   - Rename all necessary files and directories
   - Update all references in the codebase
   - Set up basic project metadata
   - Guide you through:
     - Updating project details interactively
     - Editing the README.md file
     - Initializing a git repository
     - Setting up environment (.env) file
     - Configuring OpenAI API key
     - Starting Docker containers
     - Setting up next steps for development

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

## Quick Start

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
- All required dependencies pre-installed
- Isolated environment for consistent development

### Customization
1. Modify `config/agents.yaml` to define your agents
2. Modify `config/tasks.yaml` to define your tasks
3. Create new tools in `src/crewai_template/tools/`
4. Update crew behavior in `crew.py`
5. Modify main execution in `main.py`

## Support
- [CrewAI Documentation](https://docs.crewai.com)
- [CrewAI GitHub](https://github.com/joaomdmoura/crewai)
- [Discord Community](https://discord.com/invite/X4JWnZnxPb)
