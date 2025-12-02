# Docker (Windows) — Quick Start

Prerequisites:
- Docker Desktop for Windows (enable WSL2 integration recommended)
- Virtualization/WSL2 installed and running

Build & run using `docker compose` (from project root `C:\Users\moham\agent_ai`):

```cmd
cd /d C:\Users\moham\agent_ai
docker compose up --build -d
```

Verify:

```cmd
docker ps
curl http://localhost:8000/
```

Common commands:

- View logs: `docker compose logs -f`
- Stop and remove containers: `docker compose down`
- Rebuild after changes: `docker compose up --build -d`
- Remove dangling images/volumes: `docker image prune -f` and `docker volume prune -f`

Notes:
- The project exposes port `8000` (Uvicorn run via `CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]` in `Dockerfile`).
- On Windows, file-mounted volumes can cause permission and performance differences; if you encounter issues, try running without the source mount or use WSL2 paths.
- A `.dockerignore` file was added to reduce build context size and speed builds.

Files added in this change:
- `.dockerignore` — excludes unnecessary files from Docker build context
- `README.docker.md` — this quick-start doc

Commit message used: `chore(docker): add .dockerignore and README.docker.md`
Docker: Build and run the AI Agent locally

This file explains how to build and run the AI Agent inside Docker for reproducible local testing.

Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Optional: docker compose (Docker Compose v2 is recommended)

Build the Docker image

Windows (cmd.exe):
docker build -t agent-ai:latest .

Linux / macOS:
docker build -t agent-ai:latest .

Run with Docker (single container)

docker run --rm -p 8000:8000 --name agent-ai -v %cd%:/app -v %cd%/data:/app/data agent-ai:latest

On Linux/macOS replace %cd% with $(pwd).

Run with Docker Compose (recommended)

docker compose up --build

Access the API

- Open http://localhost:8000/docs for the Swagger UI
- Health check: http://localhost:8000/health

Notes

- The compose file mounts the repository into the container (useful for fast iteration). For production, consider copying source into the image and not mounting the host directory.
- Persistent SQLite data is mounted to ./data. Ensure the data folder exists and is writable.
