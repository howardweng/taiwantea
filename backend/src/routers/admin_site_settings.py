"""Admin API endpoints for site settings"""

from fastapi import APIRouter, HTTPException, Depends

from src.schemas.site_settings import SiteSettingsResponse, SiteSettingsUpdateRequest
from src.models.site_settings import SiteSettingsModel
from src.middleware.auth import require_admin

router = APIRouter()


@router.get("/site-settings", response_model=SiteSettingsResponse, dependencies=[Depends(require_admin)])
async def get_site_settings_admin():
    """
    Get site settings (Admin only)
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


@router.put("/site-settings", response_model=SiteSettingsResponse, dependencies=[Depends(require_admin)])
async def update_site_settings(
    settings_data: SiteSettingsUpdateRequest
):
    """
    Update site settings (Admin only)
    """
    try:
        # Prepare update data (only include provided fields)
        update_data = settings_data.model_dump(exclude_unset=True)

        # Validate logoType-specific requirements
        if "logoType" in update_data:
            if update_data["logoType"] == "image" and not update_data.get("logoImageUrl"):
                raise HTTPException(
                    status_code=400,
                    detail="logoImageUrl is required when logoType is 'image'"
                )
            if update_data["logoType"] == "text" and not update_data.get("logoIcon"):
                raise HTTPException(
                    status_code=400,
                    detail="logoIcon is required when logoType is 'text'"
                )

        # Update settings
        success = await SiteSettingsModel.update(update_data)

        if not success:
            raise HTTPException(status_code=500, detail="Failed to update site settings")

        # Fetch and return updated settings
        updated_settings = await SiteSettingsModel.get()
        updated_settings["_id"] = str(updated_settings["_id"])

        return SiteSettingsResponse(**updated_settings)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update site settings: {str(e)}")
