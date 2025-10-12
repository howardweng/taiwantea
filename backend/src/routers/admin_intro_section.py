"""Admin API endpoints for intro section management"""

from fastapi import APIRouter, HTTPException, Depends

from src.schemas.intro_section import IntroSection, IntroSectionUpdateRequest
from src.models.intro_section import IntroSectionModel
from src.middleware.auth import require_admin

router = APIRouter()


@router.get("/intro-section", response_model=IntroSection)
async def get_intro_section_admin(
    admin: dict = Depends(require_admin)
):
    """
    Get intro section content (admin)

    Requires admin authentication
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


@router.put("/intro-section", response_model=IntroSection)
async def update_intro_section(
    section_data: IntroSectionUpdateRequest,
    admin: dict = Depends(require_admin)
):
    """
    Update intro section content

    Requires admin authentication
    """
    try:
        # Only update fields that are provided
        update_dict = section_data.model_dump(exclude_unset=True)

        if not update_dict:
            raise HTTPException(status_code=400, detail="No fields to update")

        await IntroSectionModel.update(update_dict)

        # Fetch the updated section
        section = await IntroSectionModel.get()
        section["_id"] = str(section["_id"])

        return IntroSection(**section)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update intro section: {str(e)}")
