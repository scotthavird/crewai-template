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

The project includes optimized Docker support with intelligent caching for faster development:

```bash
# First time setup or when dependencies change:
docker compose build

# For normal development (recommended for daily work):
docker compose up
```

### Build Behavior

- `docker compose up` - Starts the container without rebuilding (recommended)
  - Use this for most development work
  - Source code changes in src/ are reflected immediately via volume mounting
  - Knowledge base changes are reflected immediately
  - Much faster than using --build

- `docker compose build` - Rebuilds the container (only needed when):
  - Dockerfile changes
  - pyproject.toml dependencies change
  - You want to force a clean build

❗ Avoid using `docker compose up --build` for regular development:
- It forces unnecessary rebuilds
- Slows down your development cycle
- Ignores the caching optimizations we've set up

### Docker Configuration

The project uses an optimized Docker setup:
- Efficient dependency caching through staged builds
- Smart volume mounting for development:
  - `./src:/app/src` - Live code updates
  - `./knowledge:/app/knowledge` - Live knowledge base updates
- Proper Python path configuration
- Immediate code change reflection without rebuilds

### Troubleshooting

If you encounter module not found errors:
```bash
# Clean up and rebuild from scratch
docker compose down
docker compose build --no-cache
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
