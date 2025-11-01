"""File upload endpoints"""

import os
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import FileResponse

from src.middleware.auth import require_admin
from src.config import settings
from src.services.media_service import upload_to_media_server, MediaServerError

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


@router.post("/upload/image")
async def upload_image(
    file: UploadFile = File(...),
    admin: dict = Depends(require_admin)
):
    """
    Upload a product image to media server

    Requires admin authentication

    Returns:
        - imageUrl: Full-size image URL from media server
        - thumbnailUrl: Thumbnail URL from media server
        - smImageUrl: Small image URL from media server
        - filename: Filename on media server
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

        # Upload to media server
        try:
            result = await upload_to_media_server(content, file.filename)

            return {
                "success": True,
                "imageUrl": result["imageUrl"],
                "thumbnailUrl": result["thumbnailUrl"],
                "smImageUrl": result["smImageUrl"],
                "filename": result["filename"]
            }

        except MediaServerError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Media server error: {str(e)}"
            )

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


# Note: Image deletion removed - images on media server are never deleted
# When a product is deleted, the image URL is simply removed from database
# Images remain on media server for potential reuse or archival purposes
