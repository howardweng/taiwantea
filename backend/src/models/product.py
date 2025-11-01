"""MongoDB model for Product entity"""

from typing import List, Optional
from datetime import datetime
from bson import ObjectId

from src.database import get_database


class ProductModel:
    """Product CRUD operations"""

    @staticmethod
    async def get_all(
        category: Optional[str] = None,
        in_stock_only: bool = True,
        limit: Optional[int] = None,
        skip: int = 0
    ) -> List[dict]:
        """Get all products with optional filters"""
        db = get_database()

        # Build query
        query = {}
        if in_stock_only:
            query["inStock"] = True
        if category:
            query["category"] = category

        # Execute query
        cursor = db.products.find(query).sort("displayOrder", 1).skip(skip)

        if limit:
            cursor = cursor.limit(limit)

        products = await cursor.to_list(length=None)
        return products

    @staticmethod
    async def get_by_id(product_id: str) -> Optional[dict]:
        """Get product by ID"""
        db = get_database()

        try:
            product = await db.products.find_one({"_id": ObjectId(product_id)})

            # Sort images by displayOrder if present
            if product and "images" in product and product["images"]:
                product["images"] = sorted(product["images"], key=lambda x: x.get("displayOrder", 0))

            return product
        except Exception:
            return None

    @staticmethod
    async def filter_by_category(category: str) -> List[dict]:
        """Get all in-stock products in a category"""
        db = get_database()

        cursor = db.products.find({
            "category": category,
            "inStock": True
        }).sort("displayOrder", 1)

        products = await cursor.to_list(length=None)
        return products

    @staticmethod
    async def count(category: Optional[str] = None, in_stock_only: bool = True) -> int:
        """Count products with optional filters"""
        db = get_database()

        query = {}
        if in_stock_only:
            query["inStock"] = True
        if category:
            query["category"] = category

        return await db.products.count_documents(query)

    @staticmethod
    async def create(product_data: dict) -> dict:
        """Create new product"""
        db = get_database()

        product = {
            **product_data,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }

        result = await db.products.insert_one(product)
        product["_id"] = result.inserted_id

        return product

    @staticmethod
    async def update(product_id: str, updates: dict) -> bool:
        """Update product"""
        db = get_database()

        updates["updatedAt"] = datetime.utcnow()

        result = await db.products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": updates}
        )

        return result.modified_count > 0

    @staticmethod
    async def delete(product_id: str) -> bool:
        """Delete product"""
        db = get_database()

        result = await db.products.delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count > 0
