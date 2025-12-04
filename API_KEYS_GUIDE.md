# 🔑 API Key Management Guide

**Status**: ✅ **LIVE AND READY**  
**Date**: December 4, 2025  
**Version**: 1.0.0  

---

## 🎯 Quick Start - Generate & Use API Keys

### 1. Generate a New API Key

```bash
# Using curl
curl -X POST http://localhost:8000/api-keys/generate \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Application",
    "expires_in_days": 90,
    "rate_limit": 1000,
    "scopes": ["read", "write"]
  }'

# Response:
{
  "key": "ak_jR3vZ9xK...",          # Save this securely!
  "key_id": "id_a1b2c3d4",
  "name": "My Application",
  "created_at": "2025-12-04T...",
  "expires_at": "2025-03-03T...",
  "scopes": ["read", "write"],
  "message": "Save this key securely. It will not be shown again."
}
```

**⚠️ Important**: The raw key is shown **only once**. Save it securely!

---

## 📚 API Key Endpoints

### Generate Key
```
POST /api-keys/generate
```

**Request**:
```json
{
  "name": "Production API Key",
  "expires_in_days": 90,
  "rate_limit": 5000,
  "scopes": ["read", "write"],
  "metadata": {"environment": "production"}
}
```

**Response**:
```json
{
  "key": "ak_...",
  "key_id": "id_...",
  "name": "Production API Key",
  "created_at": "2025-12-04T14:30:00",
  "expires_at": "2025-03-04T14:30:00",
  "scopes": ["read", "write"]
}
```

---

### List Keys
```
GET /api-keys/list?owner=default
```

**Response**:
```json
{
  "keys": [
    {
      "key_id": "id_a1b2c3d4",
      "name": "My Application",
      "created_at": "2025-12-04T14:30:00",
      "last_used": "2025-12-04T15:45:30",
      "expires_at": "2025-03-04T14:30:00",
      "status": "active",
      "rate_limit": 1000,
      "usage_count": 245,
      "owner": "default",
      "scopes": ["read", "write"],
      "is_active": true
    }
  ],
  "total": 1
}
```

---

### Get Key Details
```
GET /api-keys/{key_id}
```

**Response**: Same as list endpoint, single key

---

### Revoke Key
```
POST /api-keys/{key_id}/revoke
```

**Response**:
```json
{
  "success": true,
  "key_id": "id_a1b2c3d4",
  "message": "API key 'id_a1b2c3d4' has been revoked"
}
```

---

### Rotate Key
```
POST /api-keys/{key_id}/rotate?expires_in_days=90
```

**Response**:
```json
{
  "key": "ak_newKey...",
  "key_id": "id_xyz789",
  "message": "Old key has been revoked. Save new key securely."
}
```

---

### Delete Key
```
DELETE /api-keys/{key_id}
```

**Response**:
```json
{
  "success": true,
  "key_id": "id_a1b2c3d4",
  "message": "API key 'id_a1b2c3d4' has been permanently deleted"
}
```

---

### Get Usage Statistics
```
GET /api-keys/stats/usage?owner=default
```

**Response**:
```json
{
  "total_keys": 5,
  "total_requests": 12847,
  "last_request": "2025-12-04T15:45:30",
  "active_keys": 4
}
```

---

### Validate Key
```
POST /api-keys/validate
```

**Request**:
```json
{
  "api_key": "ak_..."
}
```

**Response**:
```json
{
  "valid": true,
  "key_id": "id_a1b2c3d4",
  "name": "My Application",
  "scopes": ["read", "write"],
  "rate_limit": 1000,
  "usage_count": 245,
  "message": "API key is valid"
}
```

---

## 🔐 Using API Keys in Requests

### Method 1: X-API-Key Header (Recommended)

```bash
curl -X GET http://localhost:8000/plans \
  -H "X-API-Key: ak_jR3vZ9xK..."
```

### Method 2: Bearer Token

