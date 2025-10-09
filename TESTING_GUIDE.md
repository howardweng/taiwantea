# TAIWANTEA Testing Guide

## Overview

This project has testing infrastructure set up for both backend (Python/pytest) and frontend (React/Vitest).

---

## Backend Testing (Python + pytest)

### Test Structure

```
backend/tests/
├── conftest.py              # Pytest configuration and fixtures
├── contract/
│   └── test_products_api.py # API contract tests (20 tests)
├── integration/             # Integration tests (TODO)
└── unit/                    # Unit tests (TODO)
```

### Running Backend Tests

**1. Run all tests:**
```bash
cd backend
source .venv/bin/activate
pytest
```

**2. Run specific test file:**
```bash
pytest tests/contract/test_products_api.py -v
```

**3. Run with coverage:**
```bash
pytest --cov=src --cov-report=html --cov-report=term
```

**4. Run specific test:**
```bash
pytest tests/contract/test_products_api.py::TestCategoriesAPI::test_get_categories_returns_200 -v
```

### Current Test Status

**Contract Tests (test_products_api.py):**
- ✅ 5 passing tests (JSON responses, error handling)
- ⚠️ 15 failing tests (need database connection)

**Issue:** Tests fail because they need MongoDB connection during test execution.

**Solution needed:** Create test fixtures with MongoDB connection or use test database.

### Test Categories Covered

1. **Categories API** (`GET /api/categories`)
   - Response status codes
   - JSON format validation
   - Data structure verification
   - Sorting by display order

2. **Products API** (`GET /api/products`)
   - Response structure
   - Product object schema
   - Category filtering
   - Pagination (limit/skip)
   - Stock filtering
   - Count matching

3. **Single Product API** (`GET /api/products/{id}`)
   - Valid ID returns 200
   - Invalid ID returns 400
   - Non-existent ID returns 404
   - Response structure

4. **Error Handling**
   - Invalid query parameters
   - Error response format

---

## Frontend Testing (React + Vitest)

### Test Structure

```
frontend/tests/
├── setup.js                 # Vitest configuration
├── components/              # Component tests (TODO)
└── integration/             # Integration tests (TODO)
```

### Running Frontend Tests

**1. Run all tests (watch mode):**
```bash
cd frontend
npm test
```

**2. Run tests once:**
```bash
npm test -- --run
```

**3. Run with coverage:**
```bash
npm run test:coverage
```

**4. Run specific test file:**
```bash
npm test -- tests/components/ProductCard.test.jsx
```

### Current Test Status

⚠️ **No frontend tests implemented yet**

Test files mentioned in plan but not created:
- `tests/components/ProductCard.test.jsx`
- `tests/components/Navigation.test.jsx`
- `tests/components/ProductForm.test.jsx`
- `tests/components/AdminLogin.test.jsx`
- `tests/integration/userFlows.test.jsx`

---

## Manual Testing Guide

### Backend API Testing

**1. Health Check:**
```bash
curl http://localhost:8585/api/health
```

**2. Get Categories:**
```bash
curl http://localhost:8585/api/categories
```

**3. Get Products:**
```bash
curl http://localhost:8585/api/products
```

**4. Filter by Category:**
```bash
curl http://localhost:8585/api/products?category=green-tea
```

**5. Admin Login:**
```bash
curl -X POST http://localhost:8585/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@taiwantea.com","password":"admin123"}'
```

**6. Create Product (requires auth):**
```bash
curl -X POST http://localhost:8585/api/admin/products \
  -H "Content-Type: application/json" \
  -H "Cookie: access_token=YOUR_TOKEN" \
  -d '{
    "name": "Test Tea",
    "category": "green-tea",
    "price": 299,
    "description": "Test description",
    "imageUrl": "https://example.com/image.jpg",
    "inStock": true
  }'
```

### Frontend Manual Testing

**1. Customer Flow:**
- Visit http://localhost:5173
- Browse products by category
- Click navigation items to jump between sections
- Scroll through all products
- View product details (images, prices, descriptions)

**2. Admin Flow:**
- Visit http://localhost:5173/admin/login
- Login: `admin@taiwantea.com` / `admin123`
- View dashboard with product statistics
- Switch between Products/Categories/Settings tabs
- Create new product with image upload
- Edit existing product
- Delete product
- Create/edit/delete categories
- Logout

---

## Test Coverage Goals (Per Constitution)

### Target: 80% Coverage Minimum

**Current Status:**
- Backend: Unknown (not measured)
- Frontend: 0% (no tests)

**Priority Areas to Test:**

1. **Critical Path (Must Test):**
   - Admin authentication
   - Product CRUD operations
   - Image upload
   - Category management
   - Public product listing

2. **Important (Should Test):**
   - Input validation
   - Error handling
   - API response formats
   - Loading states
   - Form validation

