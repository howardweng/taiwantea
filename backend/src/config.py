"""Application configuration using Pydantic Settings"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database (Remote MongoDB - required)
    MONGODB_URL: str  # No default - must be provided via environment variable
    DATABASE_NAME: str = "taiwantea"

    # Security
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # API
    API_URL: str = "http://localhost:8585"

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    # File Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 5242880  # 5MB
    ALLOWED_IMAGE_TYPES: str = "image/jpeg,image/png,image/webp"

    # Media Server
    MEDIA_SERVER_URL: str = "https://mediaserver.frrut.com"
    MEDIA_SERVER_UPLOAD_ENDPOINT: str = "/uploadPic/taiwantea"

    @property
    def cors_origins(self) -> List[str]:
        """Parse ALLOWED_ORIGINS into a list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    @property
    def image_types(self) -> List[str]:
        """Parse ALLOWED_IMAGE_TYPES into a list"""
        return [t.strip() for t in self.ALLOWED_IMAGE_TYPES.split(",")]

    # Environment
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()
