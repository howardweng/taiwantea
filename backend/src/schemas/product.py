"""Pydantic schemas for Product and Category entities"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


# ============================================
# Category Schemas
# ============================================

class CategoryResponse(BaseModel):
    """Category response schema"""
    id: str = Field(..., alias="_id")
    name: str
    description: Optional[str] = None
    displayOrder: int
    imageUrl: Optional[str] = None
    isActive: bool = True

    class Config:
        populate_by_name = True


class CategoryList(BaseModel):
    """List of categories"""
    categories: List[CategoryResponse]


# ============================================
# Product Schemas
# ============================================

class ProductResponse(BaseModel):
    """Public product response (customer-facing)"""
    id: str = Field(..., alias="_id")
    name: str
    category: str
    description: str
    price: float
    imageUrl: str
    thumbnailUrl: Optional[str] = None
    inStock: bool

    class Config:
        populate_by_name = True


class ProductAdmin(ProductResponse):
    """Admin product response (includes metadata)"""
    displayOrder: int
    createdAt: datetime
    updatedAt: datetime
    createdBy: Optional[str] = None

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class ProductList(BaseModel):
    """List of products"""
    products: List[ProductResponse]
    total: int


class ProductCreateRequest(BaseModel):
    """Create product request"""
    name: str = Field(..., min_length=1, max_length=200)
    category: str = Field(..., min_length=1)
    description: str = Field(..., min_length=10, max_length=5000)
    price: float = Field(..., ge=0)
    imageUrl: str
    thumbnailUrl: Optional[str] = None
    inStock: bool = True
    displayOrder: int = Field(default=999, ge=0)


class ProductUpdateRequest(BaseModel):
    """Update product request"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    category: Optional[str] = None
    description: Optional[str] = Field(None, min_length=10, max_length=5000)
    price: Optional[float] = Field(None, ge=0)
    imageUrl: Optional[str] = None
    thumbnailUrl: Optional[str] = None
    inStock: Optional[bool] = None
    displayOrder: Optional[int] = Field(None, ge=0)
