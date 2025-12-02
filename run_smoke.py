"""Start the API server programmatically, run smoke tests, then shut it down.

This script will:
- Start uvicorn server for `api:app` on 127.0.0.1:8000
- Poll `/health` until available
- Request: `/docs`, `/openapi.json`, `/health`, `/plans`
- Print simple summary for each
"""

import asyncio
import time
import urllib.request
import urllib.error
from uvicorn import Config, Server


async def run():
    config = Config("api:app", host="127.0.0.1", port=8000, log_level="info")
    server = Server(config)

    # Start server in background
    server_task = asyncio.create_task(server.serve())

    # Wait for server to accept connections
    start = time.time()
    healthy = False
    # Allow more time for startup on slower machines
    while time.time() - start < 30:
        try:
            with urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=1) as r:
                body = r.read(1024).decode(errors="ignore")
                print("/health ->", r.status, body[:200])
                healthy = True
                break
        except Exception:
            await asyncio.sleep(0.25)

    if not healthy:
        print("Server did not start within timeout")
        server.should_exit = True
        await server_task
        return

    # Endpoints to test
    endpoints = ["/docs", "/openapi.json", "/health", "/plans"]
    for ep in endpoints:
        url = f"http://127.0.0.1:8000{ep}"
        try:
            with urllib.request.urlopen(url, timeout=3) as r:
                data = r.read(2000)
                print(f"{ep} -> {r.status}, {len(data)} bytes")
        except urllib.error.HTTPError as he:
            print(f"{ep} -> HTTP {he.code}: {he.reason}")
        except Exception as e:
            print(f"{ep} -> ERROR: {e}")

    # Shutdown server
    server.should_exit = True
    await server_task


if __name__ == "__main__":
    asyncio.run(run())
