"""MongoDB model for Carousel entity"""

from typing import List, Optional
from datetime import datetime
from bson import ObjectId

from src.database import get_database


class CarouselModel:
    """Carousel CRUD operations"""

    @staticmethod
    async def get_all(active_only: bool = True) -> List[dict]:
        """Get all carousel slides with optional active filter"""
        db = get_database()

        # Build query
        query = {}
        if active_only:
            query["active"] = True

        # Execute query - sort by displayOrder
        cursor = db.carousel.find(query).sort("displayOrder", 1)
        slides = await cursor.to_list(length=None)
        return slides

    @staticmethod
    async def get_by_id(slide_id: str) -> Optional[dict]:
        """Get carousel slide by ID"""
        db = get_database()

        try:
            return await db.carousel.find_one({"_id": ObjectId(slide_id)})
        except Exception:
            return None

    @staticmethod
    async def create(slide_data: dict) -> dict:
        """Create new carousel slide"""
        db = get_database()

        slide = {
            **slide_data,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }

        result = await db.carousel.insert_one(slide)
        slide["_id"] = result.inserted_id

        return slide

    @staticmethod
    async def update(slide_id: str, updates: dict) -> bool:
        """Update carousel slide"""
        db = get_database()

        updates["updatedAt"] = datetime.utcnow()

        result = await db.carousel.update_one(
            {"_id": ObjectId(slide_id)},
            {"$set": updates}
        )

        return result.modified_count > 0

    @staticmethod
    async def delete(slide_id: str) -> bool:
        """Delete carousel slide"""
        db = get_database()

        result = await db.carousel.delete_one({"_id": ObjectId(slide_id)})
        return result.deleted_count > 0

    @staticmethod
    async def count(active_only: bool = True) -> int:
        """Count carousel slides"""
        db = get_database()

        query = {}
        if active_only:
            query["active"] = True

        return await db.carousel.count_documents(query)
