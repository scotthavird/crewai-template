FROM python:3.12.8-slim

WORKDIR /app

# Copy only files needed for installing dependencies
COPY pyproject.toml .
COPY src ./src

# Configure Python environment
ENV PYTHONPATH=/app/src:$PYTHONPATH \
    PYTHONUNBUFFERED=1

# Install dependencies
RUN pip install --no-cache-dir hatchling && \
    pip install --no-cache-dir -e .

# Copy the rest of the project files
COPY . .

CMD ["python", "-m", "crewai_template.main"]
