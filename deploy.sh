#!/bin/bash

set -e

REGION="<region>"
ACCOUNT_ID="<account_id>"
ECR_REPOSITORY="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"
IMAGE_NAME="travel-app"
IMAGE_TAG="${ECR_REPOSITORY}/${IMAGE_NAME}:latest"

echo "Logging into ECR..."
aws ecr get-login-password --region ${REGION} | sudo docker login --username AWS --password-stdin ${ECR_REPOSITORY}

echo "Building Docker image..."
sudo docker build -t ${IMAGE_NAME} .

echo "Tagging image..."
sudo docker tag ${IMAGE_NAME}:latest ${IMAGE_TAG}

echo "Pushing image to ECR..."
sudo docker push ${IMAGE_TAG}

echo "Stopping and removing old container..."
sudo docker stop travel-app 2>/dev/null || true
sudo docker rm travel-app 2>/dev/null || true

echo "Running new container..."
sudo docker run -d --name travel-app --network host ${IMAGE_TAG}

echo "Deployment completed successfully!"
echo "Application is running on port 8000"
