import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def verify():
    client = AsyncIOMotorClient(os.getenv('MONGODB_URL'))
    db = client['taiwantea']

    print("="*80)
    print("VERIFICATION REPORT - English Names Status")
    print("="*80)

    # Check categories
    total_categories = await db.categories.count_documents({})
    categories_with_english = await db.categories.count_documents(
        {'englishName': {'$ne': None, '$ne': ''}}
    )
    categories_without_english = await db.categories.count_documents(
        {'$or': [{'englishName': None}, {'englishName': ''}]}
    )

    print("\n📂 CATEGORIES")
    print(f"  Total: {total_categories}")
    print(f"  With English Name: {categories_with_english} ✅")
    print(f"  Without English Name: {categories_without_english}")

    if categories_without_english > 0:
        missing_cats = await db.categories.find(
            {'$or': [{'englishName': None}, {'englishName': ''}]}
        ).to_list(None)
        print("\n  Missing English names:")
        for cat in missing_cats:
            print(f"    - {cat['name']}")

    # Check products
    total_products = await db.products.count_documents({})
    products_with_english = await db.products.count_documents(
        {'englishName': {'$ne': None, '$ne': ''}}
    )
    products_without_english = await db.products.count_documents(
        {'$or': [{'englishName': None}, {'englishName': ''}]}
    )

    print("\n📦 PRODUCTS")
    print(f"  Total: {total_products}")
    print(f"  With English Name: {products_with_english} ✅")
    print(f"  Without English Name: {products_without_english}")

    if products_without_english > 0:
        missing_prods = await db.products.find(
            {'$or': [{'englishName': None}, {'englishName': ''}]}
        ).to_list(None)
        print("\n  Missing English names:")
        for prod in missing_prods:
            print(f"    - {prod['name']}")

    # Show sample data
    print("\n" + "="*80)
    print("SAMPLE DATA (First 5 of each)")
    print("="*80)

    print("\n📂 Categories:")
    categories = await db.categories.find().sort('displayOrder', 1).limit(5).to_list(None)
    for cat in categories:
        print(f"  {cat['name']}")
        print(f"    → {cat.get('englishName', 'NO ENGLISH NAME')}")

    print("\n📦 Products:")
    products = await db.products.find().limit(5).to_list(None)
    for prod in products:
        print(f"  {prod['name']}")
        print(f"    → {prod.get('englishName', 'NO ENGLISH NAME')}")

    print("\n" + "="*80)
    if categories_without_english == 0 and products_without_english == 0:
        print("✅ SUCCESS! All items have English names")
    else:
        print(f"⚠️  {categories_without_english + products_without_english} items still need English names")
    print("="*80)

    client.close()

asyncio.run(verify())
