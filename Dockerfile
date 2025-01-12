# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for serial communication
RUN apt-get update && apt-get install -y \
    gcc \
    libudev-dev \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry

# Copy only the files needed for dependency installation
COPY pyproject.toml poetry.lock* ./

# Configure poetry to not create a virtual environment inside the container
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the application
COPY . .

# Create log directory
RUN mkdir -p log

# Set environment variables
ENV DEBUG=false

# Run the application
ENTRYPOINT ["poetry", "run", "python", "main.py"]
