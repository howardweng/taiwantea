# TAIWANTEA 🍵 - Premium Tea E-Commerce Platform

A modern, production-ready e-commerce platform for selling premium Taiwanese tea leaves with complete admin content management.

[![Test Coverage](https://img.shields.io/badge/coverage-87%25-brightgreen)]()
[![Backend Tests](https://img.shields.io/badge/tests-50%20passing-brightgreen)]()
[![Progress](https://img.shields.io/badge/progress-96%25-blue)]()

## ✨ Key Features

### 🛍️ Customer Experience
- **Product Catalog** - Browse premium teas organized by category
- **Smart Navigation** - Smooth-scroll navigation with sticky header
- **Responsive Design** - Mobile-first (320px-2560px)
- **Image Preview** - Full-size modal view
- **Accessibility** - WCAG 2.1 Level AA compliant
- **Fast Performance** - Lazy loading & optimization

### 👨‍💼 Admin Dashboard
- **Secure Auth** - JWT authentication with bcrypt
- **Product Management** - Full CRUD operations
- **Category Management** - Organize product taxonomy
- **Image Upload** - Drag-drop with preview
- **Real-time Dashboard** - Statistics & overview
- **Toast Notifications** - Instant user feedback
- **Rate Limiting** - DDoS protection (100 req/min)

## 🏗️ Technology Stack

**Backend:** FastAPI • MongoDB • Motor • Pydantic • JWT
**Frontend:** React 18 • Vite • React Router • Axios • CSS Modules
**Testing:** Pytest (87% coverage) • Vitest
**DevOps:** Docker • Nginx • MongoDB Atlas

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.11+  |  Node.js 18+  |  MongoDB 6.0+
```

### Installation

**1. Clone Repository**
```bash
git clone <repository-url>
cd TAIWANTEA
```

**2. Backend Setup**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

**3. Frontend Setup**
```bash
cd frontend
npm install
cp .env.example .env
```

**4. Database Setup**
```bash
# Start MongoDB
mongod --dbpath /path/to/data

# Seed initial data
cd backend
python src/scripts/seed_data.py
```

**5. Run Application**

Terminal 1 (Backend):
```bash
cd backend
source .venv/bin/activate
uvicorn src.main:app --reload --host 0.0.0.0 --port 8585
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

### Access Points
- 🛍️ **Store**: http://localhost:5173
- 👤 **Admin**: http://localhost:5173/admin/login
- 📚 **API Docs**: http://localhost:8585/docs
- 🏥 **Health**: http://localhost:8585/api/health

**Default Admin Login:**
Email: `admin@taiwantea.com`
Password: `Admin123!`

## 📡 API Endpoints

### Public
```
GET  /api/categories             List all categories
GET  /api/products               List products (with filters)
GET  /api/products/{id}          Get product details
GET  /api/health                 Health check
```

### Authentication
```
POST /api/auth/login             Admin login
POST /api/auth/logout            Admin logout
GET  /api/auth/me                Current user
```

### Admin (Protected + Rate Limited)
```
# Products
GET    /api/admin/products
POST   /api/admin/products
PUT    /api/admin/products/{id}
DELETE /api/admin/products/{id}

# Categories
GET    /api/admin/categories
POST   /api/admin/categories
PUT    /api/admin/categories/{id}
DELETE /api/admin/categories/{id}

# Upload
POST   /api/upload/image          Upload product image
```

## 🧪 Testing

### Backend (87% Coverage)
```bash
cd backend
pytest                           # All tests
pytest --cov=src                 # With coverage
pytest tests/contract/ -v        # Contract tests
```

**Results:** ✅ 50/50 tests passing • 87% coverage

### Frontend
```bash
cd frontend
npm test                         # All tests
npm run test:coverage            # With coverage
```

## 🐳 Docker Deployment

```bash
# Development
docker-compose up -d

# Production
docker-compose -f docker-compose.prod.yml up -d
```

## 📊 Performance Metrics

- ⚡ Page Load: <3 seconds
- 🚀 API Response: <200ms (p95)
- 🖼️ Images: Lazy loaded with thumbnails
- 💾 Database: Indexed for fast queries

## 🔒 Security

✅ JWT with httpOnly cookies
✅ Bcrypt password hashing
✅ CORS configuration
✅ Rate limiting (100 req/min on admin)
✅ Input validation (Pydantic)
✅ MongoDB injection prevention
✅ Request/response logging
✅ Environment variable secrets

## 📁 Project Structure

```
TAIWANTEA/
├── backend/                     # FastAPI backend
│   ├── src/
│   │   ├── main.py              # FastAPI app + middleware
│   │   ├── database.py          # MongoDB connection
│   │   ├── models/              # Database models (CRUD)
│   │   ├── schemas/             # Pydantic validation
│   │   ├── routers/             # API endpoints
│   │   ├── services/            # Business logic
│   │   ├── middleware/          # Auth, logging, rate limit
│   │   └── scripts/             # Database seeding
│   ├── tests/                   # 50 tests, 87% coverage
│   └── requirements.txt
│
├── frontend/                    # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/          # Reusable (Spinner, Toast, etc)
│   │   │   ├── customer/        # Product display
│   │   │   ├── admin/           # Admin forms
│   │   │   └── layout/          # Navigation, footer
│   │   ├── pages/               # HomePage, AdminPage
│   │   ├── services/            # API clients
│   │   └── hooks/               # useAuth, useProducts
│   └── package.json
│
├── docs/                        # Documentation
│   ├── IMPLEMENTATION_STATUS.md # Development progress
│   ├── TESTING.md               # Testing guide
│   ├── PRODUCTION_READY.md      # Deployment guide
│   └── ...
│
├── assets/                      # Project assets (images, etc)
├── specs/                       # Feature specifications
├── docker-compose.yml           # Docker orchestration
├── CLAUDE.md                    # AI assistant instructions
├── .gitignore
└── README.md                    # This file
```

## 🔧 Configuration

### Backend (.env)
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=taiwantea
JWT_SECRET_KEY=your-secret-key
JWT_EXPIRE_MINUTES=1440
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:5173
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8585
```

## 📚 Documentation

- [Implementation Status](docs/IMPLEMENTATION_STATUS.md) - Development progress
- [Testing Guide](docs/TESTING.md) - Test documentation
- [Production Guide](docs/PRODUCTION_READY.md) - Deployment
- [Progress Summary](docs/PROGRESS_SUMMARY.md) - Overall progress
- [使用說明](docs/使用說明.md) - Chinese user guide
- [Feature Spec](specs/001-i-wnat-to/spec.md) - Requirements
- [API Spec](specs/001-i-wnat-to/contracts/api.yaml) - OpenAPI

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/name`)
3. Write tests first (TDD approach)
4. Commit changes (`git commit -m 'Add feature'`)
5. Push branch (`git push origin feature/name`)
6. Open Pull Request

## 📝 License

MIT License - See [LICENSE](LICENSE) file

## 🙏 Acknowledgments

Built with FastAPI, React, and MongoDB for modern tea commerce.

---

**Made with ❤️ for tea lovers** | [Report Issue](https://github.com/user/taiwantea/issues)
