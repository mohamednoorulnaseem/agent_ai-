# 🚀 Deployment Guide - Agent AI Framework

**Status**: ✅ **LIVE IN DOCKER**  
**Date**: December 4, 2025  
**API URL**: http://localhost:8000  
**API Docs**: http://localhost:8000/docs  

---

## 🎯 Quick Start - 5 Minutes

### 1. Prerequisites
- Docker Desktop installed and running
- Python 3.11+ (for local development)
- Git for version control

### 2. Deploy Locally with Docker

```bash
# Start the application
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs agent-ai --follow

# Stop the application
docker-compose down
```

### 3. Verify API is Running

```bash
# Health check
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","llm_provider":"mock","version":"0.2.0"}

# View interactive API documentation
# Open browser: http://localhost:8000/docs
```

---

## 📋 Configuration

### Environment Variables

The `.env` file contains configuration for:

```env
# LLM Configuration
LLM_PROVIDER=mock          # or: ollama, openai_like
LLM_MODEL=mock-model
LLM_TEMPERATURE=0.0

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_CORS_ENABLED=true

# Database Configuration
DB_TYPE=sqlite
DB_PATH=./data/agent.db

# Security
JWT_SECRET_KEY=dev-secret-key-change-in-production
AUTH_ENABLED=false

# Advanced Features
AGENT_DEBUG=true
CACHE_ENABLED=true
CACHE_TTL=3600
```

### Docker Compose Setup

**Development** (default):
- Single FastAPI container running on port 8000
- SQLite database (local storage)
- Health checks enabled
- Logs available via `docker-compose logs`

**Production** (docker-compose.prod.yml):
- PostgreSQL database with persistence
- Redis cache service
- Prometheus metrics collection
- Grafana dashboards
- Jaeger distributed tracing
- Nginx reverse proxy with SSL
- Complete monitoring stack

---

## 🛠️ Development Workflow

### Local Development (No Docker)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app locally
python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000

# 3. Access the API
# http://localhost:8000/docs  (Interactive API docs)
# http://localhost:8000/health (Health endpoint)
```

### Docker Development

```bash
# 1. Build image
docker-compose build

# 2. Start containers
docker-compose up -d

# 3. View real-time logs
docker-compose logs -f agent-ai

# 4. Execute commands in container
docker exec agent-ai python verify_setup.py

# 5. Stop and clean up
docker-compose down -v
```

---

## 📊 API Endpoints

### Health & Status
- `GET /health` - Health check endpoint
- `GET /metrics` - Prometheus metrics
- `GET /status` - Current system status

### Agent Operations
- `POST /agent/plan` - Create execution plan
- `POST /agent/execute` - Execute task
- `GET /agent/history` - Get conversation history
- `POST /agent/clear-history` - Clear history

### Webhook Management
- `POST /webhooks` - Create webhook
- `GET /webhooks` - List webhooks
- `DELETE /webhooks/{id}` - Delete webhook

### Repository Operations
- `POST /repo/scan` - Scan repository
- `POST /repo/patch` - Apply patch
- `GET /repo/status` - Repository status

---

## 🔍 Monitoring & Logs

### View Container Logs

```bash
# All containers
docker-compose logs

# Specific container
docker-compose logs agent-ai

# Follow logs (streaming)
docker-compose logs -f agent-ai

# Last 50 lines
docker-compose logs agent-ai --tail=50

# With timestamps
docker-compose logs -t agent-ai
```

### Access Metrics

```bash
# Prometheus (if using docker-compose.prod.yml)
# http://localhost:9091

# Grafana dashboards
# http://localhost:3000
# Default credentials: admin/admin

# Jaeger tracing
# http://localhost:16686
```

### Health Check Commands

```bash
# API Health
curl -X GET http://localhost:8000/health

# Metrics
curl -X GET http://localhost:8000/metrics

# Status
curl -X GET http://localhost:8000/status
```

---

## 🐛 Troubleshooting

### Issue: "Cannot connect to Docker daemon"

**Solution**: Ensure Docker Desktop is running
```bash
# Check Docker status
docker ps

# Start Docker Desktop (Windows)
"C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

### Issue: Port 8000 already in use

**Solution**: Use different port or stop other service
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (Windows)
taskkill /PID <PID> /F

# Or use different port
docker-compose -p agent-ai-alt up -d
```

### Issue: Import errors when starting

**Solution**: Rebuild image fresh
```bash
# Clean rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Issue: Database connection failures

**Solution**: Recreate volumes and reset state
```bash
# Remove all volumes
docker-compose down -v

# Start fresh
docker-compose up -d
```

### Issue: Out of memory

**Solution**: Increase Docker memory allocation
- Docker Desktop Settings → Resources → Memory → Increase to 4GB+
- Or clear unused images and containers:
```bash
docker system prune -a
```

---

## 📦 Docker Image Details

### Image Name
- **Development**: `agent_ai-agent-ai:latest`
- **Production**: `agent-ai:latest`

### Image Size
- Base Python 3.11-slim: ~150MB
- With dependencies: ~400MB
- With codebase: ~450MB

### Build Time
- Clean build: ~90 seconds (first time, ~70s on cache)
- Cached rebuild: ~3 seconds

