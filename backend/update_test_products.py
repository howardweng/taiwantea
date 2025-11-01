import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

async def update_test_products():
    client = AsyncIOMotorClient(os.getenv('MONGODB_URL'))
    db = client['taiwantea']

    # Update specific products with English names for testing
    updates = [
        {'name': '龍井綠茶(珍品量少)', 'englishName': 'Taiwan Longjing Green Tea'},
        {'name': '阿里山高山茶', 'englishName': 'Alisan High Mountain Tea'},
        {'name': '台灣碧螺春-頂極綠茶', 'englishName': 'Bilochun Green Tea'},
        {'name': '優選包種茶', 'englishName': 'Wenshan Baozhong Tea'},
        {'name': '早春清香烏龍茶', 'englishName': 'Spring Light Oolong'},
        {'name': '焙香凍頂烏龍茶', 'englishName': 'Dongding Oolong Tea'},
        {'name': '高山金萱烏龍茶', 'englishName': 'Jin Xuan Tea'},
        {'name': '大禹嶺高山茶', 'englishName': 'Dayuling High Mountain Tea'},
        {'name': '極品梨山高山茶', 'englishName': 'Lishan High Mountain Tea'},
        {'name': '杉林溪高山茶', 'englishName': 'Shanlinxi High Mountain Tea'},
        {'name': '東方美人茶', 'englishName': 'Oriental Beauty Tea'},
        {'name': '日月潭紅茶-紅玉', 'englishName': 'Sun Moon Lake Black Tea'},
    ]

    print('Updating products with English names...')
    print('='*80)

    updated_count = 0
    for update in updates:
        result = await db.products.update_one(
            {'name': update['name']},
            {'$set': {
                'englishName': update['englishName'],
                'updatedAt': datetime.utcnow()
            }}
        )

        if result.modified_count > 0:
            print(f"✅ {update['name']} → {update['englishName']}")
            updated_count += 1
        elif result.matched_count > 0:
            print(f"⚠️  {update['name']} (already had this English name)")
        else:
            print(f"❌ {update['name']} (not found)")

    print(f"\n✅ Updated {updated_count} products")

    client.close()

asyncio.run(update_test_products())
