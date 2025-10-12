# Multi-stage build for TAIWANTEA - Single Container Deployment
# Stage 1: Build Frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /frontend

# Copy frontend package files
COPY frontend/package*.json ./
RUN npm ci

# Copy frontend source
COPY frontend/ ./

# Create production .env file for build
RUN echo "VITE_API_URL=" > .env.production && \
    echo "VITE_ENV=production" >> .env.production

# Build frontend for production
RUN npm run build

# Stage 2: Final Image with Backend + Nginx
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./

# Copy frontend build from stage 1
COPY --from=frontend-builder /frontend/dist /usr/share/nginx/html

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Create uploads directory
RUN mkdir -p /app/uploads && chmod 755 /app/uploads

# Create log directories
RUN mkdir -p /var/log/supervisor /var/log/nginx /var/log/uwsgi

# Expose port 7070
EXPOSE 7070

# Start supervisor (manages both Nginx and FastAPI)
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
