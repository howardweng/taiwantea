"""
Contract tests for Products API

Tests verify that API endpoints return correct response formats
according to the API contract specification.
"""

import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
class TestCategoriesAPI:
    """Test /api/categories endpoint contract"""

    async def test_get_categories_returns_200(self, async_client: AsyncClient):
        """Should return 200 OK"""
        response = await async_client.get("/api/categories")
        assert response.status_code == status.HTTP_200_OK

    async def test_get_categories_returns_json(self, async_client: AsyncClient):
        """Should return JSON content type"""
        response = await async_client.get("/api/categories")
        assert response.headers["content-type"] == "application/json"

    async def test_get_categories_response_structure(self, async_client: AsyncClient):
        """Should return correct response structure"""
        response = await async_client.get("/api/categories")
        data = response.json()

        # Should have categories array
        assert "categories" in data
        assert isinstance(data["categories"], list)

    async def test_category_object_structure(self, async_client: AsyncClient):
        """Each category should have required fields"""
        response = await async_client.get("/api/categories")
        data = response.json()

        if len(data["categories"]) > 0:
            category = data["categories"][0]

            # Required fields
            assert "_id" in category
            assert "name" in category
            assert "displayOrder" in category
            assert "isActive" in category

            # Type checks
            assert isinstance(category["_id"], str)
            assert isinstance(category["name"], str)
            assert isinstance(category["displayOrder"], int)
            assert isinstance(category["isActive"], bool)

    async def test_categories_sorted_by_display_order(self, async_client: AsyncClient):
        """Categories should be sorted by displayOrder"""
        response = await async_client.get("/api/categories")
        data = response.json()

        if len(data["categories"]) > 1:
            orders = [cat["displayOrder"] for cat in data["categories"]]
            assert orders == sorted(orders), "Categories should be sorted by displayOrder"


@pytest.mark.asyncio
class TestProductsAPI:
    """Test /api/products endpoint contract"""

    async def test_get_products_returns_200(self, async_client: AsyncClient):
        """Should return 200 OK"""
        response = await async_client.get("/api/products")
        assert response.status_code == status.HTTP_200_OK

    async def test_get_products_returns_json(self, async_client: AsyncClient):
        """Should return JSON content type"""
        response = await async_client.get("/api/products")
        assert response.headers["content-type"] == "application/json"

    async def test_get_products_response_structure(self, async_client: AsyncClient):
        """Should return correct response structure"""
        response = await async_client.get("/api/products")
        data = response.json()

        # Should have products array and total count
        assert "products" in data
        assert "total" in data
        assert isinstance(data["products"], list)
        assert isinstance(data["total"], int)

    async def test_product_object_structure(self, async_client: AsyncClient):
        """Each product should have required fields"""
        response = await async_client.get("/api/products")
        data = response.json()

        if len(data["products"]) > 0:
            product = data["products"][0]

            # Required fields
            required_fields = [
                "_id", "name", "category", "description",
                "price", "imageUrl", "inStock"
            ]
            for field in required_fields:
                assert field in product, f"Product missing required field: {field}"

            # Type checks
            assert isinstance(product["_id"], str)
            assert isinstance(product["name"], str)
            assert isinstance(product["category"], str)
            assert isinstance(product["description"], str)
            assert isinstance(product["price"], (int, float))
            assert isinstance(product["imageUrl"], str)
            assert isinstance(product["inStock"], bool)

    async def test_get_products_with_category_filter(self, async_client: AsyncClient):
        """Should filter products by category"""
        response = await async_client.get("/api/products?category=green-tea")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        if len(data["products"]) > 0:
            # All products should be in green-tea category
            for product in data["products"]:
                assert product["category"] == "green-tea"

    async def test_get_products_with_invalid_category(self, async_client: AsyncClient):
        """Should return 404 for invalid category"""
        response = await async_client.get("/api/products?category=invalid-category")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_products_pagination(self, async_client: AsyncClient):
        """Should support limit and skip parameters"""
        # Get first 5 products
        response = await async_client.get("/api/products?limit=5")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert len(data["products"]) <= 5

        # Skip first 2 products
        response2 = await async_client.get("/api/products?skip=2&limit=5")
        assert response2.status_code == status.HTTP_200_OK

    async def test_get_products_in_stock_filter(self, async_client: AsyncClient):
        """Should filter by stock status"""
        response = await async_client.get("/api/products?in_stock_only=true")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        # All returned products should be in stock
        for product in data["products"]:
            assert product["inStock"] is True

    async def test_total_count_matches_filter(self, async_client: AsyncClient):
        """Total count should match filtered results"""
        response = await async_client.get("/api/products?in_stock_only=true")
        data = response.json()

        # Total should be >= number of returned products
        assert data["total"] >= len(data["products"])


@pytest.mark.asyncio
class TestSingleProductAPI:
    """Test /api/products/{id} endpoint contract"""

    async def test_get_product_by_id_returns_200(self, async_client: AsyncClient):
        """Should return 200 OK for valid product ID"""
        # First, get a product ID
        response = await async_client.get("/api/products?limit=1")
        data = response.json()

        if len(data["products"]) > 0:
            product_id = data["products"][0]["_id"]

            response2 = await async_client.get(f"/api/products/{product_id}")
            assert response2.status_code == status.HTTP_200_OK

    async def test_get_product_by_id_response_structure(self, async_client: AsyncClient):
        """Should return single product object"""
        # First, get a product ID
        response = await async_client.get("/api/products?limit=1")
        data = response.json()

        if len(data["products"]) > 0:
            product_id = data["products"][0]["_id"]

            response2 = await async_client.get(f"/api/products/{product_id}")
            product = response2.json()

            # Should be a single object, not an array
            assert isinstance(product, dict)
            assert "_id" in product
            assert product["_id"] == product_id

    async def test_get_product_invalid_id_returns_400(self, async_client: AsyncClient):
        """Should return 400 for invalid ObjectId format"""
        response = await async_client.get("/api/products/invalid-id")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_get_product_nonexistent_id_returns_404(self, async_client: AsyncClient):
        """Should return 404 for non-existent product"""
        # Valid ObjectId format but doesn't exist
        fake_id = "507f1f77bcf86cd799439011"
        response = await async_client.get(f"/api/products/{fake_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
class TestAPIErrorHandling:
    """Test API error handling"""

    async def test_invalid_query_parameters(self, async_client: AsyncClient):
        """Should handle invalid query parameters gracefully"""
        # Invalid limit value
        response = await async_client.get("/api/products?limit=abc")
        assert response.status_code in [400, 422]  # Bad request or validation error

        # Negative skip value
        response2 = await async_client.get("/api/products?skip=-1")
        assert response2.status_code in [400, 422]

    async def test_api_returns_proper_error_format(self, async_client: AsyncClient):
        """Error responses should have consistent format"""
        response = await async_client.get("/api/products/invalid-id")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        data = response.json()
        assert "detail" in data  # FastAPI standard error format
