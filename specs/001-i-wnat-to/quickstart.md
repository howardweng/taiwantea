# Quickstart Guide: Tea Leaves E-Commerce Website

**Feature**: Tea Leaves E-Commerce Website
**Date**: 2025-10-08
**Purpose**: Step-by-step guide to set up and run the application locally

---

## Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **MongoDB 6.0+** - [Download](https://www.mongodb.com/try/download/community) or use Docker
- **Git** - [Download](https://git-scm.com/downloads)
- **Docker & Docker Compose** (optional, recommended) - [Download](https://www.docker.com/products/docker-desktop/)

---

## Quick Start (Docker Compose - Recommended)

The fastest way to get started is using Docker Compose, which sets up all services automatically.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd TAIWANTEA
git checkout 001-i-wnat-to
```

### 2. Create Environment Files

**Backend (.env)**:
```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env`:
```env
# Database
MONGODB_URL=mongodb://mongodb:27017/taiwantea

# Security
SECRET_KEY=your-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15

# CORS
ALLOWED_ORIGINS=http://localhost:5173

# File Upload
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=5242880  # 5MB in bytes
```

**Frontend (.env)**:
```bash
cp frontend/.env.example frontend/.env
```

Edit `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
```

### 3. Start All Services

```bash
docker-compose up -d
```

This command starts:
- MongoDB on port 27017
- FastAPI backend on port 8000
- React frontend on port 5173

### 4. Seed Initial Data

```bash
# Create admin user and seed categories
docker-compose exec backend python -m src.scripts.seed_data
```

Default admin credentials:
- Email: `admin@taiwantea.com`
- Password: `Admin123!`

### 5. Access the Application

- **Frontend**: http://localhost:5173
- **Admin Panel**: http://localhost:5173/admin
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative API Docs**: http://localhost:8000/redoc (ReDoc)

### 6. Stop Services

```bash
docker-compose down
```

To remove all data (reset database):
```bash
docker-compose down -v
```

---

## Manual Setup (Without Docker)

If you prefer to run services individually:

### 1. Set Up MongoDB

**Option A: Local MongoDB**
```bash
# Start MongoDB service
mongod --dbpath /path/to/data/directory
```

**Option B: MongoDB in Docker**
```bash
docker run -d -p 27017:27017 --name mongodb mongo:6
```

### 2. Set Up Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (see Docker section above)
cp .env.example .env
# Edit .env with your settings

# Run database migrations/seed data
python -m src.scripts.seed_data

# Start development server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at http://localhost:8000

### 3. Set Up Frontend

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Create .env file (see Docker section above)
cp .env.example .env
# Edit .env with your settings

# Start development server
npm run dev
```

Frontend will be available at http://localhost:5173

---

## Verify Installation

### 1. Check API Health

```bash
curl http://localhost:8000/api/health
```

Expected response:
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

### 2. Test Public Endpoints

**Get Categories**:
```bash
curl http://localhost:8000/api/categories
```

**Get Products**:
```bash
curl http://localhost:8000/api/products
```

### 3. Test Admin Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@taiwantea.com","password":"Admin123!"}'
```

### 4. Open Frontend

Navigate to http://localhost:5173 in your browser. You should see:
- Tea category sections
- Smooth scroll navigation menu
- Product cards with images and descriptions

### 5. Access Admin Panel

1. Navigate to http://localhost:5173/admin
2. Login with default credentials (admin@taiwantea.com / Admin123!)
3. You should see the product management dashboard

---

## Common Tasks

### Add a New Product (via Admin UI)

1. Login to admin panel (http://localhost:5173/admin)
2. Click "Add New Product"
3. Fill in product details:
   - Name: e.g., "Jasmine Pearl Green Tea"
   - Category: Select from dropdown
   - Description: Product details, origin, brewing instructions
   - Price: e.g., 19.99
   - Image: Upload a product image (max 5MB)
4. Click "Save Product"
5. Verify product appears on homepage

### Add a New Product (via API)

```bash
# First, login to get auth token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@taiwantea.com","password":"Admin123!"}' \
  -c cookies.txt

# Upload image
curl -X POST http://localhost:8000/api/admin/upload \
  -H "Content-Type: multipart/form-data" \
  -F "image=@/path/to/tea-image.jpg" \
  -b cookies.txt

# Use returned imageUrl in product creation
curl -X POST http://localhost:8000/api/admin/products \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "Jasmine Pearl Green Tea",
    "category": "green-tea",
    "description": "Hand-rolled jasmine-scented green tea pearls...",
    "price": 19.99,
    "imageUrl": "/uploads/products/jasmine-pearl-001.webp",
    "inStock": true
  }'
```

### Run Tests

**Backend**:
```bash
cd backend
pytest                              # Run all tests
pytest --cov=src                    # Run with coverage
pytest tests/contract/              # Run contract tests only
pytest tests/integration/           # Run integration tests only
```

**Frontend**:
```bash
cd frontend
npm test                            # Run all tests
npm run test:coverage               # Run with coverage
npm run test:ui                     # Open Vitest UI
```

### View Logs

**Docker Compose**:
```bash
docker-compose logs -f              # All services
docker-compose logs -f backend      # Backend only
docker-compose logs -f frontend     # Frontend only
```

**Manual Setup**:
- Backend: Logs appear in terminal where `uvicorn` is running
- Frontend: Logs appear in terminal where `npm run dev` is running

---

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/add-tea-reviews
```

### 2. Make Changes

Edit code in your IDE. Hot reload is enabled for both frontend and backend.

### 3. Run Linters

**Backend**:
```bash
cd backend
black src/                          # Format code
ruff check src/                     # Lint code
```

**Frontend**:
```bash
cd frontend
npm run lint                        # ESLint
npm run format                      # Prettier
```

### 4. Run Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: add tea product reviews feature"
```

Follow [Conventional Commits](https://www.conventionalcommits.org/) format.

---

## Troubleshooting

### MongoDB Connection Error

**Error**: `pymongo.errors.ServerSelectionTimeoutError`

**Solution**:
1. Ensure MongoDB is running: `docker ps` or check local MongoDB service
2. Verify `MONGODB_URL` in `backend/.env`
3. Check MongoDB logs: `docker logs mongodb`

### CORS Error in Browser

**Error**: `Access to fetch at 'http://localhost:8000' from origin 'http://localhost:5173' has been blocked by CORS policy`

**Solution**:
1. Verify `ALLOWED_ORIGINS` in `backend/.env` includes `http://localhost:5173`
2. Restart backend server after changing .env

### Image Upload Fails

**Error**: `413 Payload Too Large` or `400 Invalid file type`

**Solution**:
1. Check file size is under 5MB
2. Ensure file type is JPG, PNG, or WebP
3. Verify `UPLOAD_DIR` in `backend/.env` exists and is writable

### Frontend Can't Connect to API

**Error**: `Network Error` or `ERR_CONNECTION_REFUSED`

**Solution**:
1. Ensure backend is running on port 8000
2. Verify `VITE_API_URL` in `frontend/.env` is correct
3. Check browser console for detailed error

### Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port
lsof -i :8000    # Backend port
lsof -i :5173    # Frontend port

# Kill process
kill -9 <PID>
```

---

## Next Steps

Once the application is running:

1. **Customize Categories**: Edit seed data in `backend/src/scripts/seed_data.py`
2. **Add Products**: Use admin panel to populate catalog
3. **Update Styling**: Modify CSS in `frontend/src/styles/`
4. **Configure Production**: Update `.env` files for production deployment
5. **Set Up CI/CD**: Configure GitHub Actions or similar for automated testing

---

## Additional Resources

- **API Documentation**: http://localhost:8000/docs
- **React DevTools**: [Chrome Extension](https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi)
- **MongoDB Compass**: [Download](https://www.mongodb.com/products/compass) for database GUI
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/

---

## Support

For issues or questions:
1. Check this quickstart guide
2. Review API documentation at http://localhost:8000/docs
3. Check application logs for error details
4. Contact the development team
