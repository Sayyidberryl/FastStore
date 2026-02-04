from ..repositories.product_repository import ProductRepository
from ..schemas.product_schemas import ProductCreate, ProductUpdate
from fastapi import HTTPException

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
    
    def update_product(self, product_id: int, product_data: ProductUpdate):
        if product_data.category_id and not self.repository.category_exists(product_data.category_id):
            raise HTTPException(status_code=400, detail="Category not found")
        
        product = self.repository.update(product_id, product_data)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return self._to_dict(product)
    
    def delete_product(self, product_id: int):
        success = self.repository.delete(product_id)
        if not success:
            raise HTTPException(status_code=404, detail="Product not found")
        return success
    
    def _to_dict(self, product):
        return {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "category_id": product.category_id,
            "created_at": product.created_at,
            "updated_at": product.updated_at
        }