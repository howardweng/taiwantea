"""Pydantic schemas for Intro Section entity"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class IntroSection(BaseModel):
    """Intro section response schema"""
    id: str = Field(..., alias="_id")
    htmlContent: str  # Rich HTML content
    buttonText: str
    buttonLink: str
    active: bool = True
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        populate_by_name = True


class IntroSectionUpdateRequest(BaseModel):
    """Request schema for updating intro section"""
    htmlContent: Optional[str] = Field(None, min_length=1)
    buttonText: Optional[str] = Field(None, min_length=1, max_length=100)
    buttonLink: Optional[str] = Field(None, min_length=1, max_length=500)
    active: Optional[bool] = None
