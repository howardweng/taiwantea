#!/bin/bash

################################################################################
# TAIWANTEA Production Deployment Script
#
# This script automates the deployment process:
# 1. Builds Docker image locally
# 2. Pushes to Docker Hub
# 3. SSHs to production server
# 4. Pulls latest image
# 5. Restarts container
#
# Usage: ./deploy-to-production.sh [version]
# Example: ./deploy-to-production.sh v1.0.0
################################################################################

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DOCKER_HUB_USER="howardweng"
IMAGE_NAME="taiwantea"
REMOTE_HOST="databack"
CONTAINER_NAME="taiwantea-app"
PORT="7070"
UPLOAD_DIR="/root/taiwantea/uploads"
LOG_DIR="/root/taiwantea/logs"

# MongoDB configuration (from container inspect)
MONGODB_URL="mongodb://datavanadmin:datavanabcbvf@172.17.0.1:2700/taiwantea?authSource=admin"
ALLOWED_ORIGINS="https://taiwantea.frrut.com,http://128.199.112.130:7070"
SECRET_KEY="taiwantea-prod-secret-key-change-this"

# Version tag (default to latest if not provided)
VERSION="${1:-latest}"
FULL_IMAGE_NAME="${DOCKER_HUB_USER}/${IMAGE_NAME}:${VERSION}"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  TAIWANTEA Production Deployment${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}Image:${NC} ${FULL_IMAGE_NAME}"
echo -e "${YELLOW}Remote:${NC} ${REMOTE_HOST}"
echo -e "${YELLOW}Container:${NC} ${CONTAINER_NAME}"
echo ""

# Function to print section headers
print_section() {
    echo -e "\n${BLUE}==>${NC} ${1}"
}

# Function to print success messages
print_success() {
    echo -e "${GREEN}✓${NC} ${1}"
}

# Function to print error messages
print_error() {
    echo -e "${RED}✗${NC} ${1}"
}

# Function to print info messages
print_info() {
    echo -e "${YELLOW}→${NC} ${1}"
}

# Step 1: Build Docker image
print_section "Step 1: Building Docker image"
print_info "Building image: ${FULL_IMAGE_NAME}"

if docker build -t "${FULL_IMAGE_NAME}" .; then
    print_success "Docker image built successfully"
else
    print_error "Failed to build Docker image"
    exit 1
fi

# Also tag as latest if a specific version was provided
if [ "$VERSION" != "latest" ]; then
    print_info "Tagging as latest"
    docker tag "${FULL_IMAGE_NAME}" "${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
fi

# Step 2: Push to Docker Hub
print_section "Step 2: Pushing to Docker Hub"
print_info "Pushing ${FULL_IMAGE_NAME}"

if docker push "${FULL_IMAGE_NAME}"; then
    print_success "Image pushed to Docker Hub"
else
    print_error "Failed to push to Docker Hub"
    exit 1
fi

# Push latest tag if version was specified
if [ "$VERSION" != "latest" ]; then
    print_info "Pushing latest tag"
    docker push "${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
fi

# Step 3: Test SSH connection
print_section "Step 3: Testing SSH connection"
print_info "Connecting to ${REMOTE_HOST}"

if ssh -o ConnectTimeout=10 "${REMOTE_HOST}" "echo 'SSH connection successful'"; then
    print_success "SSH connection established"
else
    print_error "Failed to connect to remote server"
    exit 1
fi

# Step 4: Deploy to production server
print_section "Step 4: Deploying to production"

