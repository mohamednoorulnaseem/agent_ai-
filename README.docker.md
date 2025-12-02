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