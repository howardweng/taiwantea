# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TAIWANTEA is a production-ready e-commerce platform for selling premium Taiwanese tea leaves. It's a full-stack application with:
- **Backend**: FastAPI + MongoDB (Motor async driver) + JWT authentication
- **Frontend**: React 18 + Vite + React Router + CSS Modules
- **Database**: MongoDB 6.0+ with async operations
- **Testing**: Pytest (87% coverage) + Vitest

## Development Setup

### Quick Start Commands

**Backend (from repository root):**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Configure MONGODB_URL and SECRET_KEY
python src/scripts/seed_data.py  # Seed initial data
uvicorn src.main:app --reload --host 0.0.0.0 --port 8585
```

**Frontend (from repository root):**
```bash
cd frontend
npm install
cp .env.example .env  # Configure VITE_API_URL
npm run dev  # Runs on port 5173
```

**Docker (from repository root):**
```bash
docker-compose up -d  # Development environment
```

## Testing

### Backend Tests (87% coverage)
```bash
cd backend
pytest                           # Run all tests
pytest -v                        # Verbose output
pytest --cov=src                 # With coverage report
pytest --cov=src --cov-report=html  # HTML coverage report
pytest tests/contract/ -v        # Contract tests only
pytest tests/integration/ -v     # Integration tests only
pytest tests/unit/ -v            # Unit tests only
pytest -k "test_name"            # Run specific test
```

### Frontend Tests
```bash
cd frontend
npm test                         # Run tests
npm run test:coverage            # With coverage
```

### Code Quality
```bash
cd backend
black .                          # Format Python code
ruff check .                     # Lint Python code

cd frontend
npm run lint                     # Lint JavaScript
npm run format                   # Format with Prettier
```

## Architecture

### Backend Structure
```
backend/src/
├── main.py                 # FastAPI app entry point, middleware setup, router registration
├── database.py             # MongoDB connection (Motor async), global client/database
├── config.py               # Pydantic Settings for env vars (MONGODB_URL, SECRET_KEY, etc)
├── logger.py               # Structured logging configuration
├── middleware/
│   ├── auth.py            # JWT authentication middleware
│   ├── logging.py         # Request/response logging
│   └── rate_limit.py      # Rate limiting for admin endpoints (100 req/min)
├── models/                # Database models (CRUD operations)
│   ├── admin.py           # Admin user CRUD
│   ├── product.py         # Product CRUD
│   ├── category.py        # Category CRUD
│   ├── carousel.py        # Homepage carousel CRUD
│   ├── intro_section.py   # Intro section CRUD
│   └── site_settings.py   # Site-wide settings CRUD
├── schemas/               # Pydantic validation schemas
│   ├── admin.py           # AdminLogin, AdminResponse
│   ├── product.py         # ProductCreate, ProductUpdate, ProductResponse
│   ├── category.py        # CategoryCreate, CategoryUpdate
│   └── site_settings.py   # SiteSettingsUpdate
├── routers/               # API endpoint definitions
│   ├── auth.py            # POST /api/auth/login, /logout, GET /me
│   ├── products.py        # GET /api/products, /products/{id} (public)
│   ├── admin_products.py  # Admin product CRUD (protected)
│   ├── admin_categories.py # Admin category CRUD (protected)
│   ├── carousel.py        # GET /api/carousel (public)
│   ├── admin_carousel.py  # Admin carousel CRUD (protected)
│   ├── intro_section.py   # GET /api/intro-section (public)
│   ├── admin_intro_section.py # Admin intro section CRUD (protected)
│   ├── site_settings.py   # GET /api/site-settings (public)
│   ├── admin_site_settings.py # Admin site settings (protected)
│   └── upload.py          # POST /api/upload/image (image upload with validation)
├── services/              # Business logic layer
│   ├── auth_service.py    # JWT token creation/validation, password hashing (bcrypt)
│   └── product_service.py # Product business logic
└── scripts/
    └── seed_data.py       # Database seeding script
