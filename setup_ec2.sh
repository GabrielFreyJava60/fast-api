#!/bin/bash

set -e

echo "Installing Docker..."
sudo yum install -y docker

echo "Enabling Docker service..."
sudo systemctl enable --now docker

echo "Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

echo "Pulling phi3 model..."
ollama pull phi3

echo "Setup completed successfully!"
