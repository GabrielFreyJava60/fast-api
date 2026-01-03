# Quick Start Guide

## 1. Launch EC2

```bash
Instance Type: t3.xlarge
AMI: Amazon Linux 2023
Security Group: Allow inbound TCP 8000
```

## 2. Connect & Clone

```bash
git clone https://github.com/GabrielFreyJava60/fast-api.git
cd fast-api
git checkout hw-46
```

## 3. Setup EC2

```bash
chmod +x setup_ec2.sh
./setup_ec2.sh
```

Wait 5-10 minutes for model download.

## 4. Create ECR Repository

AWS Console → ECR → Create repository → Name: `travel-app`

## 5. Add IAM Role

EC2 → Instance → Actions → Security → Modify IAM role → Add `AWSAppRunnerServicePolicyForECRAccess`

## 6. Update deploy.sh

```bash
nano deploy.sh
# Change REGION and ACCOUNT_ID
```

## 7. Deploy

```bash
chmod +x deploy.sh
./deploy.sh
```

## 8. Test

```bash
# Health check
curl http://<PUBLIC_IP>:8000/health

# Ask question
curl -X POST http://<PUBLIC_IP>:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "Best time to visit Paris?"}'
```

## Done!

Your Travel Info API is running on port 8000.

## Cost Saving

Stop instance when not in use:
- Running: ~$0.17/hour
- Stopped: ~$0.10/month

AWS Console → EC2 → Instances → Stop Instance

## Troubleshooting

### Ollama not responding
```bash
ollama serve &
```

### Check logs
```bash
sudo docker logs travel-app
```

### Restart container
```bash
sudo docker restart travel-app
```
