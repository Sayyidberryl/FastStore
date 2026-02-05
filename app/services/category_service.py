from ..repositories.category_repository import CategoryRepository
from ..schemas.category_schemas import CategoryCreate, CategoryUpdate
from fastapi import HTTPException

class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository
    
    def get_all_categories(self):
        categories = self.repository.get_all()
        return [self._to_dict(cat) for cat in categories]
    
    def get_category_by_id(self, category_id: int):
        category = self.repository.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return self._to_dict(category)
    
    def create_category(self, category_data: CategoryCreate):
        category = self.repository.create(category_data)
        return self._to_dict(category)
    
    def update_category(self, category_id: int, category_data: CategoryUpdate):
        category = self.repository.update(category_id, category_data)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return self._to_dict(category)
    
    def delete_category(self, category_id: int):
        if self.repository.has_products(category_id):
            raise HTTPException(
                status_code=400, 
                detail="Cannot delete category that has products"
            )
        
        success = self.repository.delete(category_id)
        if not success:
            raise HTTPException(status_code=404, detail="Category not found")
        return success
    
    def _to_dict(self, category):
        return {
            "id": category.id,
            "name": category.name,
            "created_at": category.created_at,
            "updated_at": category.updated_at
        }