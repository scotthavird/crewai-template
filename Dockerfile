FROM python:3.13-slim

WORKDIR /app

# Build deps for native wheels (chromadb, lxml-style packages crewai pulls in)
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
COPY src ./src
COPY knowledge ./knowledge
COPY README.md ./

RUN pip install --no-cache-dir hatchling \
    && pip install --no-cache-dir -e ".[dev]"

# Bring in the rest (examples, tests, demo, configs)
COPY . .

ENV PYTHONPATH=/app/src:$PYTHONPATH
ENV PYTHONUNBUFFERED=1

CMD ["crewai", "run"]
