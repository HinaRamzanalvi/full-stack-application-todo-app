# Use a single stage build for simplicity since we're using requirements.txt
FROM python:3.11-slim

WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# --- Gunicorn Configuration ---
# Number of workers to run.
# A common formula is (2 * number_of_cores) + 1.
# We'll use an environment variable to set this, defaulting to 3.
ENV GUNICORN_WORKERS=${GUNICORN_WORKERS:-3}

# Port to bind to. Hugging Face provides a PORT env var, defaulting to 7860.
ENV PORT=${PORT:-8000}

# Command to run the application using Gunicorn
# -w: number of workers
# -k: worker class (uvicorn for asyncio)
# -b: bind address
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:${PORT}", "main:app"]
