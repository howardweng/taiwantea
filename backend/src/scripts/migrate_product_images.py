"""
Migration Script: Convert product single image to images array

This script:
1. Reads existing products from the database
2. Converts imageUrl and thumbnailUrl into images array format
3. Updates each product with:
   - images: Array with first image from imageUrl/thumbnailUrl
   - detailContent: Empty string (for WYSIWYG editor)

This migration is safe to run multiple times - it only updates products
that don't have the images field yet.
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


async def migrate_products():
    """Migrate existing products to add images array and detailContent field"""

    mongodb_url = os.getenv("MONGODB_URL")
    if not mongodb_url:
        raise ValueError("MONGODB_URL environment variable is required")

    print("Connecting to MongoDB...")
    client = AsyncIOMotorClient(mongodb_url)
    db = client["taiwantea"]
    products_collection = db["products"]

    try:
        # Get all products
        products = await products_collection.find().to_list(None)
        print(f"\nFound {len(products)} products to check\n")

        updated_count = 0
        skipped_count = 0

        for product in products:
            product_id = product['_id']
            product_name = product.get('name', 'Unknown')

            # Check if product already has images array
            if 'images' in product and product['images']:
                print(f"Product: {product_name}")
                print(f"  ⏭️  Already has images array - skipping\n")
                skipped_count += 1
                continue

            # Get current image URLs
            image_url = product.get('imageUrl', '')
            thumbnail_url = product.get('thumbnailUrl', '')

            print(f"Product: {product_name}")
            print(f"  Image URL: {image_url}")
            print(f"  Thumbnail URL: {thumbnail_url}")

            # Create images array with first image
            images = []
            if image_url:
                images.append({
                    'url': image_url,
                    'thumbnailUrl': thumbnail_url if thumbnail_url else None,
                    'displayOrder': 0,
                    'alt': f"{product_name} 商品圖"
                })

            # Update the product
            update_data = {
                'images': images,
                'detailContent': '',
                'updatedAt': datetime.utcnow()
            }

            print(f"  Creating images array with {len(images)} image(s)")

            result = await products_collection.update_one(
                {'_id': product_id},
                {'$set': update_data}
            )

            if result.modified_count > 0:
                updated_count += 1
                print(f"  ✅ Updated\n")
            else:
                print(f"  ⚠️  No changes made\n")

        print(f"\n{'=' * 60}")
        print(f"✅ Migration complete!")
        print(f"   Updated: {updated_count} products")
        print(f"   Skipped: {skipped_count} products (already migrated)")
        print(f"   Total: {len(products)} products")
        print(f"{'=' * 60}")

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        raise

    finally:
        client.close()


if __name__ == "__main__":
    print("=" * 60)
    print("Product Images Migration")
    print("Convert single image to images array format")
    print("=" * 60)
    asyncio.run(migrate_products())
