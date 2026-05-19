# ── Stage 1: dependency install ──────────────────────────────────────────────
# Use a full Python image so we can compile any C extensions (FAISS, numpy).
FROM python:3.13-slim AS builder

WORKDIR /app

# Install system libs needed to build faiss-cpu and sentence-transformers
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# --no-cache-dir keeps the image smaller; wheels go into /app/wheels for the next stage
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Stage 2: runtime image ────────────────────────────────────────────────────
FROM python:3.13-slim AS runtime

WORKDIR /app

# Copy only the installed packages from the builder — no compiler toolchain in prod
COPY --from=builder /install /usr/local

# Copy application source
COPY . .

# The sentence-transformers model is downloaded at runtime on first request
# unless you pre-cache it. Set this env var to control the local cache path.
ENV TRANSFORMERS_CACHE=/app/.cache/huggingface
ENV HF_HOME=/app/.cache/huggingface
# Required: all intra-package imports in app/ are bare names (e.g. "from api.router import …").
# Adding app/ to sys.path lets Python resolve them when uvicorn is launched as "app.main:app".
ENV PYTHONPATH=/app/app

# Expose the port uvicorn will bind to
EXPOSE 8000

# Run the server; reload=False in production
CMD ["sh", "-c", "python scripts/download_models.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
