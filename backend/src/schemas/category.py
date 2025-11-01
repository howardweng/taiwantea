"""Pydantic schemas for Category entity"""

from typing import Optional
from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    """Base category schema"""
    id: str = Field(..., alias="_id", description="Category ID (e.g., 'oolong', 'black')")
    name: str = Field(..., min_length=1, description="Category display name (Chinese)")
    englishName: Optional[str] = Field(None, description="Category English name")
    description: str = Field(..., min_length=1, description="Category description")
    displayOrder: int = Field(..., ge=0, description="Display order (0-based)")


class CategoryCreateRequest(BaseModel):
    """Schema for creating a category"""
    id: str = Field(..., min_length=1, max_length=50, description="Category ID (e.g., 'oolong', 'black')")
    name: str = Field(..., min_length=1, max_length=100, description="Category display name (Chinese)")
    englishName: Optional[str] = Field(None, max_length=100, description="Category English name")
    description: str = Field(..., min_length=1, max_length=500, description="Category description")
    displayOrder: int = Field(default=999, ge=0, description="Display order (0-based)")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "green",
                "name": "優選綠茶",
                "englishName": "Green Tea",
                "description": "Fresh and light green teas",
                "displayOrder": 2
            }
        }


class CategoryUpdateRequest(BaseModel):
    """Schema for updating a category"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    englishName: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    displayOrder: Optional[int] = Field(None, ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "優選綠茶",
                "englishName": "Premium Green Tea",
                "displayOrder": 1
            }
        }
