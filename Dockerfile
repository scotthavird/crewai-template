FROM python:3.12.8-slim

WORKDIR /app

# Copy only the build files first
COPY pyproject.toml ./

# Install build dependencies and the package
RUN pip install --no-cache-dir ".[tools]"

# Copy the rest of the application
COPY . .

# Run the application
CMD [ "python", "-m", "crewai_template.main" ]
