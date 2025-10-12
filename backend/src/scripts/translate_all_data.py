"""Translate ALL existing database data to Traditional Chinese"""

import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()


async def translate_all_database():
    """Translate all existing data to Traditional Chinese"""

    mongodb_url = os.getenv("MONGODB_URL")
    if not mongodb_url:
        raise ValueError("MONGODB_URL environment variable is required")
    client = AsyncIOMotorClient(mongodb_url, serverSelectionTimeoutMS=5000)

    # Extract database name from URL
    db_name = mongodb_url.split("/")[-1].split("?")[0]
    db = client[db_name]

    print(f"🔄 Translating all database data: {db_name}")

    # === Get all products and translate them ===
    products = await db.products.find({}).to_list(length=None)

    # Comprehensive product translations - matching exact database names
    product_translations = {
        # Green Tea (already translated - skip)
        # "龍井綠茶" - already in Chinese
        "Sencha Japanese Green Tea": {
            "name": "日本煎茶",
            "description": "日本最受歡迎的綠茶。清新爽口，帶有植物和海洋風味。富含抗氧化劑。沖泡方式：80°C，1-2分鐘。"
        },
        "Matcha Ceremonial Grade": {
            "name": "典禮級抹茶",
            "description": "石磨研磨的最高等級抹茶粉。充滿活力的綠色，帶有濃郁的鮮味。適合茶道或拿鐵。沖泡方式：80°C，攪拌至起泡。"
        },

        # Black Tea
        # "阿薩姆紅茶" - already in Chinese
        "Earl Grey Black Tea": {
            "name": "伯爵紅茶",
            "description": "經典紅茶注入佛手柑精油。柑橘香氣濃郁，口感順滑。英式下午茶的最愛。沖泡方式：100°C，3-4分鐘。"
        },
        "Ceylon Black Tea": {
            "name": "錫蘭紅茶",
            "description": "來自斯里蘭卡的明亮清爽紅茶。中等醇度，帶有柑橘調性。冷熱皆宜。沖泡方式：100°C，3-5分鐘。"
        },
        "Lapsang Souchong": {
            "name": "正山小種",
            "description": "帶有煙燻松木香氣的紅茶。風味大膽獨特。愛茶人士的冒險選擇。沖泡方式：100°C，3-4分鐘。"
        },

        # Oolong Tea
        # "阿里山烏龍" - already in Chinese
        "Tie Guan Yin": {
            "name": "鐵觀音",
            "description": "來自福建安溪的傳統烏龍茶。蘭花香氣，口感順滑持久。數次沖泡後風味更加豐富。沖泡方式：95°C，2-3分鐘。"
        },
        "Oriental Beauty Oolong": {
            "name": "東方美人",
            "description": "台灣特有的白毫烏龍茶。蜜香果香濃郁，口感甘甜。小綠葉蟬造就獨特風味。沖泡方式：90°C，2-3分鐘。"
        },

        # White Tea
        "Silver Needle White Tea": {
            "name": "白毫銀針",
            "description": "最頂級的白茶，僅採摘嫩芽。細膩甘甜，帶有蜜香。抗氧化劑含量最高。沖泡方式：75°C，3-5分鐘。"
        },
        "White Peony Tea": {
            "name": "白牡丹",
            "description": "採摘嫩芽和葉片的白茶。花香明顯，口感細緻。天然甜味，低咖啡因。沖泡方式：80°C，3-4分鐘。"
        },
        "Moonlight White Tea": {
            "name": "月光白",
            "description": "雲南特產白茶。月光下晾曬而成，帶有獨特的蜜香和花果香。口感甘甜細膩。沖泡方式：85°C，3-4分鐘。"
        },

        # Herbal Tea
        "Chamomile Herbal Tea": {
            "name": "洋甘菊花草茶",
            "description": "舒緩鎮靜的草本茶。蘋果般的甜美香氣。睡前飲用最佳，促進放鬆。沖泡方式：100°C，5-7分鐘。"
        },
        "Peppermint Herbal Tea": {
            "name": "薄荷花草茶",
            "description": "清涼提神的草本茶。助消化，清新口氣。冷熱皆宜。沖泡方式：100°C，5-7分鐘。"
        },
        "Rooibos Red Bush Tea": {
            "name": "南非國寶茶",
            "description": "來自南非的無咖啡因紅茶。天然甜味，帶有堅果和蜂蜜風味。富含抗氧化劑。沖泡方式：100°C，5-7分鐘。"
        },
        "Hibiscus Herbal Tea": {
            "name": "洛神花茶",
            "description": "鮮豔的紅寶石色草本茶。酸甜口感，富含維生素C。冷熱皆宜，助於降血壓。沖泡方式：100°C，5-7分鐘。"
        },

        # Pu-erh Tea
        "Aged Pu-erh Tea": {
            "name": "陳年普洱",
            "description": "十年陳年的雲南普洱茶。土壤香氣，口感醇厚順滑。助消化，越陳越香。沖泡方式：100°C，3-5分鐘。"
        },
        "Raw Pu-erh Sheng": {
            "name": "生普洱",
            "description": "未經發酵的普洱茶餅。清新明亮，帶有花果香氣。隨時間陳化風味更佳。沖泡方式：95°C，2-4分鐘。"
        },
        "Ripe Pu-erh Shou": {
            "name": "熟普洱",
            "description": "經過渥堆發酵的普洱茶。醇厚甘滑，土壤香氣明顯。溫和養胃。沖泡方式：100°C，3-5分鐘。"
        },
        "10 Year Aged Pu-erh": {
            "name": "十年陳普洱",
            "description": "珍藏十年的頂級普洱茶。陳香濃郁，口感圓潤醇厚。收藏級茶品，極具品飲價值。沖泡方式：100°C，3-5分鐘。"
        }
    }

    products_updated = 0
    products_not_found = []

    for product in products:
        current_name = product.get("name", "")
        if current_name in product_translations:
            translation = product_translations[current_name]
            result = await db.products.update_one(
                {"_id": product["_id"]},
                {"$set": {
                    "name": translation["name"],
                    "description": translation["description"],
                    "updatedAt": datetime.utcnow()
                }}
            )
            if result.modified_count > 0:
                products_updated += 1
                print(f"  ✓ {current_name} → {translation['name']}")
        else:
            products_not_found.append(current_name)
            print(f"  ⚠ No translation for: {current_name}")

    print(f"\n✓ Updated {products_updated} products")

    if products_not_found:
        print(f"\n⚠ Products without translations ({len(products_not_found)}):")
        for name in products_not_found:
            print(f"  - {name}")

    print("\n✅ Database translation complete!")

    client.close()


if __name__ == "__main__":
    asyncio.run(translate_all_database())
