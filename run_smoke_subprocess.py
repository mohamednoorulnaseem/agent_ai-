"""Start uvicorn in a subprocess, run smoke HTTP tests, then terminate the subprocess."""

import subprocess
import sys
import time
import urllib.request

proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "api:app", "--port", "8000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
try:
    # Wait for server to start
    start = time.time()
    started = False
    while time.time() - start < 20:
        try:
            with urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=1) as r:
                print("/health ->", r.status, r.read(200).decode(errors="ignore")[:200])
                started = True
                break
        except Exception:
            time.sleep(0.25)

    if not started:
        print("Server failed to start within timeout")
        raise SystemExit(1)

    urls = ["/docs", "/openapi.json", "/health", "/plans"]
    for ep in urls:
        url = f"http://127.0.0.1:8000{ep}"
        try:
            with urllib.request.urlopen(url, timeout=3) as r:
                data = r.read(2000)
                print(f"{ep} -> {r.status}, {len(data)} bytes")
        except Exception as e:
            print(f"{ep} -> ERROR: {e}")

finally:
    # Terminate server
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except Exception:
        proc.kill()
    print("Server process terminated")
