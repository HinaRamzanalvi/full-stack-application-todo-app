# --- Stage 1: Build Stage ---
# We use a full Python image to build our dependencies,
# as some packages might need a compiler.
FROM python:3.11 as builder

WORKDIR /usr/src/app

# Install poetry for robust dependency management
# Using a specific version for reproducible builds
ENV POETRY_VERSION=1.8.2
RUN pip install "poetry==$POETRY_VERSION"

# Copy only the files needed for dependency installation
COPY backend/pyproject.toml backend/poetry.lock* ./

# Install dependencies using poetry
# --no-dev: Don't install development dependencies
# --no-interaction: Don't ask any interactive questions
# --no-ansi: Don't output ANSI color codes
RUN poetry install --no-dev --no-interaction --no-ansi


# --- Stage 2: Final Stage ---
# We use a slim image for the final container to reduce its size.
FROM python:3.11-slim

WORKDIR /usr/src/app

# Copy the virtual environment from the builder stage
COPY --from=builder /usr/src/app/.venv ./.venv

# Set the PATH to include the virtual environment's bin directory
ENV PATH="/usr/src/app/.venv/bin:$PATH"

# Copy the application code
COPY backend/ ./

# --- Gunicorn Configuration ---
# Number of workers to run.
# A common formula is (2 * number_of_cores) + 1.
# We'll use an environment variable to set this, defaulting to 3.
ENV GUNICORN_WORKERS=${GUNICORN_WORKERS:-3}

# Port to bind to. Hugging Face provides a PORT env var, defaulting to 7860.
ENV PORT=${PORT:-7860}

# Command to run the application using Gunicorn
# -w: number of workers
# -k: worker class (uvicorn for asyncio)
# -b: bind address
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:7860", "main:app"]
