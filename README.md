# CrewAI Template

A production-ready template for building AI crews using CrewAI. This template is designed to be easily deployable to AWS ECS/Fargate via ECR.

## Features

- 🚀 Production-ready structure
- 🐳 Docker support out of the box
- 📁 Organized project structure
- 🔧 Easy configuration with YAML
- 🧰 Custom tools support
- 📚 Knowledge base integration
- 🔄 Local development support

## Project Structure

```
.
├── src/
│   └── crewai_template/        # Main package directory
│       ├── __init__.py         # Package initialization
│       ├── main.py             # Application entry point
│       ├── crew.py             # Crew definitions
│       ├── tools/              # Custom tools
│       └── config/             # YAML configurations
├── tests/                      # Test files
├── knowledge/                  # Knowledge base files
├── Dockerfile                  # Container definition
├── docker-compose.yml          # Local development setup
├── pyproject.toml             # Python package configuration
└── .env.example               # Environment variables template
```

### Why This Structure?

This project follows modern Python packaging best practices with the `src/` layout pattern. Here's why:

1. **Package Namespace Protection**:
   - The `src/crewai_template/` structure creates a dedicated namespace for your package
   - Prevents naming conflicts with other installed packages
   - Makes imports explicit and intentional

2. **Development Benefits**:
   - Clear separation between package code and development files
   - Ensures your development environment matches the installed environment
   - Makes it easier to package and distribute your crew

3. **Import Path Clarity**:
   ```python
   # Clear and explicit imports
   from crewai_template.tools import custom_tool
   from crewai_template.config import load_config
   from crewai_template.crew import MyCrew
   ```

4. **Testing Reliability**:
   - Tests are kept separate from package code
   - Prevents accidental inclusion of test files in package
   - Ensures tests run against the installed package

5. **Production Readiness**:
   - Structure supports both local development and containerized deployment
   - Easy to package and deploy to AWS ECS/Fargate
   - Maintains consistency across different environments

## Quick Start

1. Clone this template:
   ```bash
   git clone https://github.com/yourusername/crewai-template.git
   cd crewai-template
   ```

2. Set up your environment:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Run locally:
   ```bash
   # Using Python directly
   pip install ".[tools]"
   python -m crewai_template.main

   # Or using Docker
   docker compose up
   ```

## Development

1. Install development dependencies:
   ```bash
   pip install ".[tools]"
   ```

2. Run tests:
   ```bash
   python -m pytest
   ```

## Docker Support

Build and run using Docker:
```bash
docker build -t crewai_template .
docker run -it --env-file .env crewai_template
```

Or use docker-compose for development:
```bash
docker compose up
```

## Deployment

This template is designed to be easily deployable to AWS ECS/Fargate via ECR. The repository structure and Docker configuration are already set up for cloud deployment.

To prepare for AWS deployment:

1. Build your image
2. Tag it for your ECR repository
3. Push to ECR
4. Deploy to ECS/Fargate

Detailed AWS deployment instructions will be provided in a separate guide.

## Configuration

1. Agent configurations are in `src/crewai_template/config/agents.yaml`
2. Task configurations are in `src/crewai_template/config/tasks.yaml`
3. Environment variables are managed through `.env`

## Adding Custom Tools

1. Create a new tool in `src/crewai_template/tools/`
2. Register it in `src/crewai_template/tools/__init__.py`
3. Use it in your crew configuration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
