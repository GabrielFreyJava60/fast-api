# EC2 Deployment Guide

## Prerequisites

- AWS Account
- AWS CLI configured
- EC2 instance: t3.xlarge with Amazon Linux 2023
- Security group allowing inbound traffic on port 8000

## Step-by-Step Deployment

### 1. Launch EC2 Instance

```
Instance Type: t3.xlarge
AMI: Amazon Linux 2023 kernel-6.1
Key pair: Proceed without key pair (or create one)
Security Group: Allow inbound TCP on port 8000
```

### 2. Connect to EC2 Instance

```bash
# Via AWS Console: Connect -> EC2 Instance Connect
# Or via SSH if you created a key pair
```

### 3. Clone Repository

```bash
git clone https://github.com/GabrielFreyJava60/fast-api.git
cd fast-api
git checkout hw-46
```

### 4. Run Setup Script

```bash
chmod +x setup_ec2.sh
./setup_ec2.sh
```

This installs:
- Docker
- Ollama
- phi3 model

### 5. Create ECR Repository

```bash
# In AWS Console: ECR -> Create repository
# Repository name: travel-app
```

### 6. Setup IAM Role for EC2

```
1. EC2 Console -> Instances -> Select your instance
2. Actions -> Security -> Modify IAM role
3. Create new role (if needed):
   - Trusted entity: EC2
   - Permission: AWSAppRunnerServicePolicyForECRAccess
   - Name: EC2-ECR-Access
4. Attach role to instance
```

### 7. Update deploy.sh

Edit deploy.sh and replace:
```bash
REGION="us-east-1"  # Your AWS region
ACCOUNT_ID="123456789012"  # Your AWS account ID
```

### 8. Deploy Application

```bash
chmod +x deploy.sh
./deploy.sh
```

### 9. Verify Deployment

```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Check Docker container
sudo docker ps | grep travel-app

# Test health endpoint
curl http://localhost:8000/health

# Test from your machine (replace with EC2 public IP)
curl http://<EC2_PUBLIC_IP>:8000/health
```

### 10. Test Application

```bash
# Health check
curl http://<EC2_PUBLIC_IP>:8000/health

# Ask a travel question
curl -X POST http://<EC2_PUBLIC_IP>:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the best places to visit in Paris?"}'
```

## Troubleshooting

### Ollama not responding

```bash
# Check if Ollama service is running
ps aux | grep ollama

# Start Ollama if not running
ollama serve &

# Check logs
journalctl -u ollama -f
```

### Docker container issues

```bash
# Check container logs
sudo docker logs travel-app

# Restart container
sudo docker restart travel-app

# Check if port 8000 is in use
sudo netstat -tlnp | grep 8000
```

### Connection refused from application to Ollama

```bash
# Verify network mode is host
sudo docker inspect travel-app | grep NetworkMode

# Should show: "NetworkMode": "host"
```

### Model not loaded

```bash
# List available models
ollama list

# Pull phi3 if missing
ollama pull phi3
```

## Cost Optimization

### Stop Instance When Not in Use

```bash
# In AWS Console:
# Instances -> Select instance -> Instance state -> Stop

# Note: Public IP will change on restart
# Update your Postman/API client with new IP
```

### Estimated Costs

- **Running**: ~$0.17/hour (~$122/month)
- **Stopped**: ~$0.10/month (EBS storage only)

## Security Notes

- No authentication implemented
- Firewall configured via Security Groups
- Keep instance stopped when not in use
- Monitor AWS billing

## Architecture

```
┌─────────────────────────────────────┐
│         EC2 t3.xlarge               │
│  ┌──────────────────────────────┐   │
│  │   Docker Container           │   │
│  │   (--network host)           │   │
│  │                              │   │
│  │   FastAPI App                │   │
│  │   Port: 8000                 │   │
│  │                              │   │
│  └──────────┬───────────────────┘   │
│             │ localhost:11434       │
│             ▼                        │
│  ┌──────────────────────────────┐   │
│  │   Ollama (Native)            │   │
│  │   Model: phi3                │   │
│  │   Port: 11434                │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
```

## Endpoints

### GET /health

Returns application status.

**Response:**
```json
{
  "status": "running"
}
```

### POST /ask

Submit travel-related queries.

**Request:**
```json
{
  "query": "What is the best time to visit Tokyo?"
}
```

**Response:**
```json
{
  "query": "What is the best time to visit Tokyo?",
  "response": "The best time to visit Tokyo is during spring (March-May) or fall (September-November)..."
}
```

## Validation

- Query length: 1-1000 characters
- Query field is required
- Automatic timeout: 60 seconds
- Error handling for Ollama unavailability