3. **Nice to Have:**
   - UI component rendering
   - Navigation behavior
   - Accessibility features
   - Performance metrics

---

## Test Data Setup

### Create Test Admin User

```bash
cd backend
source .venv/bin/activate
python -m src.scripts.seed_data
```

This creates:
- Admin user: `admin@taiwantea.com` / `admin123`
- Sample categories (Green Tea, Black Tea, Oolong, Pu-erh)
- Sample products in each category

### Create Test Database Indexes

```bash
cd backend
source .venv/bin/activate
python -m src.database_indexes
```

---

## Testing Best Practices

### TDD Approach (Recommended)

1. **Write test first** (should fail)
2. **Implement minimum code** to pass
3. **Refactor** while keeping tests green
4. **Commit** after each cycle

### Test Naming Convention

```python
# Backend (pytest)
def test_<function>_<condition>_<expected_result>():
    """Should <expected behavior>"""
    pass

# Examples:
def test_get_products_returns_200():
    """Should return 200 OK"""

def test_get_products_with_invalid_category_returns_404():
    """Should return 404 for invalid category"""
```

```javascript
// Frontend (Vitest)
describe('ComponentName', () => {
  it('should <expected behavior>', () => {
    // test code
  });
});

// Example:
describe('ProductCard', () => {
  it('should display product name and price', () => {
    // test code
  });
});
```

### Fixture Usage

```python
# Backend: Use async_client fixture
async def test_example(async_client: AsyncClient):
    response = await async_client.get("/api/products")
    assert response.status_code == 200
```

```javascript
// Frontend: Use Testing Library
import { render, screen } from '@testing-library/react';
import ProductCard from './ProductCard';

test('renders product name', () => {
  render(<ProductCard name="Test Tea" price={299} />);
  expect(screen.getByText('Test Tea')).toBeInTheDocument();
});
```

---

## Common Test Commands Summary

### Backend
```bash
cd backend
source .venv/bin/activate

# Run all tests
pytest

# Verbose output
pytest -v

# With coverage
pytest --cov=src --cov-report=html

# Run specific file
pytest tests/contract/test_products_api.py

# Run specific test
pytest tests/contract/test_products_api.py::TestCategoriesAPI::test_get_categories_returns_200

# Stop on first failure
pytest -x

# Run only failed tests from last run
pytest --lf
```

### Frontend
```bash
cd frontend

# Watch mode (interactive)
npm test

# Run once
npm test -- --run

# With coverage
npm run test:coverage

# Run specific file
npm test -- tests/components/ProductCard.test.jsx

# UI mode (interactive)
npm test -- --ui
```

---

## Next Steps for Complete Test Coverage

### Phase 1: Fix Existing Tests
- [ ] Add database connection fixture for backend tests
- [ ] Create test database setup/teardown
- [ ] Run existing 20 contract tests successfully

### Phase 2: Backend Tests
- [ ] Integration tests for product CRUD flow
- [ ] Integration tests for admin authentication
- [ ] Unit tests for product service
- [ ] Unit tests for auth service
- [ ] Image upload tests

### Phase 3: Frontend Tests
- [ ] Component tests (ProductCard, CategorySection, Navigation)
- [ ] Admin component tests (ProductForm, ImageUpload, AdminLogin)
- [ ] Integration tests for user flows
- [ ] Accessibility tests

### Phase 4: Measure Coverage
- [ ] Run coverage reports
- [ ] Identify gaps (<80%)
- [ ] Add tests for uncovered code
- [ ] Achieve 80% target

---

## Troubleshooting

### Backend Tests Fail with "Database not initialized"

**Problem:** Tests need MongoDB connection but fixture doesn't initialize it.

**Solution:** Update `conftest.py` to include database setup:
```python
@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    await connect_to_mongo()
    yield
    await close_mongo_connection()
```

### Frontend Tests Hang

**Problem:** Vitest may wait for user input in watch mode.

**Solution:** Use `--run` flag for CI/automated testing:
```bash
npm test -- --run
```

### Import Errors in Tests

**Problem:** Module path issues.

**Solution:** Ensure pytest.ini and vitest.config.js have correct paths configured.

---

## Continuous Integration (CI)

### Recommended CI Pipeline

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    services:
      mongodb:
        image: mongo:7
        ports:
          - 27017:27017
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: cd backend && pip install -r requirements.txt
      - run: cd backend && pytest --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v3

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: cd frontend && npm ci
      - run: cd frontend && npm test -- --run --coverage
      - uses: codecov/codecov-action@v3
```

---

## Resources

- **pytest Documentation:** https://docs.pytest.org/
- **Vitest Documentation:** https://vitest.dev/
- **React Testing Library:** https://testing-library.com/react
- **FastAPI Testing:** https://fastapi.tiangolo.com/tutorial/testing/
- **Test Coverage Tools:** pytest-cov, Vitest coverage
