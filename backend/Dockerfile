# Use Python 3.11 as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including ffmpeg and supervisor
RUN apt-get update && apt-get install -y \
    ffmpeg \
    supervisor \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install poetry and add it to PATH
ENV PATH="/root/.local/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Copy the package
COPY src ./src

# Configure poetry to not create virtual environment (we're in a container)
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-interaction --no-ansi

# Copy the rest of the application
COPY alembic.ini .
COPY alembic ./alembic

# Create directory for uploaded files
RUN mkdir -p uploaded_audio_files

# Setup supervisord configuration
RUN mkdir -p /etc/supervisor/conf.d
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy production env file
COPY deploy/env .env

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Create entrypoint script
RUN echo '#!/bin/sh\n\
# Run migrations\n\
poetry run alembic upgrade head\n\
# Start supervisord\n\
/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf\n\
' > /entrypoint.sh && chmod +x /entrypoint.sh

# Expose the port your application runs on
EXPOSE 8000

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]