#!/bin/bash
echo "Pulling latest images..."
docker compose pull

echo "Stopping containers..."
docker compose down

echo "Starting containers..."
docker compose up -d

echo "Cleaning unused Docker resources..."
docker system prune -f