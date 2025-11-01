"""
Translate and update missing English names for categories and products
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


# Translation mappings for tea-related terms
TEA_TRANSLATIONS = {
    # Categories
    '工藝窨花茶': 'Scented Tea',
    '茶葉禮盒': 'Tea Gift Box',
    '茶具週邊': 'Tea Accessories',
    '普洱茶': 'Puerh Tea',

    # Common tea terms
    '紅茶': 'Black Tea',
    '綠茶': 'Green Tea',
    '烏龍茶': 'Oolong Tea',
    '白茶': 'White Tea',
    '花茶': 'Flower Tea',
    '普洱': 'Puerh',
    '高山茶': 'High Mountain Tea',
    '包種茶': 'Baozhong Tea',
    '金萱': 'Jin Xuan',
    '凍頂': 'Dongding',
    '東方美人': 'Oriental Beauty',

    # Product descriptions
    '極品': 'Premium',
    '優選': 'Selected',
    '特選': 'Special Selection',
    '精品級': 'Premium Grade',
    '比賽茶': 'Competition Tea',
    '得獎': 'Award-winning',
    '季節限定': 'Seasonal Limited',
    '限量': 'Limited Edition',
    '蜜香': 'Honey Fragrance',
    '桂花': 'Osmanthus',
    '含笑花': 'Michelia',
    '茉莉': 'Jasmine',
    '玫瑰': 'Rose',
    '陳年': 'Aged',
    '自然工法': 'Natural Process',
    '禮盒': 'Gift Box',
    '茶組': 'Tea Set',
    '茶杯': 'Tea Cup',
    '茶碗': 'Tea Bowl',
    '古典': 'Classic',
    '典雅': 'Elegant',
    '青花': 'Blue and White',
    '竹盒': 'Bamboo Box',
    '木盒': 'Wooden Box',
    '竹簡': 'Bamboo Scroll',
    '風雅': 'Refined',
    '心意': 'Heartfelt',
    '品醖': 'Savoring',
    '茶香': 'Tea Fragrance',
    '喜氣': 'Festive',
    '大氣': 'Grand',
    '格局': 'Style',
    '綻藍之美': 'Blooming Blue Beauty',
    '春櫻': 'Spring Cherry Blossom',
    '玉蘭': 'Magnolia',
    '泡茶變簡單': 'Easy Tea Brewing',
}


def translate_tea_name(chinese_name: str) -> str:
    """
    Translate Chinese tea name to English

    Args:
        chinese_name: Chinese name

    Returns:
        English translation
    """
    # Direct match
    if chinese_name in TEA_TRANSLATIONS:
        return TEA_TRANSLATIONS[chinese_name]

    # Try to translate by matching parts
    english_parts = []
    remaining = chinese_name

    # Sort by length (longest first) to match longer phrases first
    sorted_terms = sorted(TEA_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)

    for chinese, english in sorted_terms:
        if chinese in remaining:
            english_parts.append(english)
            remaining = remaining.replace(chinese, '', 1)

    if english_parts:
        return ' '.join(english_parts)

    # If no translation found, return original
    return chinese_name


async def update_missing_english_names():
    """Find and update all categories and products missing English names"""

    mongodb_url = os.getenv("MONGODB_URL")
    if not mongodb_url:
        raise ValueError("MONGODB_URL environment variable is required")

    print("Connecting to MongoDB...")
    client = AsyncIOMotorClient(mongodb_url)
    db = client["taiwantea"]

    try:
        print("\n" + "="*80)
        print("CATEGORIES - Finding items with missing English names")
        print("="*80)

        # Get categories without English names
        categories = await db.categories.find(
            {'$or': [{'englishName': None}, {'englishName': ''}]}
        ).to_list(None)

        print(f"\nFound {len(categories)} categories without English names:\n")

        category_updates = 0
        for category in categories:
            chinese_name = category['name']
            english_name = translate_tea_name(chinese_name)

            print(f"Category: {chinese_name}")
            print(f"  → Translation: {english_name}")

            result = await db.categories.update_one(
                {'_id': category['_id']},
                {'$set': {
                    'englishName': english_name,
                    'updatedAt': datetime.utcnow()
                }}
            )

            if result.modified_count > 0:
                print(f"  ✅ Updated\n")
                category_updates += 1
            else:
                print(f"  ⚠️  No change\n")

        print(f"✅ Updated {category_updates} categories")

        print("\n" + "="*80)
        print("PRODUCTS - Finding items with missing English names")
        print("="*80)

        # Get products without English names
        products = await db.products.find(
            {'$or': [{'englishName': None}, {'englishName': ''}]}
        ).to_list(None)

        print(f"\nFound {len(products)} products without English names:\n")

        product_updates = 0
        for product in products:
            chinese_name = product['name']
            english_name = translate_tea_name(chinese_name)

            print(f"Product: {chinese_name}")
            print(f"  → Translation: {english_name}")

            result = await db.products.update_one(
                {'_id': product['_id']},
                {'$set': {
                    'englishName': english_name,
                    'updatedAt': datetime.utcnow()
                }}
            )

            if result.modified_count > 0:
                print(f"  ✅ Updated\n")
                product_updates += 1
            else:
                print(f"  ⚠️  No change\n")

        print(f"✅ Updated {product_updates} products")

        print("\n" + "="*80)
        print(f"SUMMARY")
        print("="*80)
        print(f"Categories updated: {category_updates}/{len(categories)}")
        print(f"Products updated: {product_updates}/{len(products)}")
        print(f"Total updated: {category_updates + product_updates}")

    except Exception as e:
        print(f"\n❌ Update failed: {e}")
        raise

    finally:
        client.close()


if __name__ == "__main__":
    print("="*80)
    print("Translate Missing English Names")
    print("="*80)
    asyncio.run(update_missing_english_names())