```bash
curl -X GET http://localhost:8000/plans \
  -H "Authorization: Bearer ak_jR3vZ9xK..."
```

### Method 3: Python Requests Library

```python
import requests

api_key = "ak_jR3vZ9xK..."

headers = {
    "X-API-Key": api_key
}

response = requests.get(
    "http://localhost:8000/plans",
    headers=headers
)

print(response.json())
```

### Method 4: JavaScript/Fetch API

```javascript
const apiKey = "ak_jR3vZ9xK...";

const response = await fetch("http://localhost:8000/plans", {
  headers: {
    "X-API-Key": apiKey
  }
});

const data = await response.json();
console.log(data);
```

---

## 🛡️ Security Best Practices

### Key Generation

- ✅ Keys are generated using `secrets.token_urlsafe()` (cryptographically secure)
- ✅ Keys are hashed with SHA-256 before storage
- ✅ Raw key shown only once at generation time
- ✅ Keys cannot be recovered after initial generation

### Storage

- ✅ Store keys in environment variables or secure vaults:
  ```bash
  export API_KEY="ak_..."
  ```

- ✅ Never commit keys to version control:
  ```bash
  echo "API_KEY=ak_..." >> .env
  git add .env  # ⚠️ NO! Add .env to .gitignore instead
  ```

- ✅ Use `.env` file with `.gitignore`:
  ```
  # .gitignore
  .env
  .env.local
  *.key
  ```

### Rotation & Expiration

- ✅ Set expiration dates: `expires_in_days=90`
- ✅ Rotate keys periodically using `/api-keys/{key_id}/rotate`
- ✅ Revoke keys before rotation using `/api-keys/{key_id}/revoke`
- ✅ Monitor usage with statistics endpoint

### Access Control

- ✅ Use scopes to limit permissions:
  - `["read"]` - Read-only access
  - `["write"]` - Write-only access
  - `["read", "write"]` - Full access
  - Custom: `["read:plans", "write:webhooks"]`

- ✅ Different keys for different applications:
  ```bash
  # Web frontend
  curl -X POST http://localhost:8000/api-keys/generate \
    -d '{"name": "Web App", "scopes": ["read"]}'

  # Mobile app
  curl -X POST http://localhost:8000/api-keys/generate \
    -d '{"name": "Mobile App", "scopes": ["read"]}'

  # CI/CD pipeline
  curl -X POST http://localhost:8000/api-keys/generate \
    -d '{"name": "CI/CD", "scopes": ["write"]}'
  ```

### Monitoring

- ✅ Track usage with statistics:
  ```bash
  curl http://localhost:8000/api-keys/stats/usage
  ```

- ✅ Check last used time:
  ```bash
  curl http://localhost:8000/api-keys/list | jq '.keys[] | {name, last_used}'
  ```

- ✅ Alert on unused keys (check `last_used` is recent)

- ✅ Audit key operations (API logs track all key actions)

---

## 📋 Complete Workflow Example

### 1. Generate a Production API Key

```bash
# Generate key for production service
curl -X POST http://localhost:8000/api-keys/generate \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Production Service",
    "expires_in_days": 365,
    "rate_limit": 10000,
    "scopes": ["read", "write"],
    "metadata": {
      "environment": "production",
      "service": "main-api",
      "owner": "devops-team"
    }
  }'

# Save output:
# key: ak_abc123xyz789...
# key_id: id_prod001
```

### 2. Store Key Securely

```bash
# Save to environment variable (local development)
export AGENT_API_KEY="ak_abc123xyz789..."

# Or save to .env file (also add to .gitignore)
echo "AGENT_API_KEY=ak_abc123xyz789..." >> .env
```

### 3. Use Key in Application

```python
import os
import requests

api_key = os.getenv("AGENT_API_KEY")

def get_plans():
    headers = {"X-API-Key": api_key}
    response = requests.get(
        "http://localhost:8000/plans",
        headers=headers
    )
    return response.json()

# Make API calls
plans = get_plans()
for plan in plans:
    print(f"Plan: {plan['goal']}")
```

