"""
Refine English names with better translations
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


# Better, more natural English translations
REFINED_TRANSLATIONS = {
    # Products that need refinement
    '極品蜜香紅茶': 'Premium Honey Fragrance Black Tea',
    '桂花紅茶-蜜甜香': 'Osmanthus Black Tea - Sweet Honey',
    '陳年普洱': 'Aged Puerh Tea',
    '比賽茶-得奬綠茶': 'Award-Winning Competition Green Tea',
    '阿里山紅茶-紅烏龍': 'Alishan Red Oolong Tea',
    '含笑花紅茶-季節限定': 'Michelia Black Tea - Seasonal Limited',
    '精品級-台灣白茶禮盒(限量)': 'Premium Taiwan White Tea Gift Box (Limited)',
    '特選-自然工法白茶': 'Natural Process White Tea - Special Selection',
    '苿莉綠茶-芬芳美麗': 'Jasmine Green Tea - Fragrant Beauty',
    '八月桂花包種茶': 'August Osmanthus Baozhong Tea',
    '含笑花紅茶': 'Michelia Black Tea',
    '生普洱': 'Raw Puerh Tea',
    '熟普洱': 'Ripe Puerh Tea',
    '十年陳普洱': '10-Year Aged Puerh Tea',
    '桂花紅茶-八月秋香': 'Osmanthus Black Tea - August Autumn Fragrance',
    '高級木質盒-日式風格茶禮': 'Premium Wooden Box - Japanese Style Tea Gift',
    '慕茶竹盒-可當茶盤使用': 'Bamboo Tea Box - Double as Tea Tray',
    '喜氣木盒茶禮-大氣': 'Festive Wooden Box Tea Gift - Grand Style',
    'Living Stone 茶禮': 'Living Stone Tea Gift',
    '心意茶禮-竹簡風雅': 'Heartfelt Tea Gift - Bamboo Scroll Elegance',
    '品醖茶香禮盒': 'Savoring Tea Fragrance Gift Box',
    '古典青花茶碗': 'Classic Blue and White Tea Bowl',
    '綻藍之美茶組(一壼二杯)': 'Blooming Blue Beauty Tea Set (1 Pot 2 Cups)',
    '玫瑰故事茶禮': 'Rose Story Tea Gift',
    '春櫻典雅茶杯-泡茶變簡單': 'Spring Cherry Blossom Elegant Tea Cup - Easy Brewing',
    '玉蘭典雅茶杯-泡茶變簡單': 'Magnolia Elegant Tea Cup - Easy Brewing',
}


async def refine_english_names():
    """Refine English translations with better names"""

    mongodb_url = os.getenv("MONGODB_URL")
    if not mongodb_url:
        raise ValueError("MONGODB_URL environment variable is required")

    print("Connecting to MongoDB...")
    client = AsyncIOMotorClient(mongodb_url)
    db = client["taiwantea"]

    try:
        print("\n" + "="*80)
        print("REFINING ENGLISH NAMES")
        print("="*80)

        updated_count = 0

        for chinese_name, english_name in REFINED_TRANSLATIONS.items():
            print(f"\n{chinese_name}")
            print(f"  → {english_name}")

            # Try products first
            result = await db.products.update_one(
                {'name': chinese_name},
                {'$set': {
                    'englishName': english_name,
                    'updatedAt': datetime.utcnow()
                }}
            )

            if result.modified_count > 0:
                print(f"  ✅ Updated product")
                updated_count += 1
                continue

            # Try categories
            result = await db.categories.update_one(
                {'name': chinese_name},
                {'$set': {
                    'englishName': english_name,
                    'updatedAt': datetime.utcnow()
                }}
            )

            if result.modified_count > 0:
                print(f"  ✅ Updated category")
                updated_count += 1
            else:
                print(f"  ⚠️  Not found or already has this name")

        print("\n" + "="*80)
        print(f"SUMMARY: Refined {updated_count} English names")
        print("="*80)

    except Exception as e:
        print(f"\n❌ Refinement failed: {e}")
        raise

    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(refine_english_names())
