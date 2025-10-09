# TAIWANTEA Testing Documentation

**Project:** TAIWANTEA E-commerce Platform
**Last Updated:** October 9, 2025
**Test Status:** ✅ 20/20 Backend Tests Passing | ⚠️ Frontend Tests Not Implemented

---

## Table of Contents

1. [Test Status Overview](#test-status-overview)
2. [Backend Testing](#backend-testing)
3. [Frontend Testing](#frontend-testing)
4. [Manual Testing](#manual-testing)
5. [Test Coverage Analysis](#test-coverage-analysis)
6. [Running Tests](#running-tests)
7. [Writing New Tests](#writing-new-tests)
8. [Continuous Integration](#continuous-integration)
9. [Troubleshooting](#troubleshooting)
10. [Next Steps](#next-steps)

---

## Test Status Overview

### Current Status

| Component | Tests | Passing | Failing | Coverage | Status |
|-----------|-------|---------|---------|----------|--------|
| **Backend API** | 20 | 20 | 0 | 58% | ✅ Working |
| **Backend Models** | 0 | 0 | 0 | 44-69% | ⚠️ Need Tests |
| **Backend Services** | 0 | 0 | 0 | 38-68% | ⚠️ Need Tests |
| **Backend Auth** | 0 | 0 | 0 | 36% | ⚠️ Need Tests |
| **Frontend** | 0 | 0 | 0 | 0% | ❌ Not Implemented |
| **Integration** | 0 | 0 | 0 | N/A | ❌ Not Implemented |

### Test Infrastructure

- ✅ pytest configured with asyncio support
- ✅ pytest-cov for coverage reports
- ✅ httpx AsyncClient for API testing
- ✅ MongoDB test connection working
- ✅ Session-scoped fixtures
- ✅ Vitest configured (frontend)
- ⚠️ No frontend tests written yet

---

## Backend Testing

### Test Structure

```
backend/tests/
├── conftest.py              # Pytest configuration & fixtures
├── contract/
│   └── test_products_api.py # API contract tests (20 tests) ✅
├── integration/             # Integration tests (TODO)
└── unit/                    # Unit tests (TODO)
```

### Test Categories

#### 1. Contract Tests (20 tests - ALL PASSING ✅)

**Purpose:** Verify API endpoints return correct response formats according to the API contract.

**File:** `tests/contract/test_products_api.py`

**Test Classes:**

**A. TestCategoriesAPI (5 tests)**
- ✅ `test_get_categories_returns_200` - Status code verification
- ✅ `test_get_categories_returns_json` - Content-Type header check
- ✅ `test_get_categories_response_structure` - Response has `categories` array
- ✅ `test_category_object_structure` - Category objects have required fields
- ✅ `test_categories_sorted_by_display_order` - Categories are properly sorted

**B. TestProductsAPI (9 tests)**
- ✅ `test_get_products_returns_200` - Status code verification
- ✅ `test_get_products_returns_json` - Content-Type header check
- ✅ `test_get_products_response_structure` - Response has `products` and `total`
- ✅ `test_product_object_structure` - Product objects have required fields
- ✅ `test_get_products_with_category_filter` - Category filtering works
- ✅ `test_get_products_with_invalid_category` - Returns 404 for invalid category
- ✅ `test_get_products_pagination` - Limit and skip parameters work
- ✅ `test_get_products_in_stock_filter` - Stock filtering works
- ✅ `test_total_count_matches_filter` - Total count matches filtered results

**C. TestSingleProductAPI (4 tests)**
- ✅ `test_get_product_by_id_returns_200` - Valid ID returns 200
- ✅ `test_get_product_by_id_response_structure` - Returns single product object
- ✅ `test_get_product_invalid_id_returns_400` - Invalid ObjectId format returns 400
- ✅ `test_get_product_nonexistent_id_returns_404` - Non-existent ID returns 404

**D. TestAPIErrorHandling (2 tests)**
- ✅ `test_invalid_query_parameters` - Handles invalid query params gracefully
- ✅ `test_api_returns_proper_error_format` - Errors have consistent format

### Fixtures

#### Event Loop Fixture
```python
@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the entire test session"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
```

#### Database Setup Fixture
```python
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_database(event_loop):
    """Setup database connection for entire test session"""
    print("\n✓ Connecting to test database...")
    await connect_to_mongo()
    print("✓ Database connection initialized")
    yield
    print("\n✓ Closing test database connection...")
    await close_mongo_connection()
```

#### HTTP Client Fixture
```python
@pytest_asyncio.fixture
async def async_client(setup_test_database):
    """Create an async HTTP client for testing"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client
```

### Running Backend Tests

#### Basic Commands

```bash
cd backend
source .venv/bin/activate

# Run all tests
pytest

# Run specific test file
pytest tests/contract/test_products_api.py

# Verbose output
pytest tests/contract/test_products_api.py -v

# Show print statements
pytest tests/contract/test_products_api.py -s

# Run specific test
pytest tests/contract/test_products_api.py::TestCategoriesAPI::test_get_categories_returns_200

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf
```

#### Coverage Commands

```bash
# Run with coverage
pytest --cov=src

# Coverage with terminal report
pytest --cov=src --cov-report=term-missing

# Coverage with HTML report
pytest --cov=src --cov-report=html

# View HTML report (opens in browser)
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Test Output Example

```bash
$ pytest tests/contract/test_products_api.py -v

============================= test session starts ==============================
platform linux -- Python 3.11.13, pytest-7.4.4
plugins: asyncio-0.23.3, anyio-4.11.0, cov-4.1.0
asyncio: mode=Mode.AUTO
collected 20 items

tests/contract/test_products_api.py::TestCategoriesAPI::test_get_categories_returns_200 PASSED [  5%]
tests/contract/test_products_api.py::TestCategoriesAPI::test_get_categories_returns_json PASSED [ 10%]
...
tests/contract/test_products_api.py::TestAPIErrorHandling::test_api_returns_proper_error_format PASSED [100%]

======================= 20 passed, 12 warnings in 0.19s ========================
```

---

## Frontend Testing

### Test Structure (Planned)

```
frontend/tests/
├── setup.js                 # Vitest configuration
├── components/
│   ├── ProductCard.test.jsx
│   ├── CategorySection.test.jsx
│   ├── Navigation.test.jsx
│   ├── ProductForm.test.jsx
│   └── AdminLogin.test.jsx
└── integration/
    └── userFlows.test.jsx
```

### Running Frontend Tests

```bash
cd frontend

# Run tests in watch mode (interactive)
npm test

# Run tests once
npm test -- --run

# Run with coverage
npm run test:coverage

# Run specific test file
npm test -- tests/components/ProductCard.test.jsx

# UI mode (interactive browser)
npm test -- --ui
```

### Frontend Test Example (Not Yet Implemented)

```javascript
// tests/components/ProductCard.test.jsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import ProductCard from '../../src/components/customer/ProductCard';

describe('ProductCard', () => {
  it('should display product name and price', () => {
    const product = {
      name: 'Dragon Well Green Tea',
      price: 299,
      imageUrl: 'https://example.com/tea.jpg',
      inStock: true
    };

    render(<ProductCard product={product} />);

    expect(screen.getByText('Dragon Well Green Tea')).toBeInTheDocument();
    expect(screen.getByText('NT$299')).toBeInTheDocument();
  });

  it('should show out of stock badge when not in stock', () => {
    const product = {
      name: 'Test Tea',
      price: 299,
      imageUrl: 'https://example.com/tea.jpg',
      inStock: false
    };

    render(<ProductCard product={product} />);

    expect(screen.getByText(/out of stock/i)).toBeInTheDocument();
  });
});
```

---

## Manual Testing

### API Testing with cURL

#### Health Check
```bash
curl http://localhost:8000/api/health
```

**Expected Response:**
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

#### Get Categories
```bash
curl http://localhost:8000/api/categories
```

**Expected Response:**
```json
{
  "categories": [
    {
      "_id": "green-tea",
      "name": "Green Tea",
      "description": "Fresh, delicate green teas...",
      "displayOrder": 1,
      "imageUrl": null,
      "isActive": true
    },
    ...
  ]
}
```

#### Get Products
```bash
curl http://localhost:8000/api/products
```

**Expected Response:**
```json
{
  "products": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "name": "Dragon Well Green Tea",
      "category": "green-tea",
      "price": 299,
      "description": "Premium green tea...",
      "imageUrl": "https://example.com/tea.jpg",
      "thumbnailUrl": "https://example.com/tea_thumb.jpg",
      "inStock": true,
      "displayOrder": 1
    },
    ...
  ],
  "total": 10
}
```

#### Filter by Category
```bash
curl "http://localhost:8000/api/products?category=green-tea"
```

#### Pagination
```bash
curl "http://localhost:8000/api/products?limit=5&skip=0"
```

#### Admin Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@taiwantea.com",
    "password": "admin123"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": "...",
      "email": "admin@taiwantea.com",
      "name": "Admin"
    }
  }
}
```

### Browser Testing

#### Customer Frontend
**URL:** http://localhost:5173

**Test Scenarios:**
1. ✅ Homepage loads with product grid
2. ✅ Categories displayed in navigation
3. ✅ Click category to filter products
4. ✅ Smooth scroll navigation works
5. ✅ Product cards show name, price, image
6. ✅ Out of stock badge displays correctly
7. ✅ Responsive design on mobile/tablet
8. ✅ Back to top button appears on scroll

#### Admin Panel
**URL:** http://localhost:5173/admin/login

**Login Credentials:**
- Email: `admin@taiwantea.com`
- Password: `admin123`

**Test Scenarios:**

**Authentication:**
1. ✅ Login page displays
2. ✅ Invalid credentials show error
3. ✅ Valid login redirects to dashboard
4. ✅ Logout returns to login page
5. ✅ Protected routes redirect to login when not authenticated

**Dashboard:**
1. ✅ Statistics cards show correct counts
2. ✅ Product list displays by category
3. ✅ Category tabs work (Products/Categories/Settings)

**Product Management:**
1. ✅ "Add New Product" opens form
2. ✅ Form validation works (required fields)
3. ✅ Image upload with preview
4. ✅ Thumbnail generated automatically
5. ✅ Create product saves and shows in list
6. ✅ Edit product pre-fills form
7. ✅ Update product saves changes
8. ✅ Delete product shows confirmation
9. ✅ Toast notifications display
10. ✅ Products appear on public site immediately

**Category Management:**
1. ✅ Category list displays
2. ✅ Add category form works
3. ✅ Edit category pre-fills form
4. ✅ Delete category confirmation
5. ✅ Display order affects sorting

---

## Test Coverage Analysis

### Current Coverage: 58%

#### Coverage by Component

```
Name                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------
src/schemas/admin.py                21      0   100%
src/schemas/category.py             20      0   100%
src/schemas/product.py              55      0   100%
src/config.py                       25      1    96%
src/logger.py                       26      1    96%
src/routers/products.py             40      6    85%
src/database.py                     22      4    82%
src/models/product.py               58     18    69%
src/services/product_service.py     38     12    68%
src/main.py                         37     13    65%
src/routers/auth.py                 22      9    59%
src/models/category.py              39     16    59%
src/models/admin.py                 34     19    44%
src/services/auth_service.py        50     31    38%
src/middleware/auth.py              22     14    36%
src/routers/upload.py               81     57    30%
src/routers/admin_categories.py     44     33    25%
src/routers/admin_products.py       64     49    23%
src/database_indexes.py             23     23     0%
---------------------------------------------------------------
TOTAL                              722    306    58%
```

#### High Coverage (>80%) ✅
- **Schemas:** 100% - All Pydantic models fully covered
- **Config:** 96% - Configuration module well tested
- **Logger:** 96% - Logging setup verified
- **Products Router:** 85% - Public API well tested
- **Database:** 82% - Connection handling tested

#### Medium Coverage (50-80%) ⚠️
- **Models:** 44-69% - CRUD operations partially tested
- **Product Service:** 68% - Business logic partially tested
- **Auth Router:** 59% - Login tested, logout/me routes not tested

#### Low Coverage (<50%) ❌
- **Auth Middleware:** 36% - JWT verification not tested
- **Auth Service:** 38% - Password hashing/verification not tested
- **Upload Router:** 30% - File upload/thumbnail generation not tested
- **Admin Routers:** 23-25% - Admin CRUD operations not tested

#### No Coverage (0%) ❌
- **Database Indexes:** 0% - Script not tested (run manually)

### Coverage Goals

| Priority | Component | Current | Target | Tests Needed |
|----------|-----------|---------|--------|--------------|
| P1 | Auth Middleware | 36% | 80% | Token validation, error cases |
| P1 | Admin Routers | 23-25% | 80% | CRUD operations, auth checks |
| P1 | Upload Router | 30% | 80% | File upload, thumbnail, validation |
| P2 | Auth Service | 38% | 80% | Password hashing, JWT generation |
| P2 | Models | 44-69% | 80% | All CRUD methods, error cases |
| P3 | Services | 68% | 85% | Edge cases, error handling |

---

## Running Tests

### Quick Start

```bash
# Backend tests
cd backend
source .venv/bin/activate
pytest -v

# Frontend tests (when implemented)
cd frontend
npm test
```

### Complete Test Suite

```bash
# Backend: All tests with coverage
cd backend
source .venv/bin/activate
pytest --cov=src --cov-report=html --cov-report=term-missing

# View coverage report
open htmlcov/index.html

# Frontend: All tests with coverage
cd frontend
npm run test:coverage
```

### Specific Test Categories

```bash
# Contract tests only
pytest tests/contract/ -v

# Integration tests (when implemented)
pytest tests/integration/ -v

# Unit tests (when implemented)
pytest tests/unit/ -v

# Tests by marker
pytest -m "contract" -v
pytest -m "integration" -v
pytest -m "unit" -v
```

### Continuous Testing (Watch Mode)

```bash
# Backend: Run tests on file change
pytest-watch

# Or use pytest with file monitoring
ptw -- -v

# Frontend: Watch mode (built-in)
cd frontend
npm test  # Automatically watches for changes
```

### Performance Testing

```bash
# Show slowest 10 tests
pytest --durations=10

# Profile test execution
pytest --profile

# Parallel execution (when you have many tests)
pytest -n auto  # Requires pytest-xdist
```

---

## Writing New Tests

### Test Writing Guidelines

#### 1. Follow TDD (Test-Driven Development)
1. Write test first (should FAIL)
2. Implement minimum code to pass
3. Refactor while keeping tests green
4. Commit after each cycle

#### 2. Test Naming Convention

```python
# Backend (pytest)
def test_<function>_<condition>_<expected_result>():
    """Should <expected behavior>"""
    pass

# Examples:
def test_get_products_returns_200():
    """Should return 200 OK"""

def test_create_product_with_invalid_price_returns_422():
    """Should return 422 for invalid price"""
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

#### 3. Test Structure (AAA Pattern)

```python
async def test_example(async_client):
    # Arrange - Set up test data
    product_data = {
        "name": "Test Tea",
        "price": 299,
        "category": "green-tea"
    }

    # Act - Perform the action
    response = await async_client.post("/api/admin/products", json=product_data)

    # Assert - Verify the outcome
    assert response.status_code == 201
    assert response.json()["name"] == "Test Tea"
```

### Backend Test Examples

#### API Contract Test
```python
@pytest.mark.asyncio
class TestProductsAPI:
    async def test_get_products_returns_200(self, async_client):
        """Should return 200 OK"""
        response = await async_client.get("/api/products")
        assert response.status_code == status.HTTP_200_OK

    async def test_get_products_response_structure(self, async_client):
        """Should return correct response structure"""
        response = await async_client.get("/api/products")
        data = response.json()

        assert "products" in data
        assert "total" in data
        assert isinstance(data["products"], list)
        assert isinstance(data["total"], int)
```

#### Unit Test Example (Model)
```python
@pytest.mark.asyncio
class TestProductModel:
    async def test_create_product(self):
        """Should create product in database"""
        product_data = {
            "name": "Test Tea",
            "category": "green-tea",
            "price": 299,
            "description": "Test description",
            "imageUrl": "https://example.com/image.jpg",
            "inStock": True,
            "displayOrder": 1
        }

        product_id = await ProductModel.create(product_data)
        assert product_id is not None

        # Verify product was created
        product = await ProductModel.get_by_id(product_id)
        assert product["name"] == "Test Tea"
        assert product["price"] == 299
```

#### Integration Test Example
```python
@pytest.mark.asyncio
class TestProductCreationFlow:
    async def test_complete_product_creation_flow(self, async_client):
        """Should create product and appear in public list"""
        # 1. Login as admin
        login_response = await async_client.post("/api/auth/login", json={
            "email": "admin@taiwantea.com",
            "password": "admin123"
        })
        assert login_response.status_code == 200

        # 2. Create product
        product_data = {
            "name": "Integration Test Tea",
            "category": "green-tea",
            "price": 399,
            "description": "Created in integration test",
            "imageUrl": "https://example.com/test.jpg",
            "inStock": True,
            "displayOrder": 1
        }

        create_response = await async_client.post(
            "/api/admin/products",
            json=product_data
        )
        assert create_response.status_code == 201
        product_id = create_response.json()["data"]["id"]

        # 3. Verify product appears in public API
        products_response = await async_client.get("/api/products")
        products = products_response.json()["products"]

        created_product = next(
            (p for p in products if p["_id"] == product_id),
            None
        )
        assert created_product is not None
        assert created_product["name"] == "Integration Test Tea"

        # 4. Cleanup - Delete test product
        delete_response = await async_client.delete(
            f"/api/admin/products/{product_id}"
        )
        assert delete_response.status_code == 200
```

### Frontend Test Examples

#### Component Test
```javascript
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import ProductCard from '../../src/components/customer/ProductCard';

describe('ProductCard', () => {
  const mockProduct = {
    _id: '1',
    name: 'Dragon Well Green Tea',
    price: 299,
    imageUrl: 'https://example.com/tea.jpg',
    thumbnailUrl: 'https://example.com/tea_thumb.jpg',
    description: 'Premium green tea',
    inStock: true,
    category: 'green-tea'
  };

  it('should render product information', () => {
    render(<ProductCard product={mockProduct} />);

    expect(screen.getByText('Dragon Well Green Tea')).toBeInTheDocument();
    expect(screen.getByText('NT$299')).toBeInTheDocument();
    expect(screen.getByRole('img')).toHaveAttribute('src', mockProduct.thumbnailUrl);
  });

  it('should show out of stock badge when not available', () => {
    const outOfStockProduct = { ...mockProduct, inStock: false };
    render(<ProductCard product={outOfStockProduct} />);

    expect(screen.getByText(/out of stock/i)).toBeInTheDocument();
  });

  it('should be accessible', () => {
    const { container } = render(<ProductCard product={mockProduct} />);

    // Check for proper ARIA labels
    expect(screen.getByRole('img')).toHaveAttribute('alt', expect.stringContaining('Dragon Well'));
  });
});
```

#### Hook Test
```javascript
import { renderHook, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import useProducts from '../../src/hooks/useProducts';

// Mock the API
vi.mock('../../src/services/productService', () => ({
  getProducts: vi.fn(() => Promise.resolve({
    products: [{ _id: '1', name: 'Test Tea', price: 299 }],
    total: 1
  })),
  getCategories: vi.fn(() => Promise.resolve({
    categories: [{ _id: 'green-tea', name: 'Green Tea' }]
  }))
}));

describe('useProducts', () => {
  it('should fetch products and categories', async () => {
    const { result } = renderHook(() => useProducts());

    // Initially loading
    expect(result.current.loading).toBe(true);

    // Wait for data to load
    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.products).toHaveLength(1);
    expect(result.current.categories).toHaveLength(1);
  });
});
```

---

## Continuous Integration

### GitHub Actions Example

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  backend-tests:
    runs-on: ubuntu-latest

    services:
      mongodb:
        image: mongo:7
        ports:
          - 27017:27017
        options: >-
          --health-cmd "mongosh --eval 'db.adminCommand({ping: 1})'"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt

      - name: Run tests with coverage
        run: |
          cd backend
          pytest --cov=src --cov-report=xml --cov-report=term
        env:
          MONGODB_URL: mongodb://localhost:27017
          DATABASE_NAME: taiwantea_test

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./backend/coverage.xml
          flags: backend

  frontend-tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Run tests with coverage
        run: |
          cd frontend
          npm test -- --run --coverage

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./frontend/coverage/coverage-final.json
          flags: frontend
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Running tests before commit..."

# Backend tests
cd backend
source .venv/bin/activate
pytest --tb=short
BACKEND_RESULT=$?

# Frontend tests (when implemented)
# cd ../frontend
# npm test -- --run
# FRONTEND_RESULT=$?

if [ $BACKEND_RESULT -ne 0 ]; then
    echo "❌ Backend tests failed. Commit aborted."
    exit 1
fi

echo "✅ All tests passed!"
exit 0
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Tests Fail with "Database not initialized"

**Problem:** Database connection not established before tests run.

**Solution:** Ensure `setup_test_database` fixture runs first:
```python
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_database(event_loop):
    await connect_to_mongo()
    yield
    await close_mongo_connection()
```

#### 2. "Event loop is closed" Error

**Problem:** Async event loop scope mismatch.

**Solution:** Use session-scoped event loop:
```python
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
```

#### 3. Tests Pass Locally but Fail in CI

**Problem:** Environment differences (MongoDB, environment variables).

**Solution:**
- Ensure MongoDB service is running in CI
- Set environment variables in CI configuration
- Use test-specific configuration

```yaml
# GitHub Actions
services:
  mongodb:
    image: mongo:7
    ports:
      - 27017:27017

env:
  MONGODB_URL: mongodb://localhost:27017
  DATABASE_NAME: taiwantea_test
```

#### 4. Slow Test Execution

**Problem:** Database operations are slow.

**Solutions:**
- Use in-memory MongoDB for tests (mongomock)
- Run tests in parallel with pytest-xdist
- Use database transactions for test isolation

```bash
# Install
pip install pytest-xdist

# Run in parallel
pytest -n auto
```

#### 5. Frontend Tests Hang

**Problem:** Vitest waiting for user input in watch mode.

**Solution:** Use `--run` flag for CI:
```bash
npm test -- --run
```

#### 6. Import Errors in Tests

**Problem:** Module path issues.

**Solution:** Ensure pytest.ini has correct paths:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

#### 7. Coverage Report Not Generated

**Problem:** pytest-cov not installed or misconfigured.

**Solution:**
```bash
# Install
pip install pytest-cov

# Generate coverage
pytest --cov=src --cov-report=html
```

---

## Next Steps

### Immediate Priorities

#### 1. Increase Backend Coverage to 80% (P1)

**Admin Routes Coverage (23-25% → 80%)**
- [ ] Test POST /api/admin/products
- [ ] Test PUT /api/admin/products/{id}
- [ ] Test DELETE /api/admin/products/{id}
- [ ] Test POST /api/admin/categories
- [ ] Test PUT /api/admin/categories/{id}
- [ ] Test DELETE /api/admin/categories/{id}
- [ ] Test authentication requirements
- [ ] Test validation errors

**Auth Middleware Coverage (36% → 80%)**
- [ ] Test valid JWT token acceptance
- [ ] Test invalid JWT token rejection
- [ ] Test expired token handling
- [ ] Test missing token handling
- [ ] Test malformed token handling

**Upload Router Coverage (30% → 80%)**
- [ ] Test successful image upload
- [ ] Test thumbnail generation
- [ ] Test file type validation
- [ ] Test file size limits
- [ ] Test invalid file rejection

#### 2. Implement Frontend Tests (P1)

**Component Tests**
- [ ] ProductCard component
- [ ] CategorySection component
- [ ] Navigation component
- [ ] ProductForm component
- [ ] AdminLogin component
- [ ] ImageUpload component

**Hook Tests**
- [ ] useProducts hook
- [ ] useAuth hook

**Integration Tests**
- [ ] Customer browsing flow
- [ ] Admin login flow
- [ ] Product creation flow

#### 3. Integration Tests (P2)

**Backend Integration**
- [ ] Complete admin product CRUD flow
- [ ] Complete admin category CRUD flow
- [ ] Authentication flow (login → create → logout)
- [ ] Image upload → product creation flow

**End-to-End**
- [ ] Customer views products
- [ ] Admin creates product → appears on site
- [ ] Admin edits product → changes reflect
- [ ] Admin deletes product → removed from site

#### 4. Performance Tests (P3)

- [ ] Load testing with locust/k6
- [ ] Database query performance
- [ ] API response time benchmarks
- [ ] Frontend bundle size monitoring

#### 5. Security Tests (P3)

- [ ] SQL injection attempts (N/A for MongoDB, but test input validation)
- [ ] JWT token manipulation
- [ ] File upload security (malicious files)
- [ ] CORS policy validation
- [ ] Rate limiting tests

### Long-term Goals

1. **Achieve 90% code coverage** across all components
2. **Implement E2E tests** with Playwright or Cypress
3. **Set up automated visual regression testing** with Percy or Chromatic
4. **Performance monitoring** in production with Sentry
5. **Load testing** for production readiness

---

## Resources

### Documentation

- **pytest:** https://docs.pytest.org/
- **pytest-asyncio:** https://pytest-asyncio.readthedocs.io/
- **Vitest:** https://vitest.dev/
- **React Testing Library:** https://testing-library.com/react
- **FastAPI Testing:** https://fastapi.tiangolo.com/tutorial/testing/

### Tools

- **pytest-cov:** Coverage reporting
- **pytest-xdist:** Parallel test execution
- **pytest-watch:** Auto-run tests on file changes
- **Codecov:** Coverage tracking service
- **GitHub Actions:** CI/CD platform

### Best Practices

- **Test Pyramid:** More unit tests, fewer integration tests, even fewer E2E tests
- **TDD:** Write tests first, then implementation
- **AAA Pattern:** Arrange, Act, Assert
- **DRY:** Don't Repeat Yourself - use fixtures and helpers
- **Fast Tests:** Keep tests fast (<1s each ideal)
- **Isolated Tests:** Tests should not depend on each other
- **Clear Names:** Test names should describe what they test

---

## Summary

### Current State
- ✅ **20/20 backend contract tests passing**
- ✅ **58% code coverage**
- ✅ **Test infrastructure working**
- ⚠️ **Need more backend tests** (admin, auth, upload)
- ❌ **Frontend tests not implemented**

### Test Commands
```bash
# Backend
cd backend && source .venv/bin/activate && pytest -v

# Coverage
pytest --cov=src --cov-report=html

# Frontend (when implemented)
cd frontend && npm test
```

### Next Actions
1. Write admin router tests (P1)
2. Write auth middleware tests (P1)
3. Write upload router tests (P1)
4. Implement frontend component tests (P1)
5. Achieve 80% coverage goal (P1)

**Testing infrastructure is ready. Time to write more tests! 🚀**
