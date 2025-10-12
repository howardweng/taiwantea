# TAIWANTEA Deployment Guide - Single Container

This guide explains how to deploy TAIWANTEA as a single Docker container on a remote VM.

## Architecture

**Single Container includes:**
- Nginx (serves frontend + reverse proxy on port 7070)
- FastAPI Backend (runs on internal port 8585)
- Supervisord (manages both processes)

**External Dependencies:**
- Remote MongoDB at `YOUR_HOST:2700`

## Prerequisites

On your remote VM:
- Docker installed
- Docker Compose installed
- Port 7070 open in firewall
- Network access to MongoDB server (YOUR_HOST:2700)

## Deployment Steps

### 1. Clone Repository on Remote VM

```bash
git clone <your-repo-url>
cd TAIWANTEA
```

### 2. Update Environment Variables

Edit `docker-compose.production.yml` and update:
- `ALLOWED_ORIGINS` - Add your VM's IP or domain
- `SECRET_KEY` - Generate a secure random key

```bash
# Generate a secure secret key
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Build and Start Container

```bash
# Build the image
docker-compose -f docker-compose.production.yml build

# Start the container
docker-compose -f docker-compose.production.yml up -d

# Check logs
docker-compose -f docker-compose.production.yml logs -f
```

### 4. Verify Deployment

```bash
# Check container status
docker ps

# Check health
curl http://localhost:7070/api/health

# Test frontend
curl http://localhost:7070
```

### 5. Access Application

- **Frontend**: http://YOUR_VM_IP:7070
- **Admin Dashboard**: http://YOUR_VM_IP:7070/admin/login
- **API Docs**: http://YOUR_VM_IP:7070/docs
- **Health Check**: http://YOUR_VM_IP:7070/api/health

**Default Admin Credentials:**
- Email: `admin@taiwantea.com`
- Password: `Admin123!`

## Container Management

### View Logs

```bash
# All logs
docker-compose -f docker-compose.production.yml logs -f

# Nginx logs
docker exec taiwantea-app tail -f /var/log/nginx/access.log

# FastAPI logs
docker exec taiwantea-app tail -f /var/log/supervisor/fastapi.log

# Supervisor logs
docker exec taiwantea-app tail -f /var/log/supervisor/supervisord.log
```

### Restart Services

```bash
# Restart entire container
docker-compose -f docker-compose.production.yml restart

# Restart only FastAPI (inside container)
docker exec taiwantea-app supervisorctl restart fastapi

# Restart only Nginx (inside container)
docker exec taiwantea-app supervisorctl restart nginx
```

### Stop/Start Container

```bash
# Stop
docker-compose -f docker-compose.production.yml stop

# Start
docker-compose -f docker-compose.production.yml start

# Down (remove container)
docker-compose -f docker-compose.production.yml down
```

### Update Deployment

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose -f docker-compose.production.yml up -d --build
```

## Data Persistence

The following directories are persisted:
- `./uploads` - Product images
- `./logs` - Application logs

## Firewall Configuration

On your VM, ensure port 7070 is open:

```bash
# Ubuntu/Debian with ufw
sudo ufw allow 7070/tcp

# CentOS/RHEL with firewalld
sudo firewall-cmd --permanent --add-port=7070/tcp
sudo firewall-cmd --reload
```

## Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose -f docker-compose.production.yml logs

# Check if port 7070 is already in use
sudo netstat -tulpn | grep 7070
```

### Can't connect to MongoDB

```bash
# Test MongoDB connection from container
docker exec -it taiwantea-app python3 -c "
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
async def test():
    client = AsyncIOMotorClient('mongodb://YOUR_USERNAME:YOUR_PASSWORD@YOUR_HOST:2700/taiwantea?authSource=admin')
    await client.admin.command('ping')
    print('✓ MongoDB connected')
asyncio.run(test())
"
```

### Backend not responding

```bash
# Check if FastAPI is running
docker exec taiwantea-app supervisorctl status

# Check FastAPI logs
docker exec taiwantea-app tail -f /var/log/supervisor/fastapi.log

# Restart FastAPI
docker exec taiwantea-app supervisorctl restart fastapi
```

### Frontend not loading

```bash
# Check Nginx status
docker exec taiwantea-app supervisorctl status nginx

# Check Nginx logs
docker exec taiwantea-app tail -f /var/log/nginx/error.log

# Restart Nginx
docker exec taiwantea-app supervisorctl restart nginx
```

### Permission issues with uploads

```bash
# Fix upload directory permissions
docker exec taiwantea-app chmod -R 755 /app/uploads
```

## Production Checklist

Before going to production:

- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Update `ALLOWED_ORIGINS` with your production domain
- [ ] Ensure MongoDB credentials are secure
- [ ] Configure firewall to allow port 7070
- [ ] Set up SSL/TLS (optional, use Nginx with certbot)
- [ ] Configure backup for uploaded images
- [ ] Set up monitoring and alerting
- [ ] Test all functionality on production environment
- [ ] Document your production domain and credentials

## Monitoring

### Check Container Health

```bash
# Container health status
docker inspect --format='{{.State.Health.Status}}' taiwantea-app

# Resource usage
docker stats taiwantea-app
```

### Monitor Logs

```bash
# Real-time logs for all services
docker exec taiwantea-app tail -f /var/log/supervisor/*.log
```

## Backup

### Backup Uploaded Images

```bash
# Create backup
tar -czf uploads-backup-$(date +%Y%m%d).tar.gz uploads/

# Restore backup
tar -xzf uploads-backup-YYYYMMDD.tar.gz
```

## Additional Notes

- The container runs both Nginx and FastAPI using supervisord
- Nginx listens on port 7070 externally
- FastAPI runs on internal port 8585 (not exposed externally)
- All API requests go through Nginx proxy at `/api/*`
- Static frontend files are served by Nginx from `/usr/share/nginx/html`
- Uploaded images are served by Nginx from `/app/uploads/`

## Support

For issues or questions:
- Check logs first
- Review this documentation
- Check GitHub issues
