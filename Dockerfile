FROM python:3.13-slim-bookworm AS builder

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod -R 655 /install.sh && /install.sh && rm /install.sh

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY ./pyproject.toml .

RUN uv sync

FROM python:3.13-slim-bookworm AS runtime

RUN useradd --create-home appuser
USER appuser

WORKDIR /app

COPY /src src
COPY --from=builder /app/.venv .venv

ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "src.main:app", "--log-level", "info", "--host", "0.0.0.0" , "--port", "8080"]