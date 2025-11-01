#!/bin/bash

################################################################################
# TAIWANTEA Quick Deployment Script
#
# Simple script that only updates the remote container without rebuilding
# Use this when the image is already on Docker Hub
#
# Usage: ./quick-deploy.sh
################################################################################

set -e

# Configuration
REMOTE_HOST="databack"
CONTAINER_NAME="taiwantea-app"
IMAGE_NAME="howardweng/taiwantea:latest"

echo "🚀 Quick deploying TAIWANTEA..."
echo ""
echo "→ Pulling latest image on remote server"
ssh "${REMOTE_HOST}" "docker pull ${IMAGE_NAME}"

echo "→ Restarting container"
ssh "${REMOTE_HOST}" "docker restart ${CONTAINER_NAME}"

echo "→ Waiting for service to be ready..."
sleep 5

echo "→ Checking container status"
ssh "${REMOTE_HOST}" "docker ps | grep ${CONTAINER_NAME}"

echo ""
echo "✅ Quick deployment complete!"
echo ""
echo "Access at: https://taiwantea.frrut.com"
