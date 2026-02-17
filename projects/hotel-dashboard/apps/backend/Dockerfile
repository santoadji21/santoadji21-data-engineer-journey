FROM python:3.11-slim AS base

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir .

COPY app/ ./app/
COPY scripts/ ./scripts/

RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser && \
    mkdir -p /app/data && chown -R appuser:appgroup /app/data

EXPOSE 8000

# --- Seed target: populate DuckDB with mock data ---
FROM base AS seed
CMD ["python", "-m", "scripts.seed_data"]

# --- API target (default): serve the FastAPI app ---
FROM base AS api
USER appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
