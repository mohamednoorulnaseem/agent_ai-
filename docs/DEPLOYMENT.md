# Deployment Guide

Complete guide for deploying the AI Agent Framework to production environments.

## 📋 Table of Contents

- [Requirements](#requirements)
- [Environment Setup](#environment-setup)
- [Database Setup](#database-setup)
- [Docker Deployment](#docker-deployment)
- [Security Hardening](#security-hardening)
- [Monitoring & Logging](#monitoring--logging)
- [Troubleshooting](#troubleshooting)

---

## Requirements

### Minimum System Requirements

- **CPU**: 2+ cores
- **Memory**: 2GB+ RAM
- **Storage**: 10GB+ (for logs and data)
- **OS**: Linux (Ubuntu 20.04+, CentOS 8+) or macOS

### Software Requirements

- Docker 20.10+
- Docker Compose 2.0+
- Python 3.9+ (for direct installation)
- PostgreSQL 12+ (optional, for production DB)

---

## Environment Setup

### 1. Prepare Configuration

Copy and customize the environment template:

```bash
cp .env.example .env
```

Edit `.env` with production values:

```env
# LLM Configuration
LLM_PROVIDER=openai_like
LLM_MODEL=gpt-4
LLM_API_BASE=https://api.openai.com/v1
LLM_API_KEY=sk-xxxxxxxxxxxx

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Security
JWT_SECRET_KEY=your-super-secret-key-change-this-to-random-value
JWT_EXPIRATION_HOURS=24

# Database
DB_TYPE=postgresql
DB_CONNECTION_STRING=postgresql://user:password@db-host:5432/agent_prod

# Logging
LOG_LEVEL=INFO
LOG_FILE=true
LOG_FILE_PATH=/var/log/agent/agent.log

# Authentication
AUTH_ENABLED=true
API_KEY=api_key_xxxxxxxxxx

# Performance
WORKER_THREADS=4
CACHE_ENABLED=true
CACHE_TTL=3600
```

**⚠️ Important Security Notes:**

- Never commit `.env` to version control
- Use strong, random values for secrets
- Rotate `JWT_SECRET_KEY` regularly
- Use different keys for different environments

---

## Database Setup

### Option 1: PostgreSQL (Recommended for Production)

#### Install PostgreSQL

**Ubuntu:**

```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**macOS:**

```bash
brew install postgresql
brew services start postgresql
```

#### Create Database and User

```bash
sudo -u postgres psql

# Inside psql:
CREATE DATABASE agent_prod;
CREATE USER agent_user WITH PASSWORD 'your_secure_password';

ALTER ROLE agent_user SET client_encoding TO 'utf8';
ALTER ROLE agent_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE agent_user SET default_transaction_deferrable TO on;
ALTER ROLE agent_user SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE agent_prod TO agent_user;

\q
```

Update `.env`:

```env
DB_CONNECTION_STRING=postgresql://agent_user:your_secure_password@localhost:5432/agent_prod
```

#### Run Migrations

```bash
python -m src.persistence --migrate
# or
alembic upgrade head
```

### Option 2: SQLite (Development/Small Deployments)

```env
DB_TYPE=sqlite
DB_PATH=/var/lib/agent/agent.db
```

Ensure the directory exists:

```bash
sudo mkdir -p /var/lib/agent
sudo chown app-user:app-user /var/lib/agent
sudo chmod 755 /var/lib/agent
```

---

## Docker Deployment

### Production Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: "3.8"

services:
  agent-ai:
    image: agent-ai:latest
    container_name: agent-ai-prod
    restart: always
    ports:
      - "8000:8000"
    environment:
      - LLM_PROVIDER=${LLM_PROVIDER}
      - LLM_MODEL=${LLM_MODEL}
      - LLM_API_BASE=${LLM_API_BASE}
      - LLM_API_KEY=${LLM_API_KEY}
      - API_HOST=0.0.0.0
      - API_PORT=8000
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - DB_CONNECTION_STRING=${DB_CONNECTION_STRING}
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./logs:/var/log/agent
    networks:
      - agent-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    depends_on:
      - postgres

  postgres:
    image: postgres:15-alpine
    container_name: agent-db-prod
    restart: always
    environment:
      POSTGRES_DB: agent_prod
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - agent-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  nginx:
    image: nginx:alpine
    container_name: agent-nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
      - ./html:/usr/share/nginx/html:ro
    networks:
      - agent-network
    depends_on:
      - agent-ai

volumes:
  postgres-data:

networks:
  agent-network:
    driver: bridge
```

### Deploy with Docker Compose

```bash
# Build image
docker compose -f docker-compose.prod.yml build

# Start services
docker compose -f docker-compose.prod.yml up -d

# Check status
docker compose -f docker-compose.prod.yml ps

# View logs
docker compose -f docker-compose.prod.yml logs -f agent-ai
```

---

## Security Hardening

### 1. Firewall Configuration

```bash
sudo ufw enable
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw deny 8000/tcp     # Block direct API access (use via nginx)
```

### 2. SSL/TLS Certificates

Use Let's Encrypt:

```bash
sudo apt-get install certbot python3-certbot-nginx

sudo certbot certonly --standalone -d your-domain.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

### 3. Nginx Configuration

Create `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream agent_api {
        server agent-ai:8000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

    server {
        listen 80;
        server_name your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/certs/fullchain.pem;
        ssl_certificate_key /etc/nginx/certs/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        # Security headers
        add_header Strict-Transport-Security "max-age=31536000" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-Frame-Options "DENY" always;
        add_header X-XSS-Protection "1; mode=block" always;

        location / {
            limit_req zone=api_limit burst=20 nodelay;

            proxy_pass http://agent_api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # WebSocket support
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }

        location /health {
            access_log off;
            proxy_pass http://agent_api;
        }
    }
}
```

### 4. API Security

Set in `.env`:

```env
AUTH_ENABLED=true
API_KEY=your_secure_api_key
JWT_SECRET_KEY=your_very_long_random_secret_key_minimum_32_chars
JWT_EXPIRATION_HOURS=24
```

### 5. Backup Strategy

```bash
# Automated daily backups
0 2 * * * /usr/local/bin/backup-agent.sh

# backup-agent.sh
#!/bin/bash
BACKUP_DIR="/backups/agent"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
docker compose -f /app/docker-compose.prod.yml exec -T postgres \
  pg_dump -U agent_user agent_prod > $BACKUP_DIR/db_$DATE.sql

# Backup data
tar -czf $BACKUP_DIR/data_$DATE.tar.gz /app/data/

# Keep only last 7 days
find $BACKUP_DIR -type f -mtime +7 -delete

echo "Backup completed: $DATE"
```

---

## Monitoring & Logging

### 1. Application Logging

Logs are written to:

```
/var/log/agent/agent.log
```

Monitor in real-time:

```bash
tail -f /var/log/agent/agent.log
```

### 2. Container Monitoring

```bash
# View resource usage
docker stats agent-ai-prod

# View logs
docker logs -f agent-ai-prod

# Container health
docker inspect --format='{{.State.Health}}' agent-ai-prod
```

### 3. Database Monitoring

```bash
# Connect to PostgreSQL
psql -U agent_user -d agent_prod -h localhost

# Check database size
SELECT pg_size_pretty(pg_database_size('agent_prod'));

# List active connections
SELECT count(*) FROM pg_stat_activity;
```

### 4. Optional: Prometheus & Grafana

Add to `docker-compose.prod.yml`:

```yaml
prometheus:
  image: prom/prometheus:latest
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml

grafana:
  image: grafana/grafana:latest
  ports:
    - "3000:3000"
```

---

## Updating & Maintenance

### Regular Updates

```bash
# Pull latest changes
git pull origin main

# Rebuild image
docker compose -f docker-compose.prod.yml build

# Restart services
docker compose -f docker-compose.prod.yml up -d

# Check status
docker compose -f docker-compose.prod.yml ps
```

### Scaling

For multiple instances with load balancing:

```yaml
services:
  agent-ai-1:
    # ... config
    depends_on:
      - postgres

  agent-ai-2:
    # ... same config, different container name
    depends_on:
      - postgres

  load-balancer:
    image: nginx:alpine
    # Route traffic between instances
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs agent-ai-prod

# Check health
docker inspect agent-ai-prod | grep -A 5 "Health"

# Restart
docker compose -f docker-compose.prod.yml restart agent-ai
```

### Database Connection Failed

```bash
# Test connection
docker compose -f docker-compose.prod.yml exec postgres \
  psql -U agent_user -d agent_prod -c "SELECT 1;"

# Check network
docker network inspect agent_agent-network
```

### High Memory Usage

```bash
# Check memory
docker stats agent-ai-prod

# Adjust in docker-compose
environment:
  - WORKER_THREADS=2
  - CACHE_TTL=1800  # Reduce cache TTL
```

### Stuck Tasks

```bash
# Connect to database
psql -U agent_user -d agent_prod

# View stuck tasks
SELECT * FROM tasks WHERE status = 'executing' AND updated_at < NOW() - interval '1 hour';

# Reset task
UPDATE tasks SET status = 'failed' WHERE id = 'task_id';
```

---

## Production Checklist

- ✅ Environment configured (`.env`)
- ✅ Database created and migrated
- ✅ SSL certificates installed
- ✅ Firewall configured
- ✅ Backups enabled
- ✅ Logging configured
- ✅ Monitoring set up
- ✅ Health checks working
- ✅ Rate limiting enabled
- ✅ API keys generated
- ✅ JWT secrets configured
- ✅ Load testing completed

---

## Support

For deployment issues:

- Check [troubleshooting](#troubleshooting) section
- Review logs: `docker logs -f agent-ai-prod`
- Open an issue on [GitHub](https://github.com/mohamednoorulnaseem/agent_ai-)