# Create deployment script to run on remote server
DEPLOY_SCRIPT=$(cat << 'EOF'
#!/bin/bash
set -e

IMAGE_NAME="$1"
CONTAINER_NAME="$2"
PORT="$3"
UPLOAD_DIR="$4"
LOG_DIR="$5"
MONGODB_URL="$6"
ALLOWED_ORIGINS="$7"
SECRET_KEY="$8"

echo "→ Pulling latest image: ${IMAGE_NAME}"
docker pull "${IMAGE_NAME}"

echo "→ Stopping old container: ${CONTAINER_NAME}"
docker stop "${CONTAINER_NAME}" 2>/dev/null || echo "Container not running"

echo "→ Removing old container: ${CONTAINER_NAME}"
docker rm "${CONTAINER_NAME}" 2>/dev/null || echo "Container not found"

echo "→ Starting new container: ${CONTAINER_NAME}"
docker run -d \
    --name "${CONTAINER_NAME}" \
    --restart unless-stopped \
    -p "${PORT}:${PORT}" \
    -v "${UPLOAD_DIR}:/app/uploads" \
    -v "${LOG_DIR}:/app/logs" \
    -e "MONGODB_URL=${MONGODB_URL}" \
    -e "DATABASE_NAME=taiwantea" \
    -e "SECRET_KEY=${SECRET_KEY}" \
    -e "JWT_ALGORITHM=HS256" \
    -e "ACCESS_TOKEN_EXPIRE_MINUTES=15" \
    -e "ALLOWED_ORIGINS=${ALLOWED_ORIGINS}" \
    -e "ENVIRONMENT=production" \
    "${IMAGE_NAME}"

echo "→ Waiting for container to be healthy..."
sleep 5

echo "→ Checking container status"
docker ps | grep "${CONTAINER_NAME}"

echo "→ Checking health endpoint"
curl -f http://localhost:${PORT}/api/health || echo "Health check pending..."

echo "✓ Deployment complete!"
EOF
)

# Execute deployment on remote server
print_info "Executing deployment on remote server"

if ssh "${REMOTE_HOST}" "bash -s" -- \
    "${FULL_IMAGE_NAME}" \
    "${CONTAINER_NAME}" \
    "${PORT}" \
    "${UPLOAD_DIR}" \
    "${LOG_DIR}" \
    "${MONGODB_URL}" \
    "${ALLOWED_ORIGINS}" \
    "${SECRET_KEY}" <<< "${DEPLOY_SCRIPT}"; then
    print_success "Remote deployment completed"
else
    print_error "Remote deployment failed"
    exit 1
fi

# Step 5: Verify deployment
print_section "Step 5: Verifying deployment"

print_info "Checking container status"
ssh "${REMOTE_HOST}" "docker ps | grep ${CONTAINER_NAME}" || {
    print_error "Container is not running"
    exit 1
}

print_info "Testing health endpoint"
if curl -f -s "https://taiwantea.frrut.com/api/health" > /dev/null 2>&1 || \
   curl -f -s "http://128.199.112.130:7070/api/health" > /dev/null 2>&1; then
    print_success "Health check passed"
else
    print_error "Health check failed (service may still be starting)"
fi

print_info "Checking recent logs"
ssh "${REMOTE_HOST}" "docker logs --tail 20 ${CONTAINER_NAME}"

# Step 6: Cleanup old images
print_section "Step 6: Cleaning up old images"
print_info "Removing unused Docker images on remote server"

ssh "${REMOTE_HOST}" "docker image prune -f" || print_info "No images to remove"

# Summary
print_section "Deployment Summary"
echo ""
echo -e "${GREEN}✓ Deployment successful!${NC}"
echo ""
echo -e "${YELLOW}Access your application at:${NC}"
echo -e "  • https://taiwantea.frrut.com"
echo -e "  • http://128.199.112.130:7070"
echo ""
echo -e "${YELLOW}Useful commands:${NC}"
echo -e "  • View logs: ${BLUE}ssh ${REMOTE_HOST} 'docker logs -f ${CONTAINER_NAME}'${NC}"
echo -e "  • Restart:   ${BLUE}ssh ${REMOTE_HOST} 'docker restart ${CONTAINER_NAME}'${NC}"
echo -e "  • Stop:      ${BLUE}ssh ${REMOTE_HOST} 'docker stop ${CONTAINER_NAME}'${NC}"
echo -e "  • Status:    ${BLUE}ssh ${REMOTE_HOST} 'docker ps | grep ${CONTAINER_NAME}'${NC}"
echo ""
print_success "All done! 🎉"
