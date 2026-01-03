# Travel Info Application with FastAPI and Ollama

FastAPI application with Ollama phi3 model for travel-related queries on AWS EC2.

## Architecture

- **FastAPI Application**: Runs in Docker container with --network host mode
- **Ollama Service**: Runs natively on EC2 host (not containerized)
- **Model**: phi3
- **EC2 Instance**: t3.xlarge with Amazon Linux 2023

## Setup

### 1. EC2 Setup

Run the setup script on your EC2 instance:

```bash
chmod +x setup_ec2.sh
./setup_ec2.sh
```

This will:
- Install Docker
- Enable Docker service
- Install Ollama
- Pull phi3 model

### 2. Deploy Application

Update deploy.sh with your AWS details:
- Replace `<region>` with your AWS region
- Replace `<account_id>` with your AWS account ID

Then run:

```bash
chmod +x deploy.sh
./deploy.sh
```

## API Endpoints

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "running"
}
```

### POST /ask

Ask travel-related questions.

**Request Body:**
```json
{
  "query": "What are the best places to visit in Paris?"
}
```

**Response:**
```json
{
  "query": "What are the best places to visit in Paris?",
  "response": "..."
}
```

## Testing

```bash
# Health check
curl http://<EC2_PUBLIC_IP>:8000/health

# Ask question
curl -X POST http://<EC2_PUBLIC_IP>:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the best places to visit in Paris?"}'
```

## Requirements

- AWS EC2 t3.xlarge instance
- Amazon Linux 2023
- Docker
- Ollama with phi3 model

## Security

No authentication is implemented. This is a demonstration application.

## Notes

- Application uses --network host mode to communicate with Ollama on localhost:11434
- Stop (not terminate) the EC2 instance when not in use to save costs
- Public IP will change after restart