### 4. Monitor Usage

```bash
# Check usage statistics
curl http://localhost:8000/api-keys/stats/usage

# List all keys with details
curl http://localhost:8000/api-keys/list | jq '.'
```

### 5. Rotate Key Before Expiration

```bash
# Create new key to replace old one
NEW_KEY=$(curl -X POST http://localhost:8000/api-keys/generate \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Production Service (Rotated)",
    "expires_in_days": 365,
    "scopes": ["read", "write"]
  }' | jq -r '.key')

# Update application to use new key
export AGENT_API_KEY="$NEW_KEY"

# Revoke old key
curl -X POST http://localhost:8000/api-keys/id_prod001/revoke
```

---

## 🚀 Rate Limiting

Each API key has a configurable rate limit (requests per minute):

```bash
# Generate key with 100 requests/minute limit
curl -X POST http://localhost:8000/api-keys/generate \
  -d '{
    "name": "Limited Key",
    "rate_limit": 100
  }'

# Key tracks usage in `usage_count`
# Check current usage:
curl http://localhost:8000/api-keys/list | jq '.keys[] | {name, usage_count}'
```

---

## 📊 Key Metadata

Store custom metadata with keys:

```bash
curl -X POST http://localhost:8000/api-keys/generate \
  -d '{
    "name": "Frontend App",
    "metadata": {
      "environment": "production",
      "region": "us-east-1",
      "team": "frontend",
      "cost_center": "engineering",
      "contact": "frontend-team@example.com"
    }
  }'
```

Retrieve with key details:
```bash
curl http://localhost:8000/api-keys/list | jq '.keys[] | .metadata'
```

---

## 🔍 Troubleshooting

### Issue: "Invalid API key"

```bash
# Verify key is active
curl -X POST http://localhost:8000/api-keys/validate \
  -d '{"api_key": "ak_..."}'

# Check if key is expired
curl http://localhost:8000/api-keys/list | \
  jq '.keys[] | {name, expires_at, is_active}'
```

### Issue: "API key does not have required scope"

```bash
# Check scopes for key
curl http://localhost:8000/api-keys/list | \
  jq '.keys[] | {name, scopes}'

# Generate new key with additional scopes
curl -X POST http://localhost:8000/api-keys/generate \
  -d '{
    "name": "Enhanced Key",
    "scopes": ["read", "write"]
  }'
```

### Issue: Lost API Key

**Cannot recover lost keys!**

Solution:
1. Revoke the old key: `POST /api-keys/{key_id}/revoke`
2. Generate a new key: `POST /api-keys/generate`
3. Update application to use new key

---

## 📖 Additional Resources

- **OpenAPI/Swagger Docs**: http://localhost:8000/docs
- **API Key Routes**: See `src/api_keys_routes.py`
- **Core Implementation**: See `src/api_keys.py`
- **Middleware**: See `src/api_key_middleware.py`

---

## ✅ Deployment Checklist

Before using API keys in production:

- [ ] Generate production key with appropriate scopes
- [ ] Set expiration date (e.g., 90-365 days)
- [ ] Configure rate limits based on expected usage
- [ ] Store key in secure vault (AWS Secrets Manager, HashiCorp Vault)
- [ ] Enable audit logging for key operations
- [ ] Set up monitoring for unused keys
- [ ] Document key rotation schedule
- [ ] Brief team on security best practices
- [ ] Test key access before deployment

---

## 🎉 Success!

Your API key authentication system is now ready!

**Next Steps**:
1. Generate your first API key
2. Test with curl or Postman
3. Integrate into your application
4. Monitor usage and rotation

---

**Framework Version**: 1.0.0 - Professional Edition  
**API Version**: v0.1.0  
**Status**: ✅ LIVE AND READY  
**Last Updated**: December 4, 2025

