"""MongoDB model for Category entity"""

from typing import List, Optional
from datetime import datetime
from src.database import get_database


class CategoryModel:
    """Category CRUD operations"""

    @staticmethod
    async def get_all_active() -> List[dict]:
        """Get all active categories sorted by display order"""
        db = get_database()

        cursor = db.categories.find({"isActive": True}).sort("displayOrder", 1)
        categories = await cursor.to_list(length=None)

        return categories

    @staticmethod
    async def get_by_id(category_id: str) -> Optional[dict]:
        """Get category by ID"""
        db = get_database()
        return await db.categories.find_one({"_id": category_id, "isActive": True})

    @staticmethod
    async def exists(category_id: str) -> bool:
        """Check if category exists and is active"""
        db = get_database()
        count = await db.categories.count_documents({"_id": category_id, "isActive": True})
        return count > 0

    @staticmethod
    async def create(category_data: dict) -> dict:
        """Create new category"""
        db = get_database()

        # Check if ID already exists
        existing = await db.categories.find_one({"_id": category_data["_id"]})
        if existing:
            raise ValueError(f"Category with ID '{category_data['_id']}' already exists")

        category = {
            **category_data,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
            "isActive": True
        }

        await db.categories.insert_one(category)
        return category

    @staticmethod
    async def update(category_id: str, updates: dict) -> bool:
        """Update category"""
        db = get_database()

        updates["updatedAt"] = datetime.utcnow()

        result = await db.categories.update_one(
            {"_id": category_id},
            {"$set": updates}
        )

        return result.modified_count > 0

    @staticmethod
    async def delete(category_id: str) -> bool:
        """Soft delete category by setting isActive to False"""
        db = get_database()

        result = await db.categories.update_one(
            {"_id": category_id},
            {"$set": {"isActive": False, "updatedAt": datetime.utcnow()}}
        )

        return result.modified_count > 0
