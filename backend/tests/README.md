# Backend Tests

## Test Structure

```
tests/
├── conftest.py          # Pytest fixtures and configuration
├── contract/            # API contract tests
│   └── test_products_api.py
└── integration/         # Integration tests (to be implemented)
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/contract/test_products_api.py

# Run with verbose output
pytest -v

# Run specific test
pytest tests/contract/test_products_api.py::TestCategoriesAPI::test_get_categories_returns_200
```

## Test Categories

### Contract Tests (`tests/contract/`)
Test API endpoint contracts to ensure:
- Correct HTTP status codes
- Proper response structure
- Required fields present
- Correct data types

### Integration Tests (`tests/integration/`)
Test complete user flows through the system.

## Note on Async Testing

The current tests require additional setup for async database connections in test environment.
For production deployment, consider:
1. Using test database separate from development
2. Implementing database fixtures that reset state between tests
3. Using `pytest-asyncio` with proper event loop management

## Manual Testing

While automated tests are being set up, you can test the API manually:

```bash
# Test categories endpoint
curl http://localhost:8000/api/categories

# Test products endpoint
curl http://localhost:8000/api/products

# Test with category filter
curl "http://localhost:8000/api/products?category=green-tea"

# Test pagination
curl "http://localhost:8000/api/products?limit=5&skip=0"
```

## API Documentation

Interactive API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
