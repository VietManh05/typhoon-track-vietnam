FROM python:3.11-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
RUN addgroup --system app && adduser --system --ingroup app app
COPY pyproject.toml README.md LICENSE /app/
COPY src /app/src
COPY alembic.ini /app/
RUN pip install --upgrade pip && pip install -e ".[api,train,ingestion]"
USER app
HEALTHCHECK --interval=60s --timeout=5s --retries=3 CMD python -c "import typhoon_vn; print(typhoon_vn.__version__)"
CMD ["python", "-m", "typhoon_vn.operations.worker"]
