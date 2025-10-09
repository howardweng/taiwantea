"""Authentication router - login, logout, current user"""

from fastapi import APIRouter, HTTPException, status, Response, Depends
from datetime import timedelta

from src.schemas.admin import AdminLogin, AdminProfile
from src.services.auth_service import AuthService
from src.middleware.auth import require_admin, get_current_admin_optional
from src.config import settings

router = APIRouter()


@router.post("/login")
async def login(credentials: AdminLogin, response: Response):
    """Admin login - returns JWT token in httpOnly cookie"""

    # Authenticate admin
    admin = await AuthService.authenticate_admin(credentials.email, credentials.password)

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "error": {
                    "code": "UNAUTHORIZED",
                    "message": "Invalid email or password"
                }
            }
        )

    # Create access token
    access_token = AuthService.create_access_token(
        data={"sub": str(admin["_id"])},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Set httpOnly cookie
    response.set_cookie(
        key="accessToken",
        value=access_token,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",  # Only HTTPS in production
        samesite="strict",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    # Return admin profile
    return {
        "success": True,
        "data": {
            "admin": AdminProfile(
                _id=str(admin["_id"]),
                email=admin["email"],
                name=admin["name"],
                lastLoginAt=admin.get("lastLoginAt")
            )
        },
        "message": "Login successful"
    }


@router.post("/logout")
async def logout(response: Response, admin: dict = Depends(require_admin)):
    """Admin logout - clears JWT cookie"""

    # Clear cookie
    response.delete_cookie(key="accessToken")

    return {
        "success": True,
        "message": "Logout successful"
    }


@router.get("/me")
async def get_current_user(admin: dict = Depends(require_admin)):
    """Get current authenticated admin profile"""

    return {
        "success": True,
        "data": AdminProfile(
            _id=str(admin["_id"]),
            email=admin["email"],
            name=admin["name"],
            lastLoginAt=admin.get("lastLoginAt")
        ),
        "message": "Profile retrieved successfully"
    }
