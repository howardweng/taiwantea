"""
Migration Script: Split category names into Chinese and English fields

This script:
1. Reads existing category names from the database
2. Splits combined "中文English" names into separate fields
3. Updates each category with:
   - name: Chinese part only
   - englishName: English part (new field)
"""

import asyncio
import re
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


def split_category_name(combined_name: str) -> dict:
    """
    Split category name into Chinese and English parts

    Args:
        combined_name: Combined name like "優選綠茶Green Tea"

    Returns:
        dict with 'chinese' and 'english' keys
    """
    # Match pattern: Chinese characters followed by English text
    match = re.match(r'^([^a-zA-Z]+)(.*)$', combined_name)

    if match:
        chinese = match.group(1).strip()
        english = match.group(2).strip()
        return {
            'chinese': chinese,
            'english': english if english else None
        }

    # If no English part found, return Chinese only
    return {
        'chinese': combined_name.strip(),
        'english': None
    }


async def migrate_categories():
    """Migrate existing categories to add englishName field"""

    mongodb_url = os.getenv("MONGODB_URL")
    if not mongodb_url:
        raise ValueError("MONGODB_URL environment variable is required")

    print("Connecting to MongoDB...")
    client = AsyncIOMotorClient(mongodb_url)
    db = client["taiwantea"]
    categories_collection = db["categories"]

    try:
        # Get all categories
        categories = await categories_collection.find().to_list(None)
        print(f"\nFound {len(categories)} categories to migrate\n")

        updated_count = 0

        for category in categories:
            category_id = category['_id']
            current_name = category['name']

            # Split the name
            split_result = split_category_name(current_name)
            chinese_name = split_result['chinese']
            english_name = split_result['english']

            print(f"Category ID: {category_id}")
            print(f"  Current: {current_name}")
            print(f"  Chinese: {chinese_name}")
            print(f"  English: {english_name or '(none)'}")

            # Update the category
            update_data = {
                'name': chinese_name,
                'englishName': english_name,
                'updatedAt': datetime.utcnow()
            }

            result = await categories_collection.update_one(
                {'_id': category_id},
                {'$set': update_data}
            )

            if result.modified_count > 0:
                updated_count += 1
                print(f"  ✅ Updated\n")
            else:
                print(f"  ⚠️  No changes needed\n")

        print(f"\n✅ Migration complete! Updated {updated_count} categories")

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        raise

    finally:
        client.close()


if __name__ == "__main__":
    print("=" * 60)
    print("Category English Name Migration")
    print("=" * 60)
    asyncio.run(migrate_categories())
