"""Public API endpoints for site settings"""

from fastapi import APIRouter, HTTPException

from src.schemas.site_settings import SiteSettingsResponse
from src.models.site_settings import SiteSettingsModel

router = APIRouter()


@router.get("/site-settings", response_model=SiteSettingsResponse)
async def get_site_settings():
    """
    Get site settings

    Public endpoint - no authentication required
    """
    try:
        settings = await SiteSettingsModel.get()

        if not settings:
            raise HTTPException(status_code=404, detail="Site settings not found")

        # Convert ObjectId to string for response
        settings["_id"] = str(settings["_id"])

        return SiteSettingsResponse(**settings)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch site settings: {str(e)}")
