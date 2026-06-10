# FastAPI + yt-dlp

A lightweight microservice built with FastAPI and `yt-dlp` to resolve video streaming URLs.

## Key Features

- **Strategy Pattern for Providers**: Separate stream resolvers for YouTube, Twitch, and Pluto TV, managed by a routing coordinator.
- **FastAPI Native Dependency Injection**: Services and repositories are resolved via FastAPI's native dependency injection engine (`Depends`).
- **Structured Logging**: Clean, structured JSON logs outputted directly to standard output.
- **Pydantic Settings**: Centralized configuration management supporting environment variables and `.env` files.
- **Dockerized**: Multistage Docker build for containerization, accompanied by Docker Compose configurations.
- **Tested**: Comprehensive test suite using pytest.

## Installation

Install requirements locally:

```bash
pip install -r requirements.txt
```

## Configuration

Configurations are loaded from environment variables or a `.env` file using Pydantic Settings:

- `CACHE_TTL`: Time-to-live for cache entries in seconds (default: `300`).
- `LOG_LEVEL`: Application logging level (default: `"INFO"`).

## Running the Application

### Locally

Start the development server:

```bash
uvicorn app.main:app --reload
```

### With Docker

Build and run the containerized application:

```bash
docker compose up --build
```

## Deployment to Fly.io

Ensure you have the `flyctl` CLI installed and are authenticated.

To launch the app on Fly.io for the first time:

```bash
fly launch
```

To deploy subsequent updates:

```bash
fly deploy
```

## Deployment to Render

You can deploy the service to [Render](https://render.com) using the included `render.yaml` Blueprint:

1. Connect your repository to Render.
2. Go to **Blueprints** and click **New Blueprint Instance**.
3. Select this repository and click **Approve**.

Alternatively, deploy it as a manual **Web Service** on Render:
- **Runtime**: `Docker`
- **Build Command**: Managed by Render.
- **Start Command**: Managed by `Dockerfile`.

## API Endpoints

- **Health Check**:
  ```http
  GET /health
  ```
  Returns `{"status": "ok"}`.

- **Resolve Stream**:
  ```http
  GET /resolve?url=<url>
  ```
  Resolves the provided URL directly to its highest resolution direct HLS `.m3u8` stream. Supports YouTube, Twitch, and Pluto TV.

## Running Tests

Run the test suite using pytest:

```bash
python3 -m pytest
```
