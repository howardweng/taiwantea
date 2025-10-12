"""Site Settings Schemas"""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class SiteSettingsBase(BaseModel):
    """Base schema for site settings"""
    logoType: str = Field(..., pattern="^(image|text)$")  # "image" or "text"
    logoImageUrl: Optional[str] = None
    logoText: Optional[str] = None
    logoIcon: Optional[str] = None  # Emoji or text icon
    brandName: str = Field(..., min_length=1, max_length=100)


class SiteSettingsResponse(SiteSettingsBase):
    """Site settings response schema"""
    _id: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class SiteSettingsUpdateRequest(BaseModel):
    """Request schema for updating site settings"""
    logoType: Optional[str] = Field(None, pattern="^(image|text)$")
    logoImageUrl: Optional[str] = None
    logoText: Optional[str] = None
    logoIcon: Optional[str] = None
    brandName: Optional[str] = Field(None, min_length=1, max_length=100)
