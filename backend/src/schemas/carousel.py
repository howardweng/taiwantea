"""Pydantic schemas for Carousel entity"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime


# ============================================
# Carousel Schemas
# ============================================

class CarouselSlide(BaseModel):
    """Carousel slide response schema"""
    id: str = Field(..., alias="_id")
    title: str
    subtitle: Optional[str] = None
    imageUrl: str
    ctaLabel: Optional[str] = None  # Call-to-action button label
    ctaLink: Optional[str] = None   # Link or scroll target (e.g., "#products", "/category/tea")
    displayOrder: int = 0
    active: bool = True
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    createdBy: Optional[str] = None

    class Config:
        populate_by_name = True


class CarouselCreateRequest(BaseModel):
    """Request schema for creating a carousel slide"""
    title: str = Field(..., min_length=1, max_length=200)
    subtitle: Optional[str] = Field(None, max_length=500)
    imageUrl: str = Field(..., min_length=1)
    displayOrder: int = Field(0, ge=0)
    active: bool = True


class CarouselUpdateRequest(BaseModel):
    """Request schema for updating a carousel slide"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    subtitle: Optional[str] = Field(None, max_length=500)
    imageUrl: Optional[str] = Field(None, min_length=1)
    displayOrder: Optional[int] = Field(None, ge=0)
    active: Optional[bool] = None


class CarouselList(BaseModel):
    """List of carousel slides"""
    slides: List[CarouselSlide]
