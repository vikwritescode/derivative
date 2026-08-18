FROM python:3.11-slim AS base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DB_PATH=/data/debates.db \
    MODEL_ARTIFACT_DIR=/artifacts

COPY requirements.txt ./requirements.txt

# --no-deps skips the resolver backtracking loop entirely
RUN python -m pip install --upgrade pip && \
    python -m pip install \
    --no-deps \
    --timeout 120 \
    --retries 3 \
    -r requirements.txt && \
    python -m pip check

COPY src ./src
COPY whitelist.json ./whitelist.json


FROM base AS train

WORKDIR /app/src

CMD ["python", "-m", "ai.train_model"]


FROM base AS serve

WORKDIR /app/src

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]