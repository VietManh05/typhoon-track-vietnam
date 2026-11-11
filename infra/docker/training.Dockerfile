FROM python:3.11-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
RUN addgroup --system app && adduser --system --ingroup app app
COPY pyproject.toml README.md LICENSE /app/
COPY src /app/src
COPY configs /app/configs
RUN pip install --upgrade pip && pip install ".[train,experiment]"
USER app
VOLUME ["/app/data", "/app/checkpoints", "/app/mlruns"]
CMD ["typhoon-vn", "train", "--config", "configs/phase3_lstm.yaml", "--output-dir", "checkpoints"]
