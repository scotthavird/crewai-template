FROM python:3.12.8-slim

WORKDIR /app

# Copy the application
COPY . .

# Set Python path to include src directory and ensure output is not buffered
ENV PYTHONPATH=/app/src:$PYTHONPATH
ENV PYTHONUNBUFFERED=1

# Install build dependencies and project dependencies
RUN pip install --no-cache-dir hatchling && \
    pip install --no-cache-dir -e .

# Run the application
CMD ["python", "-m", "crewai_template.main"]
