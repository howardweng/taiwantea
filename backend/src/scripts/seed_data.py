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
            "name": "綠茶",
            "description": "來自中國和日本的清新、細緻綠茶。富含抗氧化劑，帶有植物、草本香氣。",
            "displayOrder": 1,
            "isActive": True,
            "createdAt": datetime.utcnow()
        },
        {
            "_id": "black-tea",
            "name": "紅茶",
            "description": "濃郁醇厚的全發酵茶，帶有豐富的麥芽風味。適合早晨或下午品飲。",
            "displayOrder": 2,
            "isActive": True,
            "createdAt": datetime.utcnow()
        },
        {
            "_id": "oolong-tea",
            "name": "烏龍茶",
            "description": "來自台灣和中國的半發酵茶。複雜風味從花香到焙火香皆有。",
            "displayOrder": 3,
            "isActive": True,
            "createdAt": datetime.utcnow()
        },
        {
            "_id": "white-tea",
            "name": "白茶",
            "description": "最少加工的精緻茶品，帶有細膩甜美的風味。抗氧化劑含量最高。",
            "displayOrder": 4,
            "isActive": True,
            "createdAt": datetime.utcnow()
        },
        {
            "_id": "herbal-tea",
            "name": "花草茶",
            "description": "無咖啡因的草本、花卉和水果沖泡飲品。舒緩且芳香。",
            "displayOrder": 5,
            "isActive": True,
            "createdAt": datetime.utcnow()
        },
        {
            "_id": "puerh-tea",
            "name": "普洱茶",
            "description": "來自中國雲南的陳年發酵茶。土壤香氣，口感順滑，越陳越香。",
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

    # Carousel indexes
    await db.carousel.create_index("displayOrder")
    await db.carousel.create_index("active")
    print("✓ Created carousel indexes")

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
            "name": "龍井綠茶",
            "category": "green-tea",
            "description": "來自中國杭州的頂級龍井綠茶。以其翠綠色澤、細膩香氣和甘甜回味聞名。高山茶園手工採摘。沖泡方式：80°C，2-3分鐘。",
            "price": 24.99,
            "imageUrl": "/uploads/products/dragon-well.jpg",
            "thumbnailUrl": "/uploads/products/thumbs/dragon-well.jpg",
            "inStock": True,
            "displayOrder": 1,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        },
        {
            "name": "阿薩姆紅茶",
            "category": "black-tea",
            "description": "來自印度阿薩姆的濃郁麥芽紅茶。醇厚豐富的焦糖香氣。加入牛奶和糖風味絕佳。沖泡方式：100°C，3-5分鐘。",
            "price": 18.99,
            "imageUrl": "/uploads/products/assam-black.jpg",
            "thumbnailUrl": "/uploads/products/thumbs/assam-black.jpg",
            "inStock": True,
            "displayOrder": 1,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        },
        {
            "name": "阿里山烏龍",
            "category": "oolong-tea",
            "description": "來自台灣阿里山地區的高山烏龍茶。花香濃郁，口感綿密，回甘持久。多次回沖展現複雜風味。沖泡方式：90°C，2-3分鐘。",
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

    # === 5. Create Sample Carousel Slides ===

    sample_carousel = [
        {
            "title": "TAIWANTEA",
            "subtitle": "探索台灣精品茶葉的極致風味",
            "imageUrl": "https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=1920&h=1080&fit=crop",
            "ctaLabel": "立即選購",
            "ctaLink": "#products",
            "displayOrder": 0,
            "active": True,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        },
        {
            "title": "頂級烏龍茶",
            "subtitle": "來自台灣高山的純淨茶香",
            "imageUrl": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=1920&h=1080&fit=crop",
            "ctaLabel": "了解更多",
            "ctaLink": "#oolong-tea",
            "displayOrder": 1,
            "active": True,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        },
        {
            "title": "傳統工藝",
            "subtitle": "百年製茶技術，每一片茶葉都是藝術品",
            "imageUrl": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=1920&h=1080&fit=crop",
            "ctaLabel": "探索茶藝",
            "ctaLink": "#products",
            "displayOrder": 2,
            "active": True,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }
    ]

    # Only insert if carousel collection is empty
    carousel_count = await db.carousel.count_documents({})
    if carousel_count == 0:
        await db.carousel.insert_many(sample_carousel)
        print(f"✓ Inserted {len(sample_carousel)} carousel slides")
    else:
        print(f"⚠ Carousel slides already exist ({carousel_count}), skipping samples")

    # === 6. Create Initial Intro Section ===

    intro_section = {
        "htmlContent": """<h2>關於 TAIWANTEA</h2>
<p>我們專注於提供來自台灣及世界各地的頂級茶葉。每一片茶葉都經過精心挑選，確保您品嚐到最純正的茶香。</p>
<p>從清新的綠茶到濃郁的紅茶，從高山烏龍到陳年普洱，我們的茶葉系列涵蓋了各種口味和風格。無論您是茶道愛好者還是初次品茗，都能在這裡找到適合您的茶品。</p>""",
        "buttonText": "瀏覽全系列商品",
        "buttonLink": "https://shopee.tw",
        "active": True,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }

    # Only insert if intro section doesn't exist
    intro_count = await db.intro_section.count_documents({})
    if intro_count == 0:
        await db.intro_section.insert_one(intro_section)
        print("✓ Inserted intro section")
    else:
        print("⚠ Intro section already exists, skipping")

    # === 7. Create Initial Site Settings ===

    site_settings = {
        "logoType": "text",  # "image" or "text"
        "logoImageUrl": None,
        "logoText": None,
        "logoIcon": "🍵",  # Tea cup emoji
        "brandName": "TAIWANTEA",
        "shopeeStoreUrl": "https://shopee.tw/",  # Default Shopee store URL
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }

    # Only insert if site settings don't exist
    settings_count = await db.site_settings.count_documents({})
    if settings_count == 0:
        await db.site_settings.insert_one(site_settings)
        print("✓ Inserted site settings")
    else:
        print("⚠ Site settings already exist, skipping")

    print("\n✅ Database seeding complete!")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed_database())
