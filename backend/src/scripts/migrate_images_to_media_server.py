"""
Migration script to upload all existing images to media server

This script:
1. Finds all products with relative image URLs (/api/uploads/products/...)
2. Uploads each image to the media server
3. Updates database with new media server URLs
4. Keeps local files as backup

Usage:
    # Dry run (preview changes)
    python src/scripts/migrate_images_to_media_server.py --dry-run

    # Real migration
    python src/scripts/migrate_images_to_media_server.py

Exit codes:
    0: Success
    1: Database connection failed
    2: Migration had errors (partial success)
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from motor.motor_asyncio import AsyncIOMotorClient
from src.config import settings
from src.services.media_service import upload_to_media_server, MediaServerError


# Logging configuration
LOG_DIR = Path(__file__).parent.parent.parent.parent / "taiwantea-server" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / f"image_migration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"


def log(message: str, level: str = "INFO"):
    """Log message to console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}"
    print(log_line)
    with open(LOG_FILE, "a") as f:
        f.write(log_line + "\n")


async def migrate_images(dry_run: bool = False):
    """
    Main migration function

    Args:
        dry_run: If True, preview changes without applying them
    """
    log("=" * 80)
    log(f"Starting image migration to media server (dry_run={dry_run})")
    log(f"Log file: {LOG_FILE}")
    log("=" * 80)

    # Connect to database
    try:
        log("Connecting to MongoDB...")
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.DATABASE_NAME]

        # Test connection
        await client.admin.command('ping')
        log("✓ Connected to MongoDB successfully")

    except Exception as e:
        log(f"✗ Failed to connect to MongoDB: {str(e)}", "ERROR")
        return 1

    try:
        # Get collections
        products_collection = db.products
        carousel_collection = db.carousel_items

        # Count documents to migrate
        products_count = await products_collection.count_documents({
            "imageUrl": {"$regex": "^/api/uploads/products/"}
        })
        carousel_count = await carousel_collection.count_documents({
            "imageUrl": {"$regex": "^/api/uploads/products/"}
        })

        total_count = products_count + carousel_count

        log(f"\nFound {products_count} products and {carousel_count} carousel items to migrate")
        log(f"Total: {total_count} items")

        if total_count == 0:
            log("\n✓ No images to migrate. All images already on media server or no images found.")
            return 0

        if dry_run:
            log("\n⚠️  DRY RUN MODE - No changes will be made")

        # Base directory for uploads
        upload_dir = Path(__file__).parent.parent.parent.parent / "backend" / "uploads" / "products"

        success_count = 0
        error_count = 0
        skipped_count = 0

        # Migrate products
        log("\n" + "=" * 80)
        log("Migrating product images...")
        log("=" * 80)

        async for product in products_collection.find({"imageUrl": {"$regex": "^/api/uploads/products/"}}):
            product_id = product["_id"]
            product_name = product.get("name", "Unknown")
            old_image_url = product["imageUrl"]

            log(f"\n[{success_count + error_count + skipped_count + 1}/{products_count}] Product: {product_name} (ID: {product_id})")
            log(f"  Current URL: {old_image_url}")

            # Extract filename from URL
            filename = old_image_url.split("/")[-1]
            image_path = upload_dir / filename

            # Check if file exists
            if not image_path.exists():
                log(f"  ✗ Image file not found: {image_path}", "ERROR")
                error_count += 1
                continue

            if dry_run:
                log(f"  [DRY RUN] Would upload: {filename}")
                skipped_count += 1
                continue

            # Read image file
            try:
                with open(image_path, "rb") as f:
                    image_content = f.read()

                log(f"  Uploading to media server... ({len(image_content)} bytes)")

                # Upload to media server
                result = await upload_to_media_server(image_content, filename)

                log(f"  ✓ Uploaded successfully")
                log(f"    Full: {result['imageUrl']}")
                log(f"    Thumb: {result['thumbnailUrl']}")
                log(f"    Small: {result['smImageUrl']}")

                # Update database
                update_result = await products_collection.update_one(
                    {"_id": product_id},
                    {"$set": {
                        "imageUrl": result["imageUrl"],
                        "thumbnailUrl": result["thumbnailUrl"],
                        "smImageUrl": result["smImageUrl"]
                    }}
                )

                if update_result.modified_count == 1:
                    log(f"  ✓ Database updated")
                    success_count += 1
                else:
                    log(f"  ✗ Database update failed", "ERROR")
                    error_count += 1

            except MediaServerError as e:
                log(f"  ✗ Media server error: {str(e)}", "ERROR")
                error_count += 1
            except Exception as e:
                log(f"  ✗ Unexpected error: {str(e)}", "ERROR")
                error_count += 1

        # Migrate carousel items
        if carousel_count > 0:
            log("\n" + "=" * 80)
            log("Migrating carousel images...")
            log("=" * 80)

            carousel_success = 0
            carousel_errors = 0

            async for item in carousel_collection.find({"imageUrl": {"$regex": "^/api/uploads/products/"}}):
                item_id = item["_id"]
                old_image_url = item["imageUrl"]

                log(f"\nCarousel item (ID: {item_id})")
                log(f"  Current URL: {old_image_url}")

                # Extract filename from URL
                filename = old_image_url.split("/")[-1]
                image_path = upload_dir / filename

                # Check if file exists
                if not image_path.exists():
                    log(f"  ✗ Image file not found: {image_path}", "ERROR")
                    carousel_errors += 1
                    error_count += 1
                    continue

                if dry_run:
                    log(f"  [DRY RUN] Would upload: {filename}")
                    skipped_count += 1
                    continue

                # Read and upload
                try:
                    with open(image_path, "rb") as f:
                        image_content = f.read()

                    log(f"  Uploading to media server... ({len(image_content)} bytes)")

                    result = await upload_to_media_server(image_content, filename)

                    log(f"  ✓ Uploaded successfully")
                    log(f"    URL: {result['imageUrl']}")

                    # Update database
                    update_result = await carousel_collection.update_one(
                        {"_id": item_id},
                        {"$set": {"imageUrl": result["imageUrl"]}}
                    )

                    if update_result.modified_count == 1:
                        log(f"  ✓ Database updated")
                        carousel_success += 1
                        success_count += 1
                    else:
                        log(f"  ✗ Database update failed", "ERROR")
                        carousel_errors += 1
                        error_count += 1

                except MediaServerError as e:
                    log(f"  ✗ Media server error: {str(e)}", "ERROR")
                    carousel_errors += 1
                    error_count += 1
                except Exception as e:
                    log(f"  ✗ Unexpected error: {str(e)}", "ERROR")
                    carousel_errors += 1
                    error_count += 1

        # Summary
        log("\n" + "=" * 80)
        log("Migration Summary")
        log("=" * 80)
        log(f"Total items: {total_count}")
        log(f"✓ Successful: {success_count}")
        log(f"✗ Errors: {error_count}")

        if dry_run:
            log(f"⚠️  Skipped (dry run): {skipped_count}")
            log("\nTo perform actual migration, run without --dry-run flag")
            return 0
        else:
            log(f"\n✓ Migration complete!")
            log(f"Log file: {LOG_FILE}")

            if error_count > 0:
                log(f"\n⚠️  {error_count} errors occurred. Check log for details.", "WARNING")
                return 2

            return 0

    except Exception as e:
        log(f"\n✗ Fatal error during migration: {str(e)}", "ERROR")
        import traceback
        log(traceback.format_exc(), "ERROR")
        return 2

    finally:
        # Close database connection
        client.close()
        log("\nDatabase connection closed")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Migrate images from local storage to media server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview changes without applying
  python src/scripts/migrate_images_to_media_server.py --dry-run

  # Perform actual migration
  python src/scripts/migrate_images_to_media_server.py

IMPORTANT:
  - Backup your database before running this script!
  - Run in dry-run mode first to preview changes
  - Check the log file after completion
        """
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without applying them"
    )

    args = parser.parse_args()

    # Run migration
    exit_code = asyncio.run(migrate_images(dry_run=args.dry_run))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
