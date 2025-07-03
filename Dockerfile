# Use official Python 3.12.9 slim base image
FROM python:3.12.9-slim

# Set working directory
WORKDIR /app

# Install dependencies for pip and requests (SSL, DNS)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python project files
COPY . /app

# Install Python dependencies (assumes you have requirements.txt)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Run the module
CMD ["python", "-m", "homeip.main"]
