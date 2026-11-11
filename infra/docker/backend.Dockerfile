FROM python:3.11-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /app
RUN addgroup --system app && adduser --system --ingroup app app
COPY pyproject.toml README.md LICENSE /app/
COPY src /app/src
COPY alembic.ini /app/
RUN pip install --upgrade pip \
    && pip install 'torch>=2.4,<3' --index-url https://download.pytorch.org/whl/cpu \
    && pip install -e ".[api,train]" \
    && mkdir -p /app/data/operational && chown -R app:app /app/data
USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3).read()"
CMD ["uvicorn", "typhoon_vn.api.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
