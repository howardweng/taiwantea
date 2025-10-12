"""Admin API endpoints for carousel management"""

from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from src.schemas.carousel import (
    CarouselSlide,
    CarouselCreateRequest,
    CarouselUpdateRequest,
    CarouselList
)
from src.models.carousel import CarouselModel
from src.middleware.auth import require_admin

router = APIRouter()


@router.get("/carousel", response_model=CarouselList)
async def get_all_carousel_slides(
    admin: dict = Depends(require_admin)
):
    """
    Get all carousel slides (including inactive)

    Requires admin authentication
    """
    try:
        slides = await CarouselModel.get_all(active_only=False)

        # Convert ObjectId to string for response
        for slide in slides:
            slide["_id"] = str(slide["_id"])

        return CarouselList(slides=slides)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch carousel slides: {str(e)}")


@router.post("/carousel", response_model=CarouselSlide)
async def create_carousel_slide(
    slide_data: CarouselCreateRequest,
    admin: dict = Depends(require_admin)
):
    """
    Create a new carousel slide

    Requires admin authentication
    """
    try:
        # Add admin ID who created the slide
        slide_dict = slide_data.model_dump()
        slide_dict["createdBy"] = str(admin["_id"])

        slide = await CarouselModel.create(slide_dict)
        slide["_id"] = str(slide["_id"])

        return CarouselSlide(**slide)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create carousel slide: {str(e)}")


@router.put("/carousel/{slide_id}", response_model=CarouselSlide)
async def update_carousel_slide(
    slide_id: str,
    slide_data: CarouselUpdateRequest,
    admin: dict = Depends(require_admin)
):
    """
    Update an existing carousel slide

    Requires admin authentication
    """
    try:
        # Validate ObjectId format
        if not ObjectId.is_valid(slide_id):
            raise HTTPException(status_code=400, detail="Invalid slide ID format")

        # Only update fields that are provided
        update_dict = slide_data.model_dump(exclude_unset=True)

        if not update_dict:
            raise HTTPException(status_code=400, detail="No fields to update")

        success = await CarouselModel.update(slide_id, update_dict)

        if not success:
            raise HTTPException(status_code=404, detail="Carousel slide not found")

        # Fetch the updated slide
        slide = await CarouselModel.get_by_id(slide_id)
        slide["_id"] = str(slide["_id"])

        return CarouselSlide(**slide)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update carousel slide: {str(e)}")


@router.delete("/carousel/{slide_id}")
async def delete_carousel_slide(
    slide_id: str,
    admin: dict = Depends(require_admin)
):
    """
    Delete a carousel slide

    Requires admin authentication
    """
    try:
        # Validate ObjectId format
        if not ObjectId.is_valid(slide_id):
            raise HTTPException(status_code=400, detail="Invalid slide ID format")

        success = await CarouselModel.delete(slide_id)

        if not success:
            raise HTTPException(status_code=404, detail="Carousel slide not found")

        return {"message": "Carousel slide deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete carousel slide: {str(e)}")
