# =============================================================================
# Backend Dockerfile - FastAPI Development
# =============================================================================
# This Dockerfile creates a development environment for the FastAPI backend.
# It uses uv package manager and enables hot reload via uvicorn.
#
# Build: docker build -t todo-backend .
# Run: docker run -p 8000:8000 -v $(pwd):/app todo-backend
#
# Note: This is a DEVELOPMENT Dockerfile. For production, use multi-stage build.
# =============================================================================

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy dependency files
COPY pyproject.toml ./

# Install Python dependencies using uv
# Note: This will be updated when dependencies are added to pyproject.toml
RUN uv pip install --system fastapi uvicorn sqlmodel pyjwt python-dotenv

# Copy source code
# Note: In docker-compose, source is mounted as volume for hot reload
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Set Python environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Start Uvicorn with hot reload
# Note: --reload enables auto-restart on code changes
# Note: --host 0.0.0.0 allows external connections from docker network
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
