# -------------------------------
# Stage 1: Build dependencies
# -------------------------------
FROM python:3.12.9-slim AS builder

WORKDIR /build

# Install build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only the current directory contents (homeip package)
COPY . /build/homeip

# Install Python deps into /install
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r /build/homeip/requirements.txt

# -------------------------------
# Stage 2: Final runtime image
# -------------------------------
FROM python:3.12.9-slim

RUN useradd -r -u 10001 -m appuser
WORKDIR /app

# Copy deps and code
COPY --from=builder /install /usr/local/
COPY --from=builder /build/homeip /app/homeip

USER appuser

# Ensure the parent directory is in PYTHONPATH so `homeip.main` is resolvable
ENV PYTHONPATH=/app

CMD ["python", "-m", "homeip.main"]
