"""Business logic for products and categories"""

from typing import List, Optional

from src.models.category import CategoryModel
from src.models.product import ProductModel


class ProductService:
    """Product-related business logic"""

    @staticmethod
    async def get_all_categories() -> List[dict]:
        """Get all active categories sorted by display order"""
        return await CategoryModel.get_all_active()

    @staticmethod
    async def get_all_products(
        category: Optional[str] = None,
        in_stock_only: bool = True,
        limit: Optional[int] = None,
        skip: int = 0
    ) -> tuple[List[dict], int]:
        """
        Get products with optional filters

        Returns:
            tuple of (products list, total count)
        """
        # Validate category exists if provided
        if category:
            if not await CategoryModel.exists(category):
                raise ValueError(f"Category '{category}' not found")

        products = await ProductModel.get_all(
            category=category,
            in_stock_only=in_stock_only,
            limit=limit,
            skip=skip
        )

        total = await ProductModel.count(
            category=category,
            in_stock_only=in_stock_only
        )

        return products, total

    @staticmethod
    async def get_product_by_id(product_id: str) -> Optional[dict]:
        """Get single product by ID"""
        return await ProductModel.get_by_id(product_id)

    @staticmethod
    async def get_products_by_category(category: str) -> List[dict]:
        """Get all in-stock products in a specific category"""
        # Validate category exists
        if not await CategoryModel.exists(category):
            raise ValueError(f"Category '{category}' not found")

        return await ProductModel.filter_by_category(category)

    @staticmethod
    async def create_product(product_data: dict) -> str:
        """Create a new product"""
        # Validate category exists
        if not await CategoryModel.exists(product_data["category"]):
            raise ValueError(f"Category '{product_data['category']}' not found")

        product = await ProductModel.create(product_data)
        return str(product["_id"])

    @staticmethod
    async def update_product(product_id: str, update_data: dict) -> bool:
        """Update an existing product"""
        # Validate category if being updated
        if "category" in update_data:
            if not await CategoryModel.exists(update_data["category"]):
                raise ValueError(f"Category '{update_data['category']}' not found")

        return await ProductModel.update(product_id, update_data)

    @staticmethod
    async def delete_product(product_id: str) -> bool:
        """Delete a product"""
        return await ProductModel.delete(product_id)
