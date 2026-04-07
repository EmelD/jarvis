FROM python:3.13-slim AS base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app


FROM base AS builder
RUN pip install --upgrade pip && pip install uv
COPY pyproject.toml uv.lock ./
RUN uv venv && uv sync --frozen --no-dev


FROM base AS agent
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY src/jarvis ./jarvis
EXPOSE 80
CMD ["uvicorn", "jarvis.main:app", "--host", "0.0.0.0", "--port", "80"]


FROM base AS bot
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY src/jarvis ./jarvis
CMD ["python", "-m", "jarvis.bot.main"]


FROM base AS calendar_mcp
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY src/jarvis ./jarvis
CMD ["uvicorn", "jarvis.apps.google_calendar.app:app", "--host", "0.0.0.0", "--port", "80"]


FROM base AS todoist_mcp
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY src/jarvis ./jarvis
CMD ["uvicorn", "jarvis.apps.todoist.app:app", "--host", "0.0.0.0", "--port", "80"]
