import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def check():
    client = AsyncIOMotorClient(os.getenv('MONGODB_URL'))
    db = client['taiwantea']

    # Find products where name contains specific text
    products = await db.products.find({'name': {'$regex': '阿里山'}}).to_list(None)

    print(f'Found {len(products)} products with 阿里山:')
    print('='*80)
    for product in products:
        print(f"Name: {product.get('name')}")
        print(f"English Name: {product.get('englishName')}")
        print()

    # Check one more with different name
    products2 = await db.products.find({'name': {'$regex': '龍井'}}).to_list(None)

    print(f'\nFound {len(products2)} products with 龍井:')
    print('='*80)
    for product in products2:
        print(f"Name: {product.get('name')}")
        print(f"English Name: {product.get('englishName')}")
        print()

    client.close()

asyncio.run(check())
