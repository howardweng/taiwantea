# TAIWANTEA - Tea Leaves E-Commerce Website

A modern, single-page tea e-commerce website with React frontend and FastAPI backend.

## 🌐 Architecture

- **Frontend**: React 18 + Vite + CSS Modules
- **Backend**: FastAPI + Motor (async MongoDB) + Pydantic
- **Database**: MongoDB
- **Authentication**: JWT with httpOnly cookies + bcrypt

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB 6.0+
- Docker & Docker Compose (recommended)

### Using Docker Compose (Recommended)

```bash
# Clone and navigate to project
cd TAIWANTEA

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Start all services
docker-compose up -d

# Seed initial data
docker-compose exec backend python -m src.scripts.seed_data
```

Access the application:
- **Frontend**: http://localhost:5173
- **Admin Panel**: http://localhost:5173/admin
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Manual Setup

**Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
python -m src.scripts.seed_data
uvicorn src.main:app --reload
```

**Frontend**:
```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with your settings
npm run dev
```

## 📁 Project Structure

```
TAIWANTEA/
├── backend/
│   ├── src/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   ├── services/
│   │   └── middleware/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── styles/
│   ├── tests/
│   └── package.json
├── specs/
│   └── 001-i-wnat-to/
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       └── ...
└── docker-compose.yml
```

## 🎯 Features

### Customer-Facing
- ✅ Single-page tea catalog with category sections
- ✅ Smooth-scroll navigation
- ✅ Responsive design (320px - 2560px)
- ✅ WCAG 2.1 AA accessibility

### Admin Panel
- ✅ Secure JWT authentication
- ✅ Product CRUD operations
- ✅ Image upload with auto-optimization (WebP)
- ✅ Real-time updates to public site

## 🧪 Testing

**Backend**:
```bash
cd backend
pytest                    # Run all tests
pytest --cov=src          # With coverage
pytest tests/contract/    # Contract tests only
```

**Frontend**:
```bash
cd frontend
npm test                  # Run all tests
npm run test:coverage     # With coverage
```

## 📝 Development

### Code Quality

**Backend**:
```bash
black src/                # Format code
ruff check src/           # Lint code
```

**Frontend**:
```bash
npm run lint              # ESLint
npm run format            # Prettier
```

### Default Admin Credentials

- Email: `admin@taiwantea.com`
- Password: `Admin123!`

⚠️ **Change these in production!**

## 📚 Documentation

- **Specification**: `specs/001-i-wnat-to/spec.md`
- **Implementation Plan**: `specs/001-i-wnat-to/plan.md`
- **Task List**: `specs/001-i-wnat-to/tasks.md`
- **Quickstart Guide**: `specs/001-i-wnat-to/quickstart.md`
- **Website Overview (中文)**: `specs/001-i-wnat-to/website-overview-zh-TW.md`
- **API Documentation**: http://localhost:8000/docs (when running)

## 🔧 Configuration

### Backend Environment Variables

See `backend/.env.example` for all available options.

### Frontend Environment Variables

See `frontend/.env.example` for all available options.

## 📦 Deployment

TBD - Follow quickstart.md for deployment guidelines

## 📄 License

MIT

## 🤝 Contributing

This project follows TDD (Test-Driven Development) approach. Please ensure:
- Tests are written first and verified to fail
- Code coverage meets 80% minimum
- All linters pass
- Constitution principles are followed

## 🆘 Support

For issues or questions, refer to:
1. Quickstart guide: `specs/001-i-wnat-to/quickstart.md`
2. API documentation: http://localhost:8000/docs
3. Check application logs for error details
