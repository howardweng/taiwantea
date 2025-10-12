"""FastAPI application entry point"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import traceback

from src.config import settings
from src.database import connect_to_mongo, close_mongo_connection
from src.routers import auth, products, admin_products, admin_categories, upload, carousel, admin_carousel, intro_section, admin_intro_section
from src.logger import logger
from src.middleware.logging import add_logging_middleware
from src.middleware.rate_limit import add_rate_limiting


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting TAIWANTEA API...")
    await connect_to_mongo()
    logger.info("Application startup complete")
    yield
    # Shutdown
    logger.info("Shutting down application...")
    await close_mongo_connection()
    logger.info("Application shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="TAIWANTEA API",
    description="RESTful API for tea product catalog and admin content management",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request logging middleware
add_logging_middleware(app)

# Add rate limiting for admin endpoints (100 requests per minute)
add_rate_limiting(app, requests_per_minute=100)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions"""
    # Log the error with full traceback
    logger.error(f"Unhandled exception at {request.url.path}")
    logger.error(f"Error: {str(exc)}")
    logger.error(f"Traceback: {traceback.format_exc()}")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal server error occurred",
                "details": str(exc) if settings.ENVIRONMENT == "development" else None
            }
        }
    )


# Health check endpoint
@app.get("/api/health")
async def health_check():
    """API health check"""
    return {
        "success": True,
        "message": "API is healthy",
        "data": {
            "database": "connected",
            "version": "1.0.0"
        }
    }


# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/api", tags=["Products"])
app.include_router(carousel.router, prefix="/api", tags=["Carousel"])
app.include_router(intro_section.router, prefix="/api", tags=["Intro Section"])
app.include_router(admin_products.router, prefix="/api/admin", tags=["Admin - Products"])
app.include_router(admin_categories.router, prefix="/api/admin", tags=["Admin - Categories"])
app.include_router(admin_carousel.router, prefix="/api/admin", tags=["Admin - Carousel"])
app.include_router(admin_intro_section.router, prefix="/api/admin", tags=["Admin - Intro Section"])
app.include_router(upload.router, prefix="/api", tags=["Upload"])


# Root endpoint
@app.get("/")
async def root():
    """API root"""
    return {
        "message": "TAIWANTEA API",
        "version": "1.0.0",
        "docs": "/docs"
    }
