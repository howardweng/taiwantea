"""Admin API endpoints for category management"""

from fastapi import APIRouter, HTTPException, Depends

from src.schemas.category import (
    CategoryBase,
    CategoryCreateRequest,
    CategoryUpdateRequest
)
from src.models.category import CategoryModel
from src.middleware.auth import require_admin

router = APIRouter()


@router.post("/categories", response_model=CategoryBase)
async def create_category(
    category_data: CategoryCreateRequest,
    admin: dict = Depends(require_admin)
):
    """
    Create a new category

    Requires admin authentication
    """
    try:
        category_dict = category_data.model_dump()
        # Use the id field as _id for MongoDB
        category_dict["_id"] = category_dict.pop("id")

        category = await CategoryModel.create(category_dict)

        return CategoryBase(**category)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create category: {str(e)}")


@router.put("/categories/{category_id}", response_model=CategoryBase)
async def update_category(
    category_id: str,
    category_data: CategoryUpdateRequest,
    admin: dict = Depends(require_admin)
):
    """
    Update an existing category

    Requires admin authentication
    """
    try:
        # Only update fields that are provided
        update_dict = category_data.model_dump(exclude_unset=True)

        if not update_dict:
            raise HTTPException(status_code=400, detail="No fields to update")

        success = await CategoryModel.update(category_id, update_dict)

        if not success:
            raise HTTPException(status_code=404, detail="Category not found")

        # Fetch the updated category
        category = await CategoryModel.get_by_id(category_id)

        return CategoryBase(**category)

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update category: {str(e)}")


@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: str,
    admin: dict = Depends(require_admin)
):
    """
    Delete (deactivate) a category

    Requires admin authentication
    """
    try:
        success = await CategoryModel.delete(category_id)

        if not success:
            raise HTTPException(status_code=404, detail="Category not found")

        return {"message": "Category deleted successfully", "id": category_id}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete category: {str(e)}")
