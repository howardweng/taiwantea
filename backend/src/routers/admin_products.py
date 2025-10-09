"""Admin API endpoints for product management"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from src.schemas.product import (
    ProductAdmin,
    ProductCreateRequest,
    ProductUpdateRequest,
    ProductList
)
from src.services.product_service import ProductService
from src.middleware.auth import require_admin

router = APIRouter()


@router.post("/products", response_model=ProductAdmin)
async def create_product(
    product_data: ProductCreateRequest,
    admin: dict = Depends(require_admin)
):
    """
    Create a new product

    Requires admin authentication
    """
    try:
        # Add admin ID who created the product
        product_dict = product_data.model_dump()
        product_dict["createdBy"] = str(admin["_id"])

        product_id = await ProductService.create_product(product_dict)

        # Fetch the created product
        product = await ProductService.get_product_by_id(product_id)
        product["_id"] = str(product["_id"])

        return ProductAdmin(**product)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create product: {str(e)}")


@router.put("/products/{product_id}", response_model=ProductAdmin)
async def update_product(
    product_id: str,
    product_data: ProductUpdateRequest,
    admin: dict = Depends(require_admin)
):
    """
    Update an existing product

    Requires admin authentication
    """
    try:
        # Validate ObjectId format
        if not ObjectId.is_valid(product_id):
            raise HTTPException(status_code=400, detail="Invalid product ID format")

        # Only update fields that are provided
        update_dict = product_data.model_dump(exclude_unset=True)

        if not update_dict:
            raise HTTPException(status_code=400, detail="No fields to update")

        success = await ProductService.update_product(product_id, update_dict)

        if not success:
            raise HTTPException(status_code=404, detail="Product not found")

        # Fetch the updated product
        product = await ProductService.get_product_by_id(product_id)
        product["_id"] = str(product["_id"])

        return ProductAdmin(**product)

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update product: {str(e)}")


@router.delete("/products/{product_id}")
async def delete_product(
    product_id: str,
    admin: dict = Depends(require_admin)
):
    """
    Delete a product

    Requires admin authentication
    """
    try:
        # Validate ObjectId format
        if not ObjectId.is_valid(product_id):
            raise HTTPException(status_code=400, detail="Invalid product ID format")

        success = await ProductService.delete_product(product_id)

        if not success:
            raise HTTPException(status_code=404, detail="Product not found")

        return {"message": "Product deleted successfully", "id": product_id}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete product: {str(e)}")


@router.get("/products", response_model=ProductList)
async def get_all_products_admin(
    category: Optional[str] = None,
    admin: dict = Depends(require_admin)
):
    """
    Get all products (admin view - includes out of stock)

    Requires admin authentication
    """
    try:
        products, total = await ProductService.get_all_products(
            category=category,
            in_stock_only=False  # Admin can see all products
        )

        # Convert ObjectId to string for response
        for product in products:
            product["_id"] = str(product["_id"])

        return ProductList(products=products, total=total)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch products: {str(e)}")
