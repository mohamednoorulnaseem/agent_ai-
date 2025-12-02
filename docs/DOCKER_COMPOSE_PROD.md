# Production Docker Compose Configuration

This file contains a complete production-ready Docker Compose setup for the Agent AI Framework with monitoring, logging, and high availability.

## Quick Start

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- At least 8GB RAM
- 20GB free disk space

### Environment Setup

Create `.env.prod` file:

```env
ENVIRONMENT=production
LOG_LEVEL=info

# LLM Configuration
LLM_PROVIDER=openai
LLM_API_KEY=sk-your-api-key-here

# Database
DB_USER=postgres
DB_PASSWORD=your-secure-password-here
DB_NAME=agent_ai

# Redis
REDIS_PASSWORD=your-redis-password-here
REDIS_MAX_MEMORY=512mb

# Webhook Security
WEBHOOK_SECRET=your-webhook-secret-here

# Performance
CACHE_TTL=3600
MAX_WORKERS=4

# Grafana
GRAFANA_PASSWORD=your-grafana-admin-password

# Versions
AGENT_AI_VERSION=1.0.0
```

### Start Services

```bash
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

### Verify Services

```bash
# Check all services
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs -f agent-ai

# Health check
curl http://localhost:8000/health
```

## Services

### Agent AI Application
- **Port**: 8000 (HTTP), 9090 (Metrics)
- **Container**: `agent-ai-app`
- **Health Check**: `/health` endpoint
- **Logging**: JSON format, rotated daily

### PostgreSQL Database
- **Port**: 5432
- **Container**: `agent-ai-postgres`
- **Persistence**: `postgres-data` volume
- **Backups**: Use `pg_dump` for backups
- **Init Script**: `docker/postgres/init.sql`

### Redis Cache
- **Port**: 6379
- **Container**: `agent-ai-redis`
- **Auth**: Password-protected
- **Persistence**: AOF (Append-Only File)
- **Memory Policy**: LRU eviction
- **Max Memory**: Configurable via `REDIS_MAX_MEMORY`

### Prometheus Monitoring
- **Port**: 9091 (mapped from 9090)
- **Container**: `agent-ai-prometheus`
- **Config**: `docker/prometheus/prometheus.yml`
- **Scrapes**: Agent AI metrics every 15s
- **Retention**: 30 days (default)

### Grafana Dashboards
- **Port**: 3000
- **Container**: `agent-ai-grafana`
- **Default Admin**: admin / (password from .env)
- **Data Source**: Prometheus (auto-configured)
- **Dashboards**: Auto-provisioned from config

### Jaeger Tracing
- **Port**: 16686 (UI)
- **Container**: `agent-ai-jaeger`
- **Collector**: Port 14268
- **UI**: http://localhost:16686

### NGINX Reverse Proxy
- **Port**: 80, 443
- **Container**: `agent-ai-nginx`
- **Config**: `docker/nginx/nginx.conf`
- **SSL**: Optional certificates in `docker/nginx/ssl`

## Networking

All services communicate via `agent-ai-network` bridge network:
- Isolated from host network
- Internal DNS resolution
- Service discovery by container name

## Volumes

| Volume | Purpose | Mount Point |
|--------|---------|-------------|
| `postgres-data` | Database files | `/var/lib/postgresql/data` |
| `redis-data` | Redis persistence | `/data` |
| `agent-ai-cache` | Application cache | `/app/cache` |
| `agent-ai-logs` | Application logs | `/app/logs` |
| `prometheus-data` | Metrics storage | `/prometheus` |
| `grafana-data` | Grafana config | `/var/lib/grafana` |

## Resource Limits

Each service has memory and CPU limits:

```
agent-ai:      1.0 CPU, 1GB RAM (reserved: 0.5 CPU, 512MB)
postgres:      1.0 CPU, 512MB RAM (reserved: 0.5 CPU, 256MB)
redis:         0.5 CPU, 512MB RAM (reserved: 0.25 CPU, 256MB)
prometheus:    0.5 CPU, 256MB RAM (reserved: 0.25 CPU, 128MB)
grafana:       0.5 CPU, 256MB RAM (reserved: 0.25 CPU, 128MB)
jaeger:        0.5 CPU, 256MB RAM (reserved: 0.25 CPU, 128MB)
nginx:         0.25 CPU, 128MB RAM (reserved: 0.1 CPU, 64MB)
```

## Logging

All services use JSON file logging driver:
- Max file size: 10MB
- Max files: 3
- Automatic rotation

## Health Checks

Each service includes health checks:
- Agent AI: HTTP `/health` endpoint
- PostgreSQL: `pg_isready` command
- Redis: INCR ping command
- Success after 3 retries with 10s interval

## Scaling

### Scale Agent AI Application

```bash
docker-compose -f docker-compose.prod.yml up -d --scale agent-ai=3
```

Note: Must use different port bindings or load balancer.

### Scale Other Services

Other services (postgres, redis) are single instances for data consistency.

## Backup & Recovery

### PostgreSQL Backup

```bash
docker-compose -f docker-compose.prod.yml exec postgres \
  pg_dump -U postgres agent_ai > backup.sql
