# Dockerfile

# Use a minimal Python image as the base
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    curl libsnappy-dev make gcc g++ libc6-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN pip install uv

# Copy only dependency files first (to leverage caching)
COPY pyproject.toml uv.lock ./

# Make uv work in system's python
ENV UV_PROJECT_ENVIRONMENT=/usr/local

# Install project dependencies using uv
RUN uv sync

# Copy the rest of the application code
COPY ../.. .

# Expose the application port
EXPOSE 8000

# Run the application with uv
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]