"""
Database Indexes Setup

Creates indexes for better query performance
"""

from motor.motor_asyncio import AsyncIOMotorClient
from src.config import settings
import asyncio


async def create_indexes():
    """Create database indexes for optimal performance"""

    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]

    print("Creating database indexes...")

    # Products Collection Indexes
    print("  - Creating products indexes...")
    await db.products.create_index("category")  # Filter by category
    await db.products.create_index("inStock")   # Filter by stock status
    await db.products.create_index([("category", 1), ("inStock", 1)])  # Compound index
    await db.products.create_index("displayOrder")  # Sort by display order
    await db.products.create_index("createdAt")  # Sort by creation date

    # Categories Collection Indexes
    print("  - Creating categories indexes...")
    await db.categories.create_index("isActive")  # Filter active categories
    await db.categories.create_index("displayOrder")  # Sort by display order
    await db.categories.create_index([("isActive", 1), ("displayOrder", 1)])  # Compound index

    # Admins Collection Indexes
    print("  - Creating admins indexes...")
    await db.admins.create_index("email", unique=True)  # Unique email for login

    print("✓ All indexes created successfully!")

    client.close()


if __name__ == "__main__":
    asyncio.run(create_indexes())
