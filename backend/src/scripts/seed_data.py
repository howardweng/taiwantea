"""Seed initial data: categories, indexes, and admin user"""

import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def seed_database():
    """Seed initial data into MongoDB"""

    mongodb_url = os.getenv("MONGODB_URL")
    if not mongodb_url:
        raise ValueError("MONGODB_URL environment variable is required")
    client = AsyncIOMotorClient(mongodb_url, serverSelectionTimeoutMS=5000)

    # Extract database name from URL
    db_name = mongodb_url.split("/")[-1].split("?")[0]
    db = client[db_name]

    print(f"🌱 Seeding database: {db_name}")

    # === 1. Create Categories ===
    categories = [
        {
            "_id": "green-tea",
            "name": "Green Tea",
            "description": "Fresh, delicate green teas from China and Japan. Rich in antioxidants with vegetal, grassy notes.",
            "displayOrder": 1,
            "isActive": True,
            "createdAt": datetime.utcnow()
        },
        {
            "_id": "black-tea",
            "name": "Black Tea",
            "description": "Full-bodied, oxidized teas with rich, malty flavors. Perfect for morning or afternoon.",
            "displayOrder": 2,
            "isActive": True,
            "createdAt": datetime.utcnow()
        },
        {
            "_id": "oolong-tea",
            "name": "Oolong Tea",
            "description": "Semi-oxidized teas from Taiwan and China. Complex flavors ranging from floral to roasted.",
            "displayOrder": 3,
            "isActive": True,
            "createdAt": datetime.utcnow()
        },
        {
            "_id": "white-tea",
            "name": "White Tea",
            "description": "Minimally processed, delicate teas with subtle, sweet flavors. Highest antioxidant content.",
            "displayOrder": 4,
            "isActive": True,
            "createdAt": datetime.utcnow()
        },
        {
            "_id": "herbal-tea",
            "name": "Herbal Tea",
            "description": "Caffeine-free infusions of herbs, flowers, and fruits. Soothing and aromatic.",
            "displayOrder": 5,
            "isActive": True,
            "createdAt": datetime.utcnow()
        },
        {
            "_id": "puerh-tea",
            "name": "Pu-erh Tea",
            "description": "Aged, fermented teas from Yunnan, China. Earthy, smooth, and improves with age.",
            "displayOrder": 6,
            "isActive": True,
            "createdAt": datetime.utcnow()
        }
    ]

    # Clear existing categories
    await db.categories.delete_many({})

    # Insert categories
    await db.categories.insert_many(categories)
    print(f"✓ Inserted {len(categories)} categories")

    # === 2. Create Indexes ===

    # Categories indexes
    await db.categories.create_index("displayOrder")
    await db.categories.create_index("isActive")
    print("✓ Created categories indexes")

    # Products indexes
    await db.products.create_index("category")
    await db.products.create_index("displayOrder")
    await db.products.create_index([("createdAt", -1)])  # Descending
    print("✓ Created products indexes")

    # Admins indexes
    await db.admins.create_index("email", unique=True)
    await db.admins.create_index("isActive")
    print("✓ Created admins indexes")

    # === 3. Create Initial Admin User ===

    # Check if admin already exists
    existing_admin = await db.admins.find_one({"email": "admin@taiwantea.com"})

    if not existing_admin:
        admin_user = {
            "email": "admin@taiwantea.com",
            "passwordHash": pwd_context.hash("Admin123!"),
            "name": "Tea Admin",
            "isActive": True,
            "lastLoginAt": None,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }

        await db.admins.insert_one(admin_user)
        print("✓ Created initial admin user")
        print("  Email: admin@taiwantea.com")
        print("  Password: Admin123!")
    else:
        print("⚠ Admin user already exists, skipping")

    # === 4. Create Sample Products (Optional) ===

    sample_products = [
        {
            "name": "Dragon Well Green Tea",
            "category": "green-tea",
            "description": "Premium Longjing green tea from Hangzhou, China. Renowned for its jade color, delicate aroma, and sweet aftertaste. Hand-picked leaves from high mountain gardens. Brewing: 175°F (80°C), 2-3 minutes.",
            "price": 24.99,
            "imageUrl": "/uploads/products/dragon-well.jpg",
            "thumbnailUrl": "/uploads/products/thumbs/dragon-well.jpg",
            "inStock": True,
            "displayOrder": 1,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        },
        {
            "name": "Assam Black Tea",
            "category": "black-tea",
            "description": "Bold, malty black tea from Assam, India. Full-bodied with rich caramel notes. Perfect with milk and sugar. Brewing: 212°F (100°C), 3-5 minutes.",
            "price": 18.99,
            "imageUrl": "/uploads/products/assam-black.jpg",
            "thumbnailUrl": "/uploads/products/thumbs/assam-black.jpg",
            "inStock": True,
            "displayOrder": 1,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        },
        {
            "name": "Alishan Oolong",
            "category": "oolong-tea",
            "description": "High mountain oolong from Taiwan's Alishan region. Floral, creamy, with a lingering sweetness. Multiple infusions reveal complex flavors. Brewing: 195°F (90°C), 2-3 minutes.",
            "price": 32.99,
            "imageUrl": "/uploads/products/alishan-oolong.jpg",
            "thumbnailUrl": "/uploads/products/thumbs/alishan-oolong.jpg",
            "inStock": True,
            "displayOrder": 1,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }
    ]

    # Only insert if products collection is empty
    product_count = await db.products.count_documents({})
    if product_count == 0:
        await db.products.insert_many(sample_products)
        print(f"✓ Inserted {len(sample_products)} sample products")
    else:
        print(f"⚠ Products already exist ({product_count}), skipping samples")

    print("\n✅ Database seeding complete!")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed_database())
