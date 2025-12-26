# SADIT Core Dockerfile
# Base Image: Python 3.10 Slim for efficiency and security
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for OpenCV and scientific libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements (derived from environment) or install manually
# For simplicity in this step, we install via pip directly matching environment.yml
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Post-install: Download medical NLP model if needed (simulated for now or generic)
# RUN python -m spacy download en_core_sci_lg

# Copy Source Code
COPY src/ ./src/
COPY data/ ./data/
RUN mkdir -p /app/learning

# Set Python Path
ENV PYTHONPATH="${PYTHONPATH}:/app/src"

# Default Command (Keeps container alive for orchestration)
CMD ["python", "-c", "import time; print('SADIT Core Active'); time.sleep(infinity)"]
