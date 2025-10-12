"""Public API endpoints for intro section"""

from fastapi import APIRouter, HTTPException

from src.schemas.intro_section import IntroSection
from src.models.intro_section import IntroSectionModel

router = APIRouter()


@router.get("/intro-section", response_model=IntroSection)
async def get_intro_section():
    """
    Get intro section content

    Public endpoint - no authentication required
    """
    try:
        section = await IntroSectionModel.get()

        if not section:
            raise HTTPException(status_code=404, detail="Intro section not found")

        # Convert ObjectId to string for response
        section["_id"] = str(section["_id"])

        return IntroSection(**section)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch intro section: {str(e)}")
