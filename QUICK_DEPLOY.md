# TAIWANTEA Quick Deployment Guide

## Single Container - Port 7070

---

## 📦 What You Get

**ONE Docker container containing:**
- ✅ Nginx (serves frontend + reverse proxy)
- ✅ FastAPI backend
- ✅ Supervisord (process manager)
- ✅ All built and ready to go

**External Port:** 7070
**Image Size:** 322MB

---

## 🚀 Deploy to Remote VM

### 1. Prerequisites on VM

```bash
# Ensure Docker is installed
docker --version

# Ensure Docker Compose is installed
docker compose version

# Check if port 7070 is available
sudo netstat -tulpn | grep 7070
# or
ss -tlnp | grep :7070
```

### 2. Upload Files to VM

Upload these files to your VM:
- `Dockerfile`
- `docker-compose.production.yml`
- `nginx.conf`
- `supervisord.conf`
- `backend/` directory
- `frontend/` directory
- `.dockerignore`

```bash
# Example using rsync
rsync -avz --exclude 'node_modules' --exclude '.venv' \
  /local/path/TAIWANTEA/ user@VM_IP:/path/to/TAIWANTEA/
```

### 3. Update Configuration

Edit `docker-compose.production.yml`:

```yaml
environment:
  # Update with your VM's IP or domain
  - ALLOWED_ORIGINS=http://YOUR_VM_IP:7070,http://your-domain.com:7070

  # IMPORTANT: Generate a secure secret key
  - SECRET_KEY=YOUR_SECURE_RANDOM_KEY_HERE
```

Generate secure key:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. Build and Deploy

```bash
# Navigate to project directory
cd /path/to/TAIWANTEA

# Build the image
docker compose -f docker-compose.production.yml build

# Start the container
docker compose -f docker-compose.production.yml up -d

# Check logs
docker compose -f docker-compose.production.yml logs -f
```

### 5. Verify Deployment

```bash
# Check container is running
docker ps | grep taiwantea-app

# Test health endpoint
curl http://localhost:7070/api/health

# Test frontend
curl http://localhost:7070

# View logs
docker logs taiwantea-app
```

### 6. Open Firewall Port

```bash
# Ubuntu/Debian
sudo ufw allow 7070/tcp
sudo ufw reload

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=7070/tcp
sudo firewall-cmd --reload
```

---

## 🌐 Access Your Application

- **Frontend:** `http://YOUR_VM_IP:7070`
- **Admin Login:** `http://YOUR_VM_IP:7070/admin/login`
- **API Docs:** `http://YOUR_VM_IP:7070/docs`
- **Health Check:** `http://YOUR_VM_IP:7070/api/health`

**Default Admin Credentials:**
- Email: `admin@taiwantea.com`
- Password: `Admin123!`

---

## 🔧 Container Management

### View Logs

```bash
# All logs
docker compose -f docker-compose.production.yml logs -f

# Last 100 lines
docker logs taiwantea-app --tail 100

# Follow logs
docker logs taiwantea-app -f
```

### Restart Container

```bash
docker compose -f docker-compose.production.yml restart
```

### Stop Container

```bash
docker compose -f docker-compose.production.yml stop
```

### Start Container

```bash
docker compose -f docker-compose.production.yml start
```

### Rebuild and Restart

```bash
docker compose -f docker-compose.production.yml up -d --build
```

### Remove Container

```bash
docker compose -f docker-compose.production.yml down
```

---

## 📊 Monitor Container

### Check Status

```bash
# Container status
docker ps | grep taiwantea-app

# Resource usage
docker stats taiwantea-app

# Health status
docker inspect --format='{{.State.Health.Status}}' taiwantea-app
```

### Access Container Shell

```bash
docker exec -it taiwantea-app /bin/bash
```

### Check Services Inside Container

```bash
# View Nginx logs
docker exec taiwantea-app tail -f /var/log/nginx/access.log

# View FastAPI logs
docker exec taiwantea-app tail -f /var/log/supervisor/fastapi.log

# View all supervisor logs
docker exec taiwantea-app tail -f /var/log/supervisor/*.log
```

---

## 🔄 Update Deployment

When you make changes:

```bash
# Pull latest code
git pull

# Rebuild and restart
docker compose -f docker-compose.production.yml up -d --build
```

---

## 🛑 Troubleshooting

### Container won't start

```bash
# Check logs
docker compose -f docker-compose.production.yml logs

# Check port availability
sudo netstat -tulpn | grep 7070
```

### Can't access from browser

```bash
# Check firewall
sudo ufw status
sudo firewall-cmd --list-ports

# Check container is running
docker ps | grep taiwantea-app

# Check nginx logs
docker logs taiwantea-app | grep nginx
```

### Database connection issues

```bash
# Test MongoDB connection
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

### Permission issues

```bash
# Fix upload directory permissions
docker exec taiwantea-app chmod -R 755 /app/uploads
```

---

## 📝 Important Notes

1. **Port 7070** must be available on your VM
2. **Secret Key** must be changed in production
3. **ALLOWED_ORIGINS** must include your domain/IP
4. **Firewall** must allow port 7070
5. **MongoDB** connection is to remote server (YOUR_HOST:2700)
6. **Uploads** are persisted in `./uploads` directory
7. **Logs** are persisted in `./logs` directory

---

## ✅ Production Checklist

Before going live:

- [ ] Change `SECRET_KEY` to secure random value
- [ ] Update `ALLOWED_ORIGINS` with production domain
- [ ] Open firewall port 7070
- [ ] Test all endpoints
- [ ] Verify MongoDB connection
- [ ] Check admin login works
- [ ] Set up SSL/TLS (optional)
- [ ] Configure backup for uploads
- [ ] Set up monitoring

---

## 🎉 That's It!

Your TAIWANTEA application is now running in a single Docker container on port 7070!

For detailed information, see:
- `DEPLOYMENT.md` - Full deployment guide
- `TEST_RESULTS.md` - Test results and verification
- `CLAUDE.md` - Development guide
