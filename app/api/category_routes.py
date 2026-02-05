from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..schemas.category_schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from ..services.category_service import CategoryService
from ..repositories.category_repository import CategoryRepository

router = APIRouter(prefix="/categories", tags=["Categories"])

def get_category_service(db: Session = Depends(get_db)):
    return CategoryService(CategoryRepository(db))

# Mock auth dependency - replace with actual auth middleware
def get_current_user():
    # This should be replaced with actual JWT auth middleware
    return {"id": 1, "role": "ADMIN"}  # Mock user

def require_admin():
    user = get_current_user()
    if user["role"] != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user

@router.get("/", response_model=dict)
def get_categories(
    service: CategoryService = Depends(get_category_service),
    current_user: dict = Depends(get_current_user)
):
    categories = service.get_all_categories()
    return {
        "success": True,
        "message": "Categories retrieved successfully",
        "data": categories
    }

@router.get("/{category_id}", response_model=dict)
def get_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service),
    current_user: dict = Depends(get_current_user)
):
    category = service.get_category_by_id(category_id)
    return {
        "success": True,
        "message": "Category retrieved successfully",
        "data": category
    }

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
    current_user: dict = Depends(require_admin)
):
    category = service.create_category(category_data)
    return {
        "success": True,
        "message": "Category created successfully",
        "data": category
    }

@router.put("/{category_id}", response_model=dict)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
    current_user: dict = Depends(require_admin)
):
    category = service.update_category(category_id, category_data)
    return {
        "success": True,
        "message": "Category updated successfully",
        "data": category
    }

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service),
    current_user: dict = Depends(require_admin)
):
    service.delete_category(category_id)
    return None