```

### PostgreSQL Restore

```bash
docker-compose -f docker-compose.prod.yml exec -T postgres \
  psql -U postgres agent_ai < backup.sql
```

### Redis Backup

```bash
docker-compose -f docker-compose.prod.yml exec redis \
  redis-cli --rdb /data/dump.rdb
```

### Volume Backup

```bash
docker run --rm -v agent-ai-postgres:/data \
  -v $(pwd):/backup ubuntu \
  tar czf /backup/postgres.tar.gz /data
```

## Monitoring

### Prometheus Targets
http://localhost:9091/targets

### Grafana Dashboards
http://localhost:3000

### Jaeger Traces
http://localhost:16686

## Updating

### Update Application

```bash
# Update image
docker pull agent-ai:latest

# Recreate container
docker-compose -f docker-compose.prod.yml up -d agent-ai
```

### Update Monitoring Stack

```bash
# Update all images
docker-compose -f docker-compose.prod.yml pull

# Recreate services
docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

### Agent AI Not Starting

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs agent-ai

# Check health
curl http://localhost:8000/health

# Restart
docker-compose -f docker-compose.prod.yml restart agent-ai
```

### Database Connection Issues

```bash
# Check PostgreSQL
docker-compose -f docker-compose.prod.yml exec postgres psql -U postgres -c "SELECT 1"

# Check network
docker-compose -f docker-compose.prod.yml exec agent-ai \
  nslookup postgres
```

### Redis Connection Issues

```bash
# Check Redis
docker-compose -f docker-compose.prod.yml exec redis \
  redis-cli -a ${REDIS_PASSWORD} ping

# Check network
docker-compose -f docker-compose.prod.yml exec agent-ai \
  nslookup redis
```

### High Memory Usage

```bash
# Check container memory
docker stats

# Reduce Redis max memory
# Edit .env.prod: REDIS_MAX_MEMORY=256mb
docker-compose -f docker-compose.prod.yml restart redis
```

## Performance Tuning

### PostgreSQL
- Connection pooling with PgBouncer (optional)
- Index optimization
- Vacuum settings

### Redis
- Maxmemory policy: `allkeys-lru` (LRU eviction)
- AOF fsync: `everysec` (balance)
- Key expiration monitoring

### Application
- Horizontal scaling behind load balancer
- Connection pooling
- Caching strategy

## Security

### Network Security
- Internal network isolation
- No direct public access (proxy via NGINX)
- Firewall rules for external access

### Data Security
- Database password protection
- Redis password authentication
- Volume encryption (host-level)
- SSL/TLS termination (NGINX)

### Container Security
- Non-root users
- Dropped capabilities
- Read-only root filesystem
- No privilege escalation

## Cleanup

### Stop Services

```bash
docker-compose -f docker-compose.prod.yml stop
```

### Remove Containers

```bash
docker-compose -f docker-compose.prod.yml down
```

### Remove Volumes (Data Loss!)

```bash
docker-compose -f docker-compose.prod.yml down -v
```

---

For questions, see [Deployment Guide](DEPLOYMENT.md) or [Infrastructure Setup](../README.md).
