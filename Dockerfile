# syntax=docker/dockerfile:1

# Use an explicit Python base image and name the stage `base` so later
# stages that reference `base` won't be resolved from a registry.
FROM python:3.12-slim AS base
ARG PIP_NO_CACHE_DIR=1
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# Install minimal system deps (if needed for some wheels). Keep layers small.
RUN apt-get update \
	&& apt-get install -y --no-install-recommends build-essential gcc libffi-dev \
	&& rm -rf /var/lib/apt/lists/*

# Build Python wheels in a separate stage to keep runtime image small.
FROM base AS deps
COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install --upgrade pip \
 && pip wheel --no-cache-dir --no-deps -r /tmp/requirements.txt -w /wheels

FROM base AS runtime
# Create a non-root user and ensure permissions for /app
RUN useradd -m app && chown -R app:app /app

# Create data directory and set ownership so the app can write the SQLite file
RUN mkdir -p /data && chown -R app:app /data

ENV DB_PATH=/data/app.db

# Copy wheels from the deps stage and install them
COPY --from=deps /wheels /wheels
RUN pip install --no-cache-dir /wheels/* \
 && rm -rf /wheels

# Copy application code (ensure the `app/` directory exists in build context)
COPY --chown=app:app app/ /app/

USER app
EXPOSE 8080
ENV PORT=8080
ENTRYPOINT ["uvicorn","main:app","--host","0.0.0.0","--port","8080"]
