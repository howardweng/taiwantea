"""Site Settings Model - Manages site-wide configuration"""

from datetime import datetime
from src.database import get_database


class SiteSettingsModel:
    """
    Site Settings Model

    Stores site-wide configuration like logo, brand name, etc.
    Only one settings document exists in the database.
    """

    @staticmethod
    async def get():
        """Get site settings (returns single document)"""
        db = get_database()
        settings = await db.site_settings.find_one()
        return settings

    @staticmethod
    async def create(settings_data: dict):
        """Create initial site settings"""
        db = get_database()
        settings_data["createdAt"] = datetime.utcnow()
        settings_data["updatedAt"] = datetime.utcnow()
        result = await db.site_settings.insert_one(settings_data)
        settings_data["_id"] = result.inserted_id
        return settings_data

    @staticmethod
    async def update(updates: dict) -> bool:
        """Update site settings (updates the single record)"""
        db = get_database()
        updates["updatedAt"] = datetime.utcnow()

        # Get existing settings
        existing = await db.site_settings.find_one()

        if existing:
            # Update existing
            result = await db.site_settings.update_one(
                {"_id": existing["_id"]},
                {"$set": updates}
            )
            return result.modified_count > 0
        else:
            # Create new if doesn't exist
            await SiteSettingsModel.create(updates)
            return True
