"""Update existing database data to Traditional Chinese"""

import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()


async def translate_database():
    """Translate existing data to Traditional Chinese"""

    mongodb_url = os.getenv("MONGODB_URL")
    if not mongodb_url:
        raise ValueError("MONGODB_URL environment variable is required")
    client = AsyncIOMotorClient(mongodb_url, serverSelectionTimeoutMS=5000)

    # Extract database name from URL
    db_name = mongodb_url.split("/")[-1].split("?")[0]
    db = client[db_name]

    print(f"🔄 Translating database: {db_name}")

    # === 1. Update Categories ===
    category_translations = {
        "green-tea": {
            "name": "綠茶",
            "description": "來自中國和日本的清新、細緻綠茶。富含抗氧化劑，帶有植物、草本香氣。"
        },
        "black-tea": {
            "name": "紅茶",
            "description": "濃郁醇厚的全發酵茶，帶有豐富的麥芽風味。適合早晨或下午品飲。"
        },
        "oolong-tea": {
            "name": "烏龍茶",
            "description": "來自台灣和中國的半發酵茶。複雜風味從花香到焙火香皆有。"
        },
        "white-tea": {
            "name": "白茶",
            "description": "最少加工的精緻茶品，帶有細膩甜美的風味。抗氧化劑含量最高。"
        },
        "herbal-tea": {
            "name": "花草茶",
            "description": "無咖啡因的草本、花卉和水果沖泡飲品。舒緩且芳香。"
        },
        "puerh-tea": {
            "name": "普洱茶",
            "description": "來自中國雲南的陳年發酵茶。土壤香氣，口感順滑，越陳越香。"
        }
    }

    categories_updated = 0
    for category_id, translation in category_translations.items():
        result = await db.categories.update_one(
            {"_id": category_id},
            {"$set": translation}
        )
        if result.modified_count > 0:
            categories_updated += 1

    print(f"✓ Updated {categories_updated} categories")

    # === 2. Update Products ===
    product_translations = {
        "Dragon Well Green Tea": {
            "name": "龍井綠茶",
            "description": "來自中國杭州的頂級龍井綠茶。以其翠綠色澤、細膩香氣和甘甜回味聞名。高山茶園手工採摘。沖泡方式：80°C，2-3分鐘。"
        },
        "Assam Black Tea": {
            "name": "阿薩姆紅茶",
            "description": "來自印度阿薩姆的濃郁麥芽紅茶。醇厚豐富的焦糖香氣。加入牛奶和糖風味絕佳。沖泡方式：100°C，3-5分鐘。"
        },
        "Alishan Oolong": {
            "name": "阿里山烏龍",
            "description": "來自台灣阿里山地區的高山烏龍茶。花香濃郁，口感綿密，回甘持久。多次回沖展現複雜風味。沖泡方式：90°C，2-3分鐘。"
        }
    }

    products_updated = 0
    for english_name, translation in product_translations.items():
        result = await db.products.update_one(
            {"name": english_name},
            {"$set": {
                "name": translation["name"],
                "description": translation["description"],
                "updatedAt": datetime.utcnow()
            }}
        )
        if result.modified_count > 0:
            products_updated += 1

    print(f"✓ Updated {products_updated} products")

    print("\n✅ Database translation complete!")

    client.close()


if __name__ == "__main__":
    asyncio.run(translate_database())
