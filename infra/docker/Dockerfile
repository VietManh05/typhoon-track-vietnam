FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_EXTRA_INDEX_URL=https://download.pytorch.org/whl/cpu

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY src ./src

# [train] brings torch (CPU wheel) and scikit-learn, required to serve the
# trained LSTM bundle and the k-NN analog suggestions.
RUN python -m pip install --upgrade pip \
    && python -m pip install ".[api,train]" \
    && useradd --create-home --uid 10001 app \
    && mkdir -p /app/data /models \
    && chown -R app /app/data

USER app

# Mount artefacts read-only, e.g. -v ./runs/ibtracs-benchmark/bundle:/models/bundle:ro
# and set MODEL_ARTIFACT=/models/bundle (ANALOG_ARTIFACT=/models/analog-wp.npz).
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4)"

CMD ["uvicorn", "typhoon_vn.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
