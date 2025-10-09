"""Pydantic schemas for Admin entity"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class AdminLogin(BaseModel):
    """Admin login request"""
    email: EmailStr
    password: str = Field(..., min_length=8)


class AdminCreate(BaseModel):
    """Admin creation schema"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=1, max_length=100)


class AdminProfile(BaseModel):
    """Admin profile response"""
    id: str = Field(..., alias="_id")
    email: EmailStr
    name: str
    lastLoginAt: Optional[datetime] = None

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class AdminUpdate(BaseModel):
    """Admin update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    password: Optional[str] = Field(None, min_length=8)
