FROM python:3.13-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY runner.py ./

# Install dependencies
RUN uv sync

# Create experiments directory
RUN mkdir -p experiments

# Run script every 24 hours
CMD while true; do \
    echo "Running experiment at $(date)"; \
    uv run python runner.py || echo "Experiment failed"; \
    echo "Sleeping for 24 hours..."; \
    sleep 86400; \
done