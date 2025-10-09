"""Public API endpoints for products and categories"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId

from src.schemas.product import (
    CategoryList,
    CategoryResponse,
    ProductList,
    ProductResponse
)
from src.services.product_service import ProductService

router = APIRouter()


@router.get("/categories", response_model=CategoryList)
async def get_categories():
    """
    Get all active tea categories

    Public endpoint - no authentication required
    """
    try:
        categories = await ProductService.get_all_categories()

        # Convert ObjectId to string for response
        for cat in categories:
            cat["_id"] = str(cat["_id"])

        return CategoryList(categories=categories)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch categories: {str(e)}")


@router.get("/products", response_model=ProductList)
async def get_products(
    category: Optional[str] = Query(None, description="Filter by category ID"),
    in_stock_only: bool = Query(True, description="Show only in-stock products"),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Limit number of results"),
    skip: int = Query(0, ge=0, description="Skip N results for pagination")
):
    """
    Get all products with optional filters

    Public endpoint - no authentication required
    """
    try:
        products, total = await ProductService.get_all_products(
            category=category,
            in_stock_only=in_stock_only,
            limit=limit,
            skip=skip
        )

        # Convert ObjectId to string for response
        for product in products:
            product["_id"] = str(product["_id"])

        return ProductList(products=products, total=total)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch products: {str(e)}")


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """
    Get single product by ID

    Public endpoint - no authentication required
    """
    try:
        # Validate ObjectId format
        if not ObjectId.is_valid(product_id):
            raise HTTPException(status_code=400, detail="Invalid product ID format")

        product = await ProductService.get_product_by_id(product_id)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Convert ObjectId to string for response
        product["_id"] = str(product["_id"])

        return ProductResponse(**product)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch product: {str(e)}")
