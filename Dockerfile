FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim AS runner
WORKDIR /app

# Install Deno (recommended runtime per yt-dlp docs, min 2.3.0)
RUN apt-get update && apt-get install -y --no-install-recommends curl unzip ca-certificates \
    && curl -fsSL https://deno.land/install.sh | sh \
    && apt-get purge -y curl unzip && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

ENV DENO_INSTALL="/root/.deno"
ENV PATH="${DENO_INSTALL}/bin:$PATH"

COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]