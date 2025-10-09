"""JWT authentication middleware"""

from fastapi import HTTPException, status, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from src.services.auth_service import AuthService

security = HTTPBearer(auto_error=False)


async def get_token_from_cookie(request: Request) -> Optional[str]:
    """Extract JWT token from httpOnly cookie"""
    token = request.cookies.get("accessToken")
    return token


async def require_admin(request: Request) -> dict:
    """Dependency to require authenticated admin"""

    # Try to get token from cookie
    token = await get_token_from_cookie(request)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "error": {
                    "code": "UNAUTHORIZED",
                    "message": "Not authenticated"
                }
            }
        )

    # Verify token and get admin
    admin = await AuthService.get_current_admin(token)

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "error": {
                    "code": "UNAUTHORIZED",
                    "message": "Invalid or expired token"
                }
            }
        )

    return admin


async def get_current_admin_optional(request: Request) -> Optional[dict]:
    """Get current admin if authenticated, None otherwise"""
    token = await get_token_from_cookie(request)

    if not token:
        return None

    admin = await AuthService.get_current_admin(token)
    return admin
