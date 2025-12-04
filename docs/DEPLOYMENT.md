# Deployment Guide

Complete guide for deploying the Agent AI Framework to production using Kubernetes, Terraform, or Docker Compose.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Docker Compose Deployment](#docker-compose-deployment)
3. [Kubernetes Deployment](#kubernetes-deployment)
4. [AWS Deployment](#aws-deployment)
5. [Terraform IaC Deployment](#terraform-deployment)

## Quick Start

### Option 1: Docker Compose (Development/Small Scale)

```bash
cd agent_ai
cp .env.example .env.prod
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
docker-compose -f docker-compose.prod.yml ps
curl http://localhost:8000/health
```

### Option 2: Kubernetes (Production)

```bash
kubectl create namespace agent-ai
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/deployment.yaml
kubectl get deployments -n agent-ai
```

### Option 3: Terraform on AWS

```bash
cd terraform
terraform init
terraform plan -out=plan.tfplan
terraform apply plan.tfplan
aws eks update-kubeconfig --region us-east-1 --name agent-ai-cluster
kubectl apply -f ../k8s/
```

## Docker Compose Deployment

### Recommended For

- Development environments
- Small to medium deployments
- Single or multi-node Docker hosts
- Quick testing and prototyping

### Services Included

1. **Agent AI Application** (Port 8000, 9090 metrics)

   - 3 replicas with health checks
   - Automatic restart
   - Resource limits: 1.0 CPU, 1GB RAM

2. **PostgreSQL Database** (Port 5432)

   - Volume persistence
   - Automatic backups
   - Health monitoring

3. **Redis Cache** (Port 6379)

   - Password-protected
   - AOF persistence
   - LRU memory policy

4. **Prometheus** (Port 9091)

   - Metrics collection
   - 30-day retention
   - Auto-configured scraping

5. **Grafana** (Port 3000)

   - Pre-configured dashboards
   - Prometheus integration
   - User management

6. **Jaeger Tracing** (Port 16686)

   - Distributed request tracing
   - Service visualization

7. **NGINX Reverse Proxy** (Ports 80, 443)
   - SSL/TLS termination
   - Rate limiting
   - Load balancing

### Configuration

Create `.env.prod`:

```env
ENVIRONMENT=production
LOG_LEVEL=info
LLM_PROVIDER=openai
LLM_API_KEY=sk-your-api-key
DB_USER=postgres
DB_PASSWORD=your-secure-password
DB_NAME=agent_ai
REDIS_PASSWORD=redis-password
WEBHOOK_SECRET=webhook-secret
CACHE_TTL=3600
MAX_WORKERS=4
GRAFANA_PASSWORD=grafana-admin-password
AGENT_AI_VERSION=1.0.0
```

### Start Services

```bash
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

### Monitor

```bash
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs -f agent-ai
docker stats
```

### Backup Database

```bash
docker-compose -f docker-compose.prod.yml exec postgres \
  pg_dump -U postgres agent_ai > backup-$(date +%Y%m%d).sql
```

## Kubernetes Deployment

### Recommended For

- Production environments
- Multi-cloud/hybrid deployments
- Auto-scaling requirements
- Enterprise deployments

### Prerequisites

1. Kubernetes cluster (1.28+)
2. kubectl configured
3. Images in registry (Docker Hub, ECR, GCR)

### Deployment Steps

1. **Create Namespace**

   ```bash
   kubectl create namespace agent-ai
   ```

2. **Create Secrets**

   ```bash
   kubectl create secret generic agent-ai-secrets \
     --from-literal=llm_api_key=sk-your-key \
     --from-literal=database_url=postgresql://user:pass@host:5432/db \
     -n agent-ai
   ```

3. **Deploy ConfigMaps & Secrets**

   ```bash
   kubectl apply -f k8s/configmap.yaml
   ```

4. **Deploy Services**

   ```bash
   kubectl apply -f k8s/service.yaml
   ```

5. **Deploy Application**

   ```bash
   kubectl apply -f k8s/deployment.yaml
   ```

6. **Verify**
   ```bash
   kubectl get deployments -n agent-ai
   kubectl get pods -n agent-ai
   kubectl get svc -n agent-ai
   ```

### Access Application

```bash
# Port forward
kubectl port-forward svc/agent-ai-service 8000:80 -n agent-ai

# Or use LoadBalancer external IP
kubectl get svc agent-ai-service -n agent-ai
```

### Scaling

```bash
# Manual scale
kubectl scale deployment agent-ai --replicas=5 -n agent-ai

# Auto-scaling (via HPA)
kubectl get hpa -n agent-ai
```

### Update Deployment

```bash
# Update image
kubectl set image deployment/agent-ai \
  agent-ai=agent-ai:v2.0.0 -n agent-ai

# Rollback
kubectl rollout undo deployment/agent-ai -n agent-ai
```

### View Logs

```bash
kubectl logs deployment/agent-ai -n agent-ai -f
kubectl logs pod/agent-ai-xxxxx -n agent-ai
```

## AWS Deployment

### EKS (Elastic Kubernetes Service)

#### Create Cluster

```bash
eksctl create cluster \
  --name agent-ai \
  --version 1.28 \
  --region us-east-1 \
  --nodes 3 \
  --node-type t3.large
```

#### Configure kubectl

```bash
aws eks update-kubeconfig \
  --region us-east-1 \
  --name agent-ai
```

#### Deploy Application

```bash
kubectl apply -f k8s/
```

### RDS Database

```bash
aws rds create-db-instance \
  --db-instance-identifier agent-ai-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username postgres \
  --master-user-password YOUR_SECURE_PASSWORD
```

### ElastiCache Redis

```bash
aws elasticache create-cache-cluster \
  --cache-cluster-id agent-ai-redis \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --num-cache-nodes 1
```

### ECR Repository

```bash
aws ecr create-repository --repository-name agent-ai

# Push image
docker tag agent-ai:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/agent-ai:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/agent-ai:latest
```

## Terraform Deployment

### Prerequisites

```bash
# Install Terraform
brew install terraform

# AWS credentials
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret

# Create S3 backend
aws s3 mb s3://agent-ai-terraform-state
aws s3api put-bucket-versioning \
  --bucket agent-ai-terraform-state \
  --versioning-configuration Status=Enabled

# Create DynamoDB locks table
aws dynamodb create-table \
  --table-name terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1
```

### Deploy Infrastructure

```bash
cd terraform

# Initialize
terraform init

# Plan
terraform plan -out=plan.tfplan

# Apply
terraform apply plan.tfplan

# Get outputs
terraform output
```

### Outputs

```bash
terraform output eks_cluster_name
terraform output rds_endpoint
terraform output redis_endpoint
terraform output ecr_repository_url
terraform output kubeconfig_command
```

### Destroy Infrastructure

```bash
terraform destroy
```

## Monitoring

### Prometheus

Access: http://localhost:9091/targets

### Grafana

Access: http://localhost:3000
Default: admin / (password from .env)

### Jaeger

Access: http://localhost:16686

### Application Logs

```bash
# Docker Compose
docker-compose -f docker-compose.prod.yml logs agent-ai

# Kubernetes
kubectl logs deployment/agent-ai -n agent-ai -f
```

## Performance Tuning

### Database

```sql
CREATE INDEX idx_plan_status ON plans(status);
CREATE INDEX idx_task_created ON tasks(created_at);
VACUUM ANALYZE;
```

### Cache

```python
# Adjust TTL
CACHE_TTL = 3600  # 1 hour

# Use appropriate keys
cache.set("plan:123", data, ttl=3600)
```

### Load Testing

```bash
# Apache Bench
ab -n 10000 -c 100 http://localhost:8000/

# wrk
wrk -t4 -c100 -d30s http://localhost:8000/
```

## Backup & Recovery

### PostgreSQL Backup

```bash
# Dump
pg_dump -h <host> -U postgres agent_ai > backup.sql

# Restore
psql -h <host> -U postgres agent_ai < backup.sql
```

### Kubernetes Snapshots

```bash
# PVC snapshot
kubectl apply -f k8s/pvc-snapshot.yaml

# View snapshots
kubectl get volumesnapshot -n agent-ai
```

## Troubleshooting

### Container Issues

```bash
# Check logs
docker logs agent-ai-prod

# Restart
docker restart agent-ai-prod

# Check health
curl http://localhost:8000/health
```

### Database Issues

```bash
# Test connection
psql -h <host> -U postgres -c "SELECT 1;"

# Check running queries
SELECT * FROM pg_stat_activity;
```

### Kubernetes Issues

```bash
# Check events
kubectl describe pod <pod-name> -n agent-ai

# Check logs
kubectl logs <pod-name> -n agent-ai

# Debug pod
kubectl exec -it <pod-name> -n agent-ai -- /bin/sh
```

---

For detailed configuration, see [Kubernetes Manifests](../k8s/), [Terraform Configs](../terraform/), or [Docker Compose Setup](DOCKER_COMPOSE_PROD.md).
