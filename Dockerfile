FROM python:3.13-slim AS builder

RUN pip install --upgrade pip && pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv venv && uv sync

FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

COPY ./src/jarvis ./jarvis

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 80

CMD ["uvicorn", "jarvis.main:app", "--host", "0.0.0.0", "--port", "8080"]
