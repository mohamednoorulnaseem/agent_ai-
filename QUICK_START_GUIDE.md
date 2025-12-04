# Quick Start Guide (5 minutes)

This quick guide helps you get the project running locally in about 5 minutes.

Prerequisites

- Python 3.9+
- Docker (optional for quick Docker run)
- Git

Local (pip) run

```bash
git clone https://github.com/mohamednoorulnaseem/agent_ai-.git
cd agent_ai-
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m src.api
# Open http://localhost:8000 for the API
```

Quick Docker (recommended)

```bash
docker compose up --build -d
# Open http://localhost:8000
```

Further reading

- Full organization: `PHASE_7_INDEX.md`
- Tutorials: `docs/TUTORIALS.md`
- Deployment: `docs/DEPLOYMENT.md`
