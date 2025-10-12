# TAIWANTEA Docker Run Commands

## Single Container Deployment with `docker run`

---

## 🚀 Quick Start

### Build the Image

```bash
docker build -t taiwantea:latest .
```

### Run the Container

```bash
docker run -d \
  --name taiwantea-app \
  --restart unless-stopped \
  -p 7070:7070 \
  -e MONGODB_URL="mongodb://YOUR_USERNAME:YOUR_PASSWORD@YOUR_HOST:2700/taiwantea?authSource=admin" \
  -e DATABASE_NAME="taiwantea" \
  -e SECRET_KEY="YOUR-SECURE-SECRET-KEY-CHANGE-THIS" \
  -e JWT_ALGORITHM="HS256" \
  -e ACCESS_TOKEN_EXPIRE_MINUTES="15" \
  -e REFRESH_TOKEN_EXPIRE_DAYS="7" \
  -e ALLOWED_ORIGINS="http://YOUR_VM_IP:7070,http://your-domain.com:7070" \
  -e UPLOAD_DIR="/app/uploads" \
  -e MAX_FILE_SIZE="5242880" \
  -e ALLOWED_IMAGE_TYPES="image/jpeg,image/png,image/webp" \
  -e ENVIRONMENT="production" \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/logs:/var/log/supervisor \
  taiwantea:latest
```

---

## 📋 Command Breakdown

### Flags Explained

- `-d` - Run in detached mode (background)
- `--name taiwantea-app` - Container name
- `--restart unless-stopped` - Auto-restart on failure
- `-p 7070:7070` - Port mapping (host:container)
- `-e` - Environment variables
- `-v` - Volume mounts for data persistence

### Environment Variables

| Variable | Description | Default/Example |
|----------|-------------|-----------------|
| `MONGODB_URL` | Remote MongoDB connection string | Required |
| `DATABASE_NAME` | Database name | `taiwantea` |
| `SECRET_KEY` | JWT secret key | **CHANGE IN PRODUCTION** |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry | `15` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token expiry | `7` |
| `ALLOWED_ORIGINS` | CORS origins | Your VM IP/domain |
| `UPLOAD_DIR` | Upload directory | `/app/uploads` |
| `MAX_FILE_SIZE` | Max upload size (bytes) | `5242880` (5MB) |
| `ALLOWED_IMAGE_TYPES` | Allowed image types | `image/jpeg,image/png,image/webp` |
| `ENVIRONMENT` | Environment mode | `production` |

### Volume Mounts

- `$(pwd)/uploads:/app/uploads` - Persist uploaded images
- `$(pwd)/logs:/var/log/supervisor` - Persist logs

---

## 🔧 Container Management

### Check Status

```bash
docker ps | grep taiwantea-app
```

### View Logs

```bash
# All logs
docker logs taiwantea-app

# Follow logs
docker logs -f taiwantea-app

# Last 50 lines
docker logs taiwantea-app --tail 50
```

### Stop Container

```bash
docker stop taiwantea-app
```

### Start Container

```bash
docker start taiwantea-app
```

### Restart Container

```bash
docker restart taiwantea-app
```

### Remove Container

```bash
docker stop taiwantea-app
docker rm taiwantea-app
```

### Access Container Shell

```bash
docker exec -it taiwantea-app /bin/bash
```

---

## 🔄 Update and Rebuild

### Update Application

```bash
# Stop and remove old container
docker stop taiwantea-app
docker rm taiwantea-app

# Rebuild image
docker build -t taiwantea:latest .

# Run new container (use the docker run command above)
```

---

## 🧪 Test Container

### Health Check

```bash
curl http://localhost:7070/api/health
```

Expected output:
```json
{
  "success": true,
  "message": "API is healthy",
  "data": {
    "database": "connected",
    "version": "1.0.0"
  }
}
```

### Test Frontend

```bash
curl -I http://localhost:7070/
```

Should return: `HTTP/1.1 200 OK`

### Test API

```bash
curl http://localhost:7070/api/products
```

### Access in Browser

- Frontend: http://YOUR_VM_IP:7070
- Admin: http://YOUR_VM_IP:7070/admin/login
- API Docs: http://YOUR_VM_IP:7070/docs

---

## 📊 Monitor Container

### Resource Usage

```bash
docker stats taiwantea-app
```

### Inspect Container

```bash
docker inspect taiwantea-app
```

### Check Health Status

```bash
docker inspect --format='{{.State.Health.Status}}' taiwantea-app
```

---

## 🛑 Troubleshooting

### Container Exits Immediately

```bash
# Check logs
docker logs taiwantea-app

# Check if port 7070 is available
sudo netstat -tulpn | grep 7070
```

### Can't Connect to Database

```bash
# Test MongoDB connection
docker exec -it taiwantea-app python3 -c "
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
async def test():
    client = AsyncIOMotorClient('mongodb://YOUR_USERNAME:YOUR_PASSWORD@YOUR_HOST:2700/taiwantea?authSource=admin')
    await client.admin.command('ping')
    print('✓ Connected')
asyncio.run(test())
"
```

### Permission Issues

```bash
# Fix upload permissions
docker exec taiwantea-app chmod -R 755 /app/uploads
```

### View Nginx Logs

```bash
docker exec taiwantea-app tail -f /var/log/nginx/access.log
docker exec taiwantea-app tail -f /var/log/nginx/error.log
```

### View FastAPI Logs

```bash
docker exec taiwantea-app tail -f /var/log/supervisor/fastapi.log
```

---

## 🔐 Security Notes

### Before Production:

1. **Generate secure SECRET_KEY:**
   ```bash
   python3 -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Update ALLOWED_ORIGINS** with your actual domain/IP

3. **Open firewall port:**
   ```bash
   # Ubuntu/Debian
   sudo ufw allow 7070/tcp

   # CentOS/RHEL
   sudo firewall-cmd --permanent --add-port=7070/tcp
   sudo firewall-cmd --reload
   ```

---

## 📝 Alternative: Using Environment File

### Create `.env.production` file:

```bash
MONGODB_URL=mongodb://YOUR_USERNAME:YOUR_PASSWORD@YOUR_HOST:2700/taiwantea?authSource=admin
DATABASE_NAME=taiwantea
SECRET_KEY=YOUR-SECURE-SECRET-KEY
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
ALLOWED_ORIGINS=http://YOUR_VM_IP:7070
UPLOAD_DIR=/app/uploads
MAX_FILE_SIZE=5242880
ALLOWED_IMAGE_TYPES=image/jpeg,image/png,image/webp
ENVIRONMENT=production
```

### Run with env file:

```bash
docker run -d \
  --name taiwantea-app \
  --restart unless-stopped \
  -p 7070:7070 \
  --env-file .env.production \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/logs:/var/log/supervisor \
  taiwantea:latest
```

---

## ✅ Verification Checklist

After running the container:

- [ ] Container is running: `docker ps | grep taiwantea-app`
- [ ] Health check passes: `curl http://localhost:7070/api/health`
- [ ] Frontend loads: `curl http://localhost:7070/`
- [ ] API responds: `curl http://localhost:7070/api/products`
- [ ] No errors in logs: `docker logs taiwantea-app`
- [ ] Can access from browser: `http://YOUR_VM_IP:7070`

---

## 🎉 Success!

Your TAIWANTEA application is now running in a single Docker container!

For more information:
- Full deployment guide: `DEPLOYMENT.md`
- Quick deploy guide: `QUICK_DEPLOY.md`
- Test results: `TEST_RESULTS.md`
