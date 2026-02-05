from ..repositories.product_repository import ProductRepository
from ..schemas.product_schemas import ProductCreate, ProductUpdate, ProductCreateForm, ProductUpdateForm
from ..core.file_utils import save_product_image, delete_product_image
from fastapi import HTTPException
from typing import Optional

class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository
    
    def get_all_products(self):
        products = self.repository.get_all()
        return [self._to_dict(prod) for prod in products]
    
    def get_product_by_id(self, product_id: int):
        product = self.repository.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return self._to_dict(product)
    
    def create_product(self, product_data: ProductCreate):
        if not self.repository.category_exists(product_data.category_id):
            raise HTTPException(status_code=400, detail="Category not found")
        
        product = self.repository.create(product_data)
        return self._to_dict(product)
    
    def create_product_with_image(self, form_data: ProductCreateForm):
        if not self.repository.category_exists(form_data.category_id):
            raise HTTPException(status_code=400, detail="Category not found")
        
        image_url = None
        if form_data.image:
            image_url = save_product_image(form_data.image)
        
        product = self.repository.create_from_form(form_data, image_url)
        return self._to_dict(product)
    
    def update_product(self, product_id: int, product_data: ProductUpdate):
        if product_data.category_id and not self.repository.category_exists(product_data.category_id):
            raise HTTPException(status_code=400, detail="Category not found")
        
        product = self.repository.update(product_id, product_data)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return self._to_dict(product)
    
    def update_product_with_image(self, product_id: int, form_data: ProductUpdateForm):
        existing_product = self.repository.get_by_id(product_id)
        if not existing_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        if form_data.category_id and not self.repository.category_exists(form_data.category_id):
            raise HTTPException(status_code=400, detail="Category not found")
        
        image_url = existing_product.image_url
        if form_data.image:
            # Delete old image if exists
            if existing_product.image_url:
                delete_product_image(existing_product.image_url)
            # Save new image
            image_url = save_product_image(form_data.image)
        
        product = self.repository.update_from_form(product_id, form_data, image_url)
        return self._to_dict(product)
    
    def delete_product(self, product_id: int):
        product = self.repository.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Delete image file if exists
        if product.image_url:
            delete_product_image(product.image_url)
        
        success = self.repository.delete(product_id)
        return success
    
    def _to_dict(self, product):
        return {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "category_id": product.category_id,
            "image_url": product.image_url,
            "created_at": product.created_at,
            "updated_at": product.updated_at
        }