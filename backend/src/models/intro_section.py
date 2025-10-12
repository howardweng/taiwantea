"""MongoDB model for Intro Section entity"""

from typing import Optional
from datetime import datetime
from bson import ObjectId

from src.database import get_database


class IntroSectionModel:
    """Intro Section CRUD operations"""

    @staticmethod
    async def get() -> Optional[dict]:
        """Get the intro section content (only one record)"""
        db = get_database()
        return await db.intro_section.find_one()

    @staticmethod
    async def create(section_data: dict) -> dict:
        """Create intro section"""
        db = get_database()

        section = {
            **section_data,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }

        result = await db.intro_section.insert_one(section)
        section["_id"] = result.inserted_id

        return section

    @staticmethod
    async def update(updates: dict) -> bool:
        """Update intro section (updates the single record)"""
        db = get_database()

        updates["updatedAt"] = datetime.utcnow()

        # Get existing record
        existing = await db.intro_section.find_one()

        if existing:
            result = await db.intro_section.update_one(
                {"_id": existing["_id"]},
                {"$set": updates}
            )
            return result.modified_count > 0
        else:
            # Create if doesn't exist
            await IntroSectionModel.create(updates)
            return True

    @staticmethod
    async def delete() -> bool:
        """Delete intro section"""
        db = get_database()
        result = await db.intro_section.delete_many({})
        return result.deleted_count > 0
