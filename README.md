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

| Variable | Description | Default |
|---|---|---|
| `CACHE_TTL` | Cache entry lifetime in seconds | `300` |
| `LOG_LEVEL` | Application log level | `INFO` |
| `COOKIES_FILE` | Absolute path to a Netscape cookies file | `None` |

## YouTube Cookies

YouTube may return a **"Sign in to confirm you're not a bot"** error when accessed without authentication. The solution is to provide a cookies file exported from a browser session where you are already logged into YouTube.

### Exporting Cookies

Use the [cookies.txt browser extension](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp) to export your YouTube cookies in Netscape format.

### Locally (with Docker Compose)

Place the exported file at `cookies/cookies.txt` in the project root. The `docker-compose.yml` will mount it automatically:

```bash
mkdir cookies
cp ~/Downloads/cookies.txt cookies/cookies.txt
docker compose up --build
```

The `COOKIES_FILE` env var is pre-configured to `/cookies/cookies.txt` inside the container.

### On Render

1. In the Render dashboard, go to your service → **Secret Files**.
2. Create a secret file with the path `/etc/secrets/cookies.txt` and paste your cookies content.
3. In **Environment**, set `COOKIES_FILE` = `/etc/secrets/cookies.txt`.

> [!IMPORTANT]
> Make sure `COOKIES_FILE` points to the Secret File path (`/etc/secrets/cookies.txt`), not to `/tmp/`. The service copies the file to `/tmp/` internally at startup — you should never set `COOKIES_FILE=/tmp/...` directly.

> [!NOTE]
> If the file is not found at the configured path, the service will start normally and log a warning. YouTube videos that require authentication will still return a bot-check error until a valid cookies file is provided.

### On Fly.io

1. Store the cookies file using a persistent volume and mount it at `/cookies/cookies.txt`.
2. Set the `COOKIES_FILE` environment variable:
   ```bash
   fly secrets set COOKIES_FILE=/cookies/cookies.txt
   ```

> [!NOTE]
> The `cookies/` directory is already listed in `.gitignore` to prevent credentials from being committed to the repository.

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

```bash
fly launch   # first time
fly deploy   # subsequent updates
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
  Resolves the provided URL directly to its highest resolution HLS `.m3u8` stream. Supports YouTube, Twitch, and Pluto TV.

## Running Tests

```bash
python3 -m pytest
```
