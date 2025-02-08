#!/bin/bash

# Set proper locale for handling UTF-8 characters
export LC_ALL=C
export LANG=C

# Check if a project name was provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 your_project_name"
    echo "Example: $0 my_awesome_project"
    exit 1
fi

PROJECT_NAME=$1
PROJECT_NAME_PASCAL=$(echo "$PROJECT_NAME" | perl -pe 's/(^|_)./uc($&)/ge;s/_//g')

echo "🚀 Setting up your project: $PROJECT_NAME"

# Rename files and directories
echo "📁 Renaming directories..."
if [ -d "src/crewai_template" ]; then
    mv src/crewai_template "src/$PROJECT_NAME"
fi

# Replace occurrences in files
echo "📝 Updating file contents..."
find . -type f -not -path '*/\.*' -not -path '*/venv/*' -not -name 'setup.sh' -exec sed -i.bak "s/crewai_template/$PROJECT_NAME/g" {} +
find . -type f -not -path '*/\.*' -not -path '*/venv/*' -not -name 'setup.sh' -exec sed -i.bak "s/CrewaiTemplate/$PROJECT_NAME_PASCAL/g" {} +

# Update README.md with project details
echo "📝 Updating README.md..."
if [ -f "README.md" ]; then
    # Update title only
    sed -i.bak "s/# CrewAiTemplate/# $PROJECT_NAME_PASCAL/" README.md

    # If project description was provided, update it in README
    if [ ! -z "$PROJECT_DESCRIPTION" ]; then
        sed -i.bak "2a\\\\n$PROJECT_DESCRIPTION\\n" README.md
    fi
fi

# Clean up backup files
find . -name "*.bak" -type f -delete

# Update pyproject.toml with basic info
echo "📦 Updating project metadata..."
sed -i.bak "s/name = \"crew_ai_template\"/name = \"$PROJECT_NAME\"/" pyproject.toml
sed -i.bak "s/CrewAiTemplate/$PROJECT_NAME_PASCAL/" pyproject.toml
rm pyproject.toml.bak

echo "✨ Initial setup complete!"
echo

# Interactive project details update
echo "📝 Let's update your project details:"
echo

read -p "Enter project description (press Enter to skip): " PROJECT_DESCRIPTION
if [ ! -z "$PROJECT_DESCRIPTION" ]; then
    sed -i.bak "s/description = \".*\"/description = \"$PROJECT_DESCRIPTION\"/" pyproject.toml
    rm pyproject.toml.bak
fi

echo "Enter author details:"
read -p "Name (press Enter to skip): " AUTHOR_NAME
read -p "Email (press Enter to skip): " AUTHOR_EMAIL

if [ ! -z "$AUTHOR_NAME" ] || [ ! -z "$AUTHOR_EMAIL" ]; then
    if [ -z "$AUTHOR_EMAIL" ]; then
        sed -i.bak "s/authors = \[.*\]/authors = [{ name = \"$AUTHOR_NAME\" }]/" pyproject.toml
    elif [ -z "$AUTHOR_NAME" ]; then
        sed -i.bak "s/authors = \[.*\]/authors = [{ email = \"$AUTHOR_EMAIL\" }]/" pyproject.toml
    else
        sed -i.bak "s/authors = \[.*\]/authors = [{ name = \"$AUTHOR_NAME\", email = \"$AUTHOR_EMAIL\" }]/" pyproject.toml
    fi
    rm pyproject.toml.bak
fi

# Prompt for README update
echo
echo "📚 Would you like to update the README.md now? (y/N)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]; then
    if command -v nano >/dev/null 2>&1; then
        nano README.md
    elif command -v vim >/dev/null 2>&1; then
        vim README.md
    else
        echo "Please manually edit README.md with your preferred editor"
    fi
fi

echo
echo "🎉 Setup complete! Your project is ready to go!"
echo
echo "Next steps:"
echo "1. Review pyproject.toml if you need to make additional changes"
echo "2. Copy .env.example to .env and add your API keys"
echo "3. Start developing your AI crew!"

# Environment Setup
echo
echo "📄 Would you like to set up your environment file now? (y/N)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Created .env file"

        echo "Would you like to add your OpenAI API key now? (y/N)"
        read -r api_response
        if [[ "$api_response" =~ ^([yY][eE][sS]|[yY])+$ ]]; then
            read -p "Enter your OpenAI API key: " API_KEY
            if [ ! -z "$API_KEY" ]; then
                sed -i.bak "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$API_KEY/" .env
                rm .env.bak
                echo "✅ API key added to .env"
            fi
        else
            echo "⚠️ Remember to add your API key to .env before running the project"
        fi
    else
        echo "❌ .env.example not found!"
    fi
fi

# Prompt to start Docker
echo
echo "🐳 Would you like to start the Docker container now? (y/N)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]; then
    if ! command -v docker >/dev/null 2>&1; then
        echo "❌ Docker is not installed. Please install Docker first."
    else
        if [ -f "docker-compose.yml" ]; then
            echo "🚀 Starting Docker containers..."
            docker compose up --build
        else
            echo "❌ docker-compose.yml not found!"
        fi
    fi
fi
