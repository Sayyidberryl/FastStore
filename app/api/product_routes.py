from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..schemas.product_schemas import ProductCreate, ProductUpdate, ProductResponse, ProductCreateForm, ProductUpdateForm
from ..services.product_service import ProductService
from ..repositories.product_repository import ProductRepository

router = APIRouter(prefix="/products", tags=["Products"])

def get_product_service(db: Session = Depends(get_db)):
    return ProductService(ProductRepository(db))

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
def get_products(
    service: ProductService = Depends(get_product_service),
    current_user: dict = Depends(get_current_user)
):
    products = service.get_all_products()
    return {
        "success": True,
        "message": "Products retrieved successfully",
        "data": products
    }

@router.get("/{product_id}", response_model=dict)
def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
    current_user: dict = Depends(get_current_user)
):
    product = service.get_product_by_id(product_id)
    return {
        "success": True,
        "message": "Product retrieved successfully",
        "data": product
    }

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_product(
    form_data: ProductCreateForm = Depends(),
    service: ProductService = Depends(get_product_service),
    current_user: dict = Depends(require_admin)
):
    product = service.create_product_with_image(form_data)
    return {
        "success": True,
        "message": "Product created successfully",
        "data": product
    }

@router.put("/{product_id}", response_model=dict)
def update_product(
    product_id: int,
    form_data: ProductUpdateForm = Depends(),
    service: ProductService = Depends(get_product_service),
    current_user: dict = Depends(require_admin)
):
    product = service.update_product_with_image(product_id, form_data)
    return {
        "success": True,
        "message": "Product updated successfully",
        "data": product
    }

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
    current_user: dict = Depends(require_admin)
):
    service.delete_product(product_id)
    return None