### Dockerfile Location
- Development: `./Dockerfile`
- Production: `./Dockerfile` (use docker-compose.prod.yml)

---

## 🔐 Security Considerations

### Running Containers

✅ **Best Practices Implemented**:
- Non-root user (uvicorn process)
- Read-only root filesystem (production)
- Resource limits (CPU, memory)
- Network isolation (Docker networks)
- Secret management via environment variables
- Health checks configured
- Logging configured

### Production Hardening

For production deployment (docker-compose.prod.yml):
```bash
# Use environment variables for secrets
export JWT_SECRET_KEY="your-strong-secret-key"
export DB_PASSWORD="your-db-password"
export REDIS_PASSWORD="your-redis-password"

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

### SSL/TLS Configuration

Nginx reverse proxy handles SSL:
- Certificates placed in `./docker/nginx/ssl/`
- Configure in `docker-compose.prod.yml`
- Ports: 80 (HTTP) → 443 (HTTPS)

---

## 🚀 Production Deployment

### Option 1: Docker Compose (Small Scale)

```bash
# Set environment variables
export JWT_SECRET_KEY="production-secret"
export DB_PASSWORD="production-db-pass"
export REDIS_PASSWORD="production-redis-pass"

# Deploy with production compose file
docker-compose -f docker-compose.prod.yml up -d

# Monitor
docker-compose logs -f
```

### Option 2: Kubernetes (Enterprise)

```bash
# Apply manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Check status
kubectl get pods -n agent-ai
kubectl logs -f deployment/agent-ai -n agent-ai
```

### Option 3: AWS Terraform (Full Infrastructure)

```bash
# Configure AWS credentials
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"

# Plan and apply
cd terraform
terraform plan
terraform apply

# Get outputs
terraform output api_endpoint
```

---

## 📈 Performance Tuning

### Docker Compose Configuration

For high-load scenarios:

```yaml
services:
  agent-ai:
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 2G
        reservations:
          cpus: "1.0"
          memory: 1G
    environment:
      WORKER_THREADS: "8"
      CACHE_TTL: "7200"
```

### Database Optimization

For SQLite (development):
- File-based, limited to ~100 concurrent users
- Good for single-machine deployments

For PostgreSQL (production):
- Connection pooling: 20-50 connections
- Query optimization: Indexes on common filters
- Replication: Master-replica setup

### Cache Optimization

- Enable Redis for multi-instance deployments
- TTL tuning based on data freshness requirements
- Circuit breaker for failure scenarios
- Rate limiting to prevent abuse

---

## 🔄 Updating & Upgrades

### Update Code

```bash
# Pull latest changes
git pull origin main

# Rebuild container
docker-compose build --no-cache

# Restart with new code
docker-compose down
docker-compose up -d
```

### Update Dependencies

```bash
# Update requirements.txt
pip install --upgrade -r requirements.txt > new-requirements.txt

# Rebuild container
docker-compose build --no-cache
docker-compose up -d
```

### Database Migrations

```bash
# Run migrations in container
docker exec agent-ai python -m alembic upgrade head

# Or with docker-compose
docker-compose run --rm agent-ai python -m alembic upgrade head
```

---

## 📊 Monitoring Commands

### Container Health

```bash
# Check running containers
docker-compose ps

# Detailed inspection
docker inspect agent-ai

# Resource usage
docker stats agent-ai

# View system events
docker events --filter container=agent-ai
```

### Application Metrics

```bash
# Via curl
curl http://localhost:8000/metrics

# Via Python client
python -c "import requests; print(requests.get('http://localhost:8000/metrics').json())"
```

### Performance Testing

```bash
# Install Apache Bench
# apt-get install apache2-utils (Linux)
# choco install apache-bench (Windows)

# Load test
ab -n 1000 -c 10 http://localhost:8000/health

# Detailed metrics
ab -n 1000 -c 10 -g results.tsv http://localhost:8000/health
```

---

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs
- **Code Examples**: `examples/` directory
- **Configuration Guide**: `README_PROFESSIONAL.md`
- **Advanced Features**: `PROFESSIONAL_EDITION_COMPLETE.md`
- **Project Structure**: `PROJECT_STRUCTURE.md`

---

## ✅ Deployment Checklist

Before deploying to production:

- [ ] Environment variables configured
- [ ] Secrets managed securely
- [ ] Database initialized and tested
- [ ] Backup strategy defined
- [ ] Monitoring configured
- [ ] Logging centralized
- [ ] SSL certificates obtained
- [ ] Load balancer configured
- [ ] Auto-scaling policies defined
- [ ] Disaster recovery plan documented
- [ ] Security audit completed
- [ ] Performance baseline established

---

## 🎉 Success!

Your Agent AI Framework is now deployed and running!

**Next Steps**:
1. Explore the API at http://localhost:8000/docs
2. Run example workflows from `examples/` directory
3. Monitor metrics and logs
4. Plan scaling strategy for production

**Need Help?**
- Check logs: `docker-compose logs agent-ai`
- Run health check: `curl http://localhost:8000/health`
- Review troubleshooting section above

---

**Deployment Date**: December 4, 2025  
**Framework Version**: 1.0.0 - Professional Edition  
**Status**: ✅ LIVE AND READY

