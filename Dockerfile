FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirement.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Copy application code
COPY . .

# Create input and output directories
RUN mkdir -p input output

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "main.py"] 