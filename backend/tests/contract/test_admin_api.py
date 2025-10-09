"""
Contract tests for Admin API endpoints

Tests for:
- Authentication (login, logout, get current user)
- Admin Product Management (CRUD operations)
- Admin Category Management (CRUD operations)

NOTE: These tests use the seeded database data (admin@taiwantea.com / Admin123!)
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi import status
from bson import ObjectId


# ============================================================================
# AUTHENTICATION TESTS
# ============================================================================

@pytest.mark.asyncio
class TestAuthentication:

    async def test_login_with_valid_credentials_returns_200(
        self, async_client: AsyncClient
    ):
        """Should successfully login with valid credentials"""
        response = await async_client.post(
            "/api/auth/login",
            json={
                "email": "admin@taiwantea.com",
                "password": "Admin123!"
            }
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "admin" in data["data"]
        assert data["data"]["admin"]["email"] == "admin@taiwantea.com"

        # Check cookie is set
        assert "accessToken" in response.cookies

    async def test_login_with_invalid_email_returns_401(
        self, async_client: AsyncClient
    ):
        """Should return 401 with invalid email"""
        response = await async_client.post(
            "/api/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "WrongPassword123!"
            }
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_login_with_invalid_password_returns_401(
        self, async_client: AsyncClient
    ):
        """Should return 401 with invalid password"""
        response = await async_client.post(
            "/api/auth/login",
            json={
                "email": "admin@taiwantea.com",
                "password": "WrongPassword123!"
            }
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_get_current_user_without_auth_returns_401(
        self, async_client: AsyncClient
    ):
        """Should return 401 when not authenticated"""
        response = await async_client.get("/api/auth/me")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_get_current_user_with_auth_returns_200(
        self, async_client: AsyncClient
    ):
        """Should return current user profile when authenticated"""
        # Login first
        login_response = await async_client.post(
            "/api/auth/login",
            json={
                "email": "admin@taiwantea.com",
                "password": "Admin123!"
            }
        )

        # Get profile
        response = await async_client.get("/api/auth/me")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert data["data"]["email"] == "admin@taiwantea.com"

    async def test_logout_clears_cookie(
        self, async_client: AsyncClient
    ):
        """Should successfully logout and clear cookie"""
        # Login first
        await async_client.post(
            "/api/auth/login",
            json={
                "email": "admin@taiwantea.com",
                "password": "Admin123!"
            }
        )

        # Logout
        response = await async_client.post("/api/auth/logout")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True


# ============================================================================
# ADMIN PRODUCTS TESTS
# ============================================================================

@pytest.mark.asyncio
class TestAdminProducts:

    async def test_create_product_requires_authentication(
        self, async_client: AsyncClient
    ):
        """Should return 401 when creating product without auth"""
        response = await async_client.post(
            "/api/admin/products",
            json={
                "name": "New Tea",
                "category": "green-tea",
                "price": 25.99,
                "description": "New tea product",
                "imageUrl": "https://example.com/new.jpg",
                "inStock": True
            }
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_create_product_with_valid_data_returns_200(
        self, async_client: AsyncClient
    ):
        """Should successfully create product with valid data"""
        # Login first
        await async_client.post(
            "/api/auth/login",
            json={
                "email": "admin@taiwantea.com",
                "password": "Admin123!"
            }
        )

        product_data = {
            "name": "New Test Tea",
            "category": "green-tea",
            "price": 35.99,
            "description": "A newly created test tea",
            "imageUrl": "https://example.com/new-test.jpg",
            "thumbnailUrl": "https://example.com/new-test-thumb.jpg",
            "inStock": True,
            "displayOrder": 50
        }

        response = await async_client.post(
            "/api/admin/products",
            json=product_data
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "_id" in data
        assert data["name"] == product_data["name"]
        assert data["price"] == product_data["price"]
        assert data["category"] == product_data["category"]

        # Cleanup - delete the created product
        product_id = data["_id"]
        await async_client.delete(f"/api/admin/products/{product_id}")

    async def test_create_product_with_missing_fields_returns_422(
        self, async_client: AsyncClient
    ):
        """Should return 422 when required fields are missing"""
        # Login first
        await async_client.post(
            "/api/auth/login",
            json={
                "email": "admin@taiwantea.com",
                "password": "Admin123!"
            }
        )

        response = await async_client.post(
            "/api/admin/products",
            json={"name": "Incomplete Product"}
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_update_product_requires_authentication(
        self, async_client: AsyncClient
    ):
        """Should return 401 when updating product without auth"""
        # Get first product ID
        products_response = await async_client.get("/api/products")
        products = products_response.json()["products"]
        if products:
            product_id = products[0]["_id"]

            response = await async_client.put(
                f"/api/admin/products/{product_id}",
                json={"price": 39.99}
            )

            assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_update_product_with_invalid_id_returns_400(
        self, async_client: AsyncClient
    ):
        """Should return 400 with invalid product ID format"""
        # Login first
        await async_client.post(
            "/api/auth/login",
            json={
                "email": "admin@taiwantea.com",
                "password": "Admin123!"
            }
        )

        response = await async_client.put(
            "/api/admin/products/invalid-id",
            json={"price": 45.99}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_update_product_nonexistent_returns_404(
        self, async_client: AsyncClient
    ):
        """Should return 404 when product doesn't exist"""
        # Login first
        await async_client.post(
            "/api/auth/login",
            json={
                "email": "admin@taiwantea.com",
                "password": "Admin123!"
            }
        )

        fake_id = str(ObjectId())

        response = await async_client.put(
            f"/api/admin/products/{fake_id}",
            json={"price": 45.99}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_delete_product_requires_authentication(
        self, async_client: AsyncClient
    ):
        """Should return 401 when deleting product without auth"""
        # Get first product ID
        products_response = await async_client.get("/api/products")
        products = products_response.json()["products"]
        if products:
            product_id = products[0]["_id"]

            response = await async_client.delete(
                f"/api/admin/products/{product_id}"
            )

            assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_delete_product_with_invalid_id_returns_400(
        self, async_client: AsyncClient
    ):
        """Should return 400 with invalid product ID format"""
        # Login first
        await async_client.post(
            "/api/auth/login",
            json={
                "email": "admin@taiwantea.com",
                "password": "Admin123!"
            }
        )

        response = await async_client.delete(
            "/api/admin/products/invalid-id"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_delete_product_nonexistent_returns_404(
        self, async_client: AsyncClient
    ):
        """Should return 404 when product doesn't exist"""
        # Login first
        await async_client.post(
            "/api/auth/login",
            json={
                "email": "admin@taiwantea.com",
                "password": "Admin123!"
            }
        )

        fake_id = str(ObjectId())

        response = await async_client.delete(
            f"/api/admin/products/{fake_id}"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_all_products_admin_requires_authentication(
        self, async_client: AsyncClient
    ):
        """Should return 401 when getting admin products without auth"""
        response = await async_client.get("/api/admin/products")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_get_all_products_admin_returns_200(
        self, async_client: AsyncClient
    ):
        """Should return all products including out of stock"""
        # Login first
        await async_client.post(
            "/api/auth/login",
            json={
                "email": "admin@taiwantea.com",
                "password": "Admin123!"
            }
        )

        response = await async_client.get("/api/admin/products")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "products" in data
        assert "total" in data
        assert isinstance(data["products"], list)

    async def test_update_product_with_valid_data_returns_200(
        self, async_client: AsyncClient
    ):
        """Should successfully update a product"""
        # Login first
        await async_client.post(
            "/api/auth/login",
            json={
                "email": "admin@taiwantea.com",
                "password": "Admin123!"
            }
        )

        # Get first product
        products_response = await async_client.get("/api/products")
        products = products_response.json()["products"]

        if products:
            product_id = products[0]["_id"]
            original_price = products[0]["price"]

            # Update the product
            new_price = original_price + 5.0
            response = await async_client.put(
                f"/api/admin/products/{product_id}",
                json={"price": new_price}
            )

            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["price"] == new_price

            # Restore original price
            await async_client.put(
                f"/api/admin/products/{product_id}",
                json={"price": original_price}
            )

    async def test_update_product_with_no_fields_returns_400(
        self, async_client: AsyncClient
    ):
        """Should return 400 when no update fields provided"""
        # Login first
        await async_client.post(
            "/api/auth/login",
            json={
                "email": "admin@taiwantea.com",
                "password": "Admin123!"
            }
        )

        # Get first product
        products_response = await async_client.get("/api/products")
        products = products_response.json()["products"]

        if products:
            product_id = products[0]["_id"]

            response = await async_client.put(
                f"/api/admin/products/{product_id}",
                json={}
            )

            assert response.status_code == status.HTTP_400_BAD_REQUEST


# ============================================================================
# ADMIN CATEGORIES TESTS
# ============================================================================

@pytest.mark.asyncio
class TestAdminCategories:

    async def test_create_category_requires_authentication(
        self, async_client: AsyncClient
    ):
        """Should return 401 when creating category without auth"""
        response = await async_client.post(
            "/api/admin/categories",
            json={
                "id": "new-category",
                "name": "New Category",
                "displayOrder": 10
            }
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_create_category_with_valid_data_returns_200(
        self, async_client: AsyncClient
    ):
        """Should successfully create category with valid data"""
        # Login first
        await async_client.post(
            "/api/auth/login",
            json={
                "email": "admin@taiwantea.com",
                "password": "Admin123!"
            }
        )

        # Use unique ID based on timestamp
        import time
        unique_id = f"test-category-{int(time.time())}"

        category_data = {
            "id": unique_id,
            "name": "New Test Category",
            "description": "A test category",
            "displayOrder": 88,
            "isActive": True
        }

        response = await async_client.post(
            "/api/admin/categories",
            json=category_data
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["_id"] == category_data["id"]
        assert data["name"] == category_data["name"]

        # Cleanup
        await async_client.delete(f"/api/admin/categories/{category_data['id']}")

    async def test_update_category_requires_authentication(
        self, async_client: AsyncClient
    ):
        """Should return 401 when updating category without auth"""
        response = await async_client.put(
            "/api/admin/categories/green-tea",
            json={"name": "Updated Name"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_update_category_with_valid_data_returns_200(
        self, async_client: AsyncClient
    ):
        """Should successfully update category"""
        # Login first
        await async_client.post(
            "/api/auth/login",
            json={
                "email": "admin@taiwantea.com",
                "password": "Admin123!"
            }
        )

        # Update green-tea category
        response = await async_client.put(
            "/api/admin/categories/green-tea",
            json={"description": "Updated description for testing"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["description"] == "Updated description for testing"

        # Restore original
        await async_client.put(
            "/api/admin/categories/green-tea",
            json={"description": "Fresh and delicate green teas"}
        )

    async def test_update_category_with_no_fields_returns_400(
        self, async_client: AsyncClient
    ):
        """Should return 400 when no update fields provided"""
        # Login first
        await async_client.post(
            "/api/auth/login",
            json={
                "email": "admin@taiwantea.com",
                "password": "Admin123!"
            }
        )

        response = await async_client.put(
            "/api/admin/categories/green-tea",
            json={}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_update_category_nonexistent_returns_404(
        self, async_client: AsyncClient
    ):
        """Should return 404 when category doesn't exist"""
        # Login first
        await async_client.post(
            "/api/auth/login",
            json={
                "email": "admin@taiwantea.com",
                "password": "Admin123!"
            }
        )

        response = await async_client.put(
            "/api/admin/categories/nonexistent-category",
            json={"name": "Updated Name"}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_delete_category_requires_authentication(
        self, async_client: AsyncClient
    ):
        """Should return 401 when deleting category without auth"""
        response = await async_client.delete(
            "/api/admin/categories/green-tea"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_delete_category_nonexistent_returns_404(
        self, async_client: AsyncClient
    ):
        """Should return 404 when category doesn't exist"""
        # Login first
        await async_client.post(
            "/api/auth/login",
            json={
                "email": "admin@taiwantea.com",
                "password": "Admin123!"
            }
        )

        response = await async_client.delete(
            "/api/admin/categories/nonexistent-category"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
