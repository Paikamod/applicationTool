#!/bin/bash
echo ">>> Pulling latest code..."
git pull

echo ">>> Rebuilding Docker image..."
docker compose build

echo ">>> Restarting container..."
docker compose up -d

echo ">>> Done! App is running on port 8000"
