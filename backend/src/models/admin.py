"""MongoDB model for Admin entity"""

from typing import Optional
from datetime import datetime
from bson import ObjectId

from src.database import get_database


class AdminModel:
    """Admin CRUD operations"""

    @staticmethod
    async def find_by_email(email: str) -> Optional[dict]:
        """Find admin by email"""
        db = get_database()
        return await db.admins.find_one({"email": email, "isActive": True})

    @staticmethod
    async def find_by_id(admin_id: str) -> Optional[dict]:
        """Find admin by ID"""
        db = get_database()
        try:
            return await db.admins.find_one({"_id": ObjectId(admin_id), "isActive": True})
        except Exception:
            return None

    @staticmethod
    async def create(email: str, password_hash: str, name: str) -> dict:
        """Create new admin"""
        db = get_database()

        admin = {
            "email": email,
            "passwordHash": password_hash,
            "name": name,
            "isActive": True,
            "lastLoginAt": None,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }

        result = await db.admins.insert_one(admin)
        admin["_id"] = result.inserted_id

        return admin

    @staticmethod
    async def update_last_login(admin_id: str) -> bool:
        """Update last login timestamp"""
        db = get_database()

        result = await db.admins.update_one(
            {"_id": ObjectId(admin_id)},
            {
                "$set": {
                    "lastLoginAt": datetime.utcnow(),
                    "updatedAt": datetime.utcnow()
                }
            }
        )

        return result.modified_count > 0

    @staticmethod
    async def update(admin_id: str, **updates) -> bool:
        """Update admin fields"""
        db = get_database()

        updates["updatedAt"] = datetime.utcnow()

        result = await db.admins.update_one(
            {"_id": ObjectId(admin_id)},
            {"$set": updates}
        )

        return result.modified_count > 0
