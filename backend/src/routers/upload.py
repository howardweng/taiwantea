"""File upload endpoints"""

import os
import uuid
from typing import List
from io import BytesIO
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import FileResponse
from PIL import Image

from src.middleware.auth import require_admin
from src.config import settings

router = APIRouter()

# Upload directory configuration
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads", "products")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
THUMBNAIL_SIZE = (300, 300)  # Thumbnail dimensions

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_file_extension(filename: str) -> str:
    """Get file extension in lowercase"""
    return os.path.splitext(filename)[1].lower()


def is_allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return get_file_extension(filename) in ALLOWED_EXTENSIONS


def create_thumbnail(image_content: bytes, file_ext: str) -> bytes:
    """
    Create a thumbnail from image content

    Args:
        image_content: Original image bytes
        file_ext: File extension

    Returns:
        Thumbnail image bytes
    """
    # Open image from bytes
    img = Image.open(BytesIO(image_content))

    # Convert RGBA to RGB if necessary (for JPEG)
    if img.mode in ("RGBA", "LA", "P"):
        # Create a white background
        background = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        background.paste(img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None)
        img = background

    # Create thumbnail maintaining aspect ratio
    img.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)

    # Save to bytes
    output = BytesIO()
    format_map = {
        ".jpg": "JPEG",
        ".jpeg": "JPEG",
        ".png": "PNG",
        ".webp": "WEBP",
        ".gif": "GIF"
    }
    img.save(output, format=format_map.get(file_ext, "JPEG"), quality=85, optimize=True)

    return output.getvalue()


@router.post("/upload/image")
async def upload_image(
    file: UploadFile = File(...),
    admin: dict = Depends(require_admin)
):
    """
    Upload a product image and automatically generate thumbnail

    Requires admin authentication

    Returns:
        - imageUrl: Full-size image URL
        - thumbnailUrl: Thumbnail URL (300x300)
    """
    try:
        # Validate file type
        if not is_allowed_file(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # Read file content
        content = await file.read()

        # Validate file size
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024}MB"
            )

        # Generate unique filenames
        file_ext = get_file_extension(file.filename)
        unique_id = str(uuid.uuid4())
        full_filename = f"{unique_id}{file_ext}"
        thumb_filename = f"{unique_id}_thumb{file_ext}"

        full_path = os.path.join(UPLOAD_DIR, full_filename)
        thumb_path = os.path.join(UPLOAD_DIR, thumb_filename)

        # Save full-size image
        with open(full_path, "wb") as f:
            f.write(content)

        # Create and save thumbnail
        try:
            thumbnail_content = create_thumbnail(content, file_ext)
            with open(thumb_path, "wb") as f:
                f.write(thumbnail_content)
        except Exception as e:
            # If thumbnail creation fails, clean up full image and raise error
            if os.path.exists(full_path):
                os.remove(full_path)
            raise HTTPException(status_code=500, detail=f"Failed to create thumbnail: {str(e)}")

        # Return URLs
        image_url = f"{settings.API_URL}/api/uploads/products/{full_filename}"
        thumbnail_url = f"{settings.API_URL}/api/uploads/products/{thumb_filename}"

        return {
            "success": True,
            "imageUrl": image_url,
            "thumbnailUrl": thumbnail_url,
            "filename": full_filename,
            "thumbnailFilename": thumb_filename
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")


@router.get("/uploads/products/{filename}")
async def get_product_image(filename: str):
    """
    Serve a product image
    """
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(file_path)


@router.delete("/upload/image/{filename}")
async def delete_image(
    filename: str,
    admin: dict = Depends(require_admin)
):
    """
    Delete a product image

    Requires admin authentication
    """
    try:
        file_path = os.path.join(UPLOAD_DIR, filename)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Image not found")

        os.remove(file_path)

        return {
            "success": True,
            "message": "Image deleted successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete image: {str(e)}")
