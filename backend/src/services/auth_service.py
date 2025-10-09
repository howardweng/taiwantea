"""Authentication service with bcrypt and JWT"""

from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from jose import JWTError, jwt

from src.config import settings
from src.models.admin import AdminModel


class AuthService:
    """Authentication service"""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            return payload
        except JWTError:
            return None

    @staticmethod
    async def authenticate_admin(email: str, password: str) -> Optional[dict]:
        """Authenticate admin user"""
        admin = await AdminModel.find_by_email(email)

        if not admin:
            return None

        if not AuthService.verify_password(password, admin["passwordHash"]):
            return None

        # Update last login
        await AdminModel.update_last_login(str(admin["_id"]))

        return admin

    @staticmethod
    async def get_current_admin(token: str) -> Optional[dict]:
        """Get current admin from token"""
        payload = AuthService.verify_token(token)

        if not payload:
            return None

        admin_id = payload.get("sub")
        if not admin_id:
            return None

        admin = await AdminModel.find_by_id(admin_id)
        return admin
