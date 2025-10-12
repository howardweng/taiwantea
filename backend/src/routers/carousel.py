"""Public API endpoints for carousel"""

from fastapi import APIRouter, HTTPException

from src.schemas.carousel import CarouselList
from src.models.carousel import CarouselModel

router = APIRouter()


@router.get("/carousel", response_model=CarouselList)
async def get_carousel_slides():
    """
    Get all active carousel slides

    Public endpoint - no authentication required
    """
    try:
        slides = await CarouselModel.get_all(active_only=True)

        # Convert ObjectId to string for response
        for slide in slides:
            slide["_id"] = str(slide["_id"])

        return CarouselList(slides=slides)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch carousel slides: {str(e)}")
