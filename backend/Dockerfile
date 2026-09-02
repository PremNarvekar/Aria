# Build stage: compile dependencies and install packages
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build dependencies only in builder stage
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install all Python dependencies into a wheel directory for efficiency
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt

# Runtime stage: minimal production image
FROM python:3.12-slim

# Create non-root user for security
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy only wheels from builder, install without caching
COPY --from=builder /build/wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt && \
    rm -rf /wheels

# Install runtime-only packages
RUN pip install --no-cache-dir celery redis alembic

# Copy application code
COPY . /app

# Fix permissions
RUN chown -R appuser:appuser /app
USER appuser

# Healthcheck — lightweight check that Python and app module load correctly.
# Works for both API (uvicorn) and Worker (celery) containers.
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import backend.main" || exit 1

# Runtime commands via docker-compose.yml (uvicorn or celery)
