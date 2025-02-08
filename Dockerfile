FROM python:3.12.8-slim as builder

WORKDIR /app

# Copy only dependency-related files
COPY pyproject.toml .

# Create venv and install dependencies all in one layer
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install hatchling && \
    /opt/venv/bin/pip install --upgrade setuptools wheel

# Copy source and install project
COPY src ./src
RUN /opt/venv/bin/pip install -e .

FROM python:3.12.8-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Make sure we use the virtualenv
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH=/app/src:$PYTHONPATH \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=0

# Create output directory with proper permissions
RUN mkdir -p /app/output && \
    chown -R 1000:1000 /app/output && \
    chmod -R 777 /app/output

# Copy application code
COPY . .

CMD ["python", "-m", "crewai_template.main"]
