# Testing Guide

## Local Testing with Docker

### Build and Run Locally

```bash
# Build image
docker build -t travel-app .

# Run with network host mode
docker run -d --name travel-app --network host travel-app

# Check logs
docker logs travel-app
```

## API Testing

### Health Check

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "running"
}
```

### Ask Travel Question

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the best places to visit in Paris?"
  }'
```

**Expected Response:**
```json
{
  "query": "What are the best places to visit in Paris?",
  "response": "Paris offers many wonderful attractions including the Eiffel Tower, Louvre Museum, Notre-Dame Cathedral..."
}
```

## Validation Testing

### Test 1: Empty Query

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "query": ""
  }'
```

**Expected:** 422 Validation Error

### Test 2: Query Too Long

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"$(python3 -c 'print("a" * 1001)')\"
  }"
```

**Expected:** 422 Validation Error

### Test 3: Missing Query Field

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Expected:** 422 Validation Error

## Error Scenarios

### Test: Ollama Not Running

```bash
# Stop Ollama
sudo systemctl stop ollama

# Try request
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Test query"
  }'
```

**Expected Response:**
```json
{
  "detail": "Cannot connect to Ollama service. Make sure Ollama is running on localhost:11434"
}
```

**Status Code:** 503

## Postman Collection

### Health Check Request

```
Method: GET
URL: http://<EC2_PUBLIC_IP>:8000/health
```

### Ask Question Request

```
Method: POST
URL: http://<EC2_PUBLIC_IP>:8000/ask
Headers:
  Content-Type: application/json
Body (raw JSON):
{
  "query": "What is the best time to visit Tokyo?"
}
```

## Sample Travel Queries

1. "What documents do I need to travel to Japan?"
2. "Best budget hotels in Rome?"
3. "How to get from Paris to Amsterdam?"
4. "What vaccinations are required for Brazil?"
5. "Top 5 beaches in Thailand?"
6. "Local cuisine recommendations in Mexico City?"
7. "Safety tips for traveling in Egypt?"
8. "Best hiking trails in Switzerland?"
9. "Currency exchange tips for Europe?"
10. "Must-see attractions in New York City?"

## Performance Testing

### Test Response Time

```bash
time curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Best time to visit London?"
  }'
```

**Note:** First request may take longer as model loads

### Concurrent Requests

```bash
# Install Apache Bench
sudo yum install -y httpd-tools

# Run 100 requests with 10 concurrent
ab -n 100 -c 10 -p query.json -T application/json \
  http://localhost:8000/ask
```

**query.json:**
```json
{
  "query": "What are the best places to visit in Paris?"
}
```

## Monitoring

### Check Application Logs

```bash
docker logs -f travel-app
```

### Check Ollama Service

```bash
# Check if running
ps aux | grep ollama

# Check Ollama logs
journalctl -u ollama -f
```

### Monitor Resources

```bash
# CPU and Memory usage
docker stats travel-app

# System resources
htop
```

## Troubleshooting

### Application Returns 503

**Cause:** Ollama not running or not responding

**Solution:**
```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Restart Ollama if needed
ollama serve &
```

### Slow Response Times

**Cause:** Model loading or insufficient resources

**Solution:**
- Use t3.xlarge instance (minimum)
- Wait for first request to load model
- Consider using smaller model for faster responses

### Connection Refused

**Cause:** Container not using host network

**Solution:**
```bash
# Check network mode
docker inspect travel-app | grep NetworkMode

# Should show: "NetworkMode": "host"

# If not, recreate container with --network host
docker stop travel-app
docker rm travel-app
docker run -d --name travel-app --network host travel-app
```

## Cleanup

```bash
# Stop container
docker stop travel-app

# Remove container
docker rm travel-app

# Remove image
docker rmi travel-app

# Stop Ollama
sudo systemctl stop ollama
```