```

**Key Backend Patterns:**
- All database operations use Motor's async methods (`await collection.find_one()`, etc)
- Authentication uses JWT tokens with httpOnly cookies for security
- Admin endpoints protected by `get_current_admin` dependency
- Rate limiting applied globally to `/api/admin/*` routes
- Request/response logging middleware for debugging
- Standardized response format: `{"success": bool, "data": any, "error": {...}}`
- Images uploaded to `backend/uploads/` with Pillow validation

### Frontend Structure
```
frontend/src/
├── main.jsx               # React app entry point
├── App.jsx                # Router configuration, global layout
├── components/
│   ├── common/           # Reusable UI components (Spinner, Toast, Modal, etc)
│   ├── customer/         # Customer-facing components
│   │   ├── ProductCard.jsx        # Product display card
│   │   ├── ProductGrid.jsx        # Product grid layout
│   │   ├── CategorySection.jsx    # Category filter
│   │   ├── IntroSection.jsx       # Homepage intro
│   │   └── *.module.css           # CSS Modules for styling
│   ├── admin/            # Admin dashboard components
│   │   ├── ProductForm.jsx        # Product create/edit form
│   │   ├── CategoryManager.jsx    # Category management
│   │   ├── IntroSectionEditor.jsx # Intro section editor
│   │   ├── SiteSettingsEditor.jsx # Site settings editor
│   │   └── ImageUpload.jsx        # Drag-drop image upload
│   └── layout/           # Layout components (Header, Footer, Navigation)
├── pages/
│   ├── HomePage.jsx              # Customer-facing store page
│   └── admin/
│       ├── LoginPage.jsx         # Admin login
│       ├── DashboardPage.jsx     # Admin dashboard with stats
│       ├── ProductsPage.jsx      # Admin product management
│       └── CategoriesPage.jsx    # Admin category management
├── services/             # API client services
│   ├── api.js                    # Axios instance with interceptors
│   ├── productService.js         # Product API calls
│   ├── adminProductService.js    # Admin product API calls
│   ├── adminCategoryService.js   # Admin category API calls
│   └── carouselService.js        # Carousel API calls
├── hooks/                # Custom React hooks
│   ├── useAuth.jsx               # Authentication state/actions
│   ├── useProducts.js            # Product data fetching/state
│   └── useCarousel.js            # Carousel data fetching
└── styles/               # Global styles
```

**Key Frontend Patterns:**
- React Router for navigation with protected routes
- Custom hooks for data fetching and state management
- CSS Modules for component-scoped styling
- Axios interceptors for global error handling
- Toast notifications for user feedback
- Lazy loading for images with placeholders
- Form validation with controlled components
- Admin authentication persisted in localStorage

### Database Collections

MongoDB collections (managed by Motor):
- `admins` - Admin users (email, hashed_password)
- `products` - Tea products (name, description, price, category_id, image_url, badges, display_order)
- `categories` - Product categories (name, display_order)
- `carousel_items` - Homepage carousel images
- `intro_section` - Homepage intro content
- `site_settings` - Site-wide configuration (hero text, contact info, etc)

All collections use string IDs (`_id` as string, no ObjectId conversion in responses).

## Common Development Tasks

### Adding a New API Endpoint

1. Define Pydantic schema in `backend/src/schemas/`
2. Add model CRUD method in `backend/src/models/`
3. Create router endpoint in `backend/src/routers/`
4. Register router in `backend/src/main.py`
5. Add test in `backend/tests/contract/` or `backend/tests/integration/`

### Adding a New Frontend Component

1. Create component in appropriate directory (`common/`, `customer/`, or `admin/`)
2. Create CSS Module (`.module.css`) if needed
3. Add service function in `frontend/src/services/` for API calls
4. Create custom hook in `frontend/src/hooks/` if complex state needed
5. Import and use in page component

### Database Migration

Since MongoDB is schemaless, migrations are manual:
1. Update model in `backend/src/models/`
2. Update schema in `backend/src/schemas/`
3. Add migration script in `backend/src/scripts/` if needed
4. Update seed data in `backend/src/scripts/seed_data.py`

## Environment Configuration

### Backend (.env)
Required variables:
- `MONGODB_URL` - MongoDB connection string (no default)
- `SECRET_KEY` - JWT secret key (no default)
- `DATABASE_NAME` - Database name (default: "taiwantea")
- `ALLOWED_ORIGINS` - CORS origins (default: "http://localhost:5173,http://127.0.0.1:5173")
- `ENVIRONMENT` - "development" or "production" (default: "development")

### Frontend (.env)
Required variables:
- `VITE_API_URL` - Backend API URL (default: "http://localhost:8585")

## Access Points

- Customer Store: http://localhost:5173
- Admin Dashboard: http://localhost:5173/admin/login
- API Documentation: http://localhost:8585/docs
- API Health Check: http://localhost:8585/api/health

Default admin credentials (from seed data):
- Email: `admin@taiwantea.com`
- Password: `Admin123!`

## Important Notes

- Backend runs on port 8585, frontend on port 5173
- All async operations in backend use Motor (not pymongo)
- JWT tokens stored in httpOnly cookies (not localStorage)
- Images uploaded to `backend/uploads/` directory
- Rate limiting: 100 requests per minute on admin endpoints
- CORS is configured in `backend/src/main.py`
- All API responses follow standardized format with `success`, `data`, and `error` fields
- Product display order managed via drag-and-drop in admin UI
- CSS Modules used throughout frontend (not global CSS)

## Documentation

Additional documentation in `docs/`:
- `TESTING.md` - Comprehensive testing guide
- `IMPLEMENTATION_STATUS.md` - Development progress tracker
- `PRODUCTION_READY.md` - Deployment guide
- `PROGRESS_SUMMARY.md` - Overall progress summary
- `使用說明.md` - Chinese user guide

Feature specifications in `specs/001-i-wnat-to/`:
- `spec.md` - Feature requirements
- `contracts/api.yaml` - OpenAPI specification
