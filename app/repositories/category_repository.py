from sqlalchemy.orm import Session
from ..models.category import Category
from ..schemas.category_schemas import CategoryCreate, CategoryUpdate

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self):
        return self.db.query(Category).all()
    
    def get_by_id(self, category_id: int):
        return self.db.query(Category).filter(Category.id == category_id).first()
    
    def create(self, category_data: CategoryCreate):
        category = Category(**category_data.model_dump())
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def update(self, category_id: int, category_data: CategoryUpdate):
        category = self.get_by_id(category_id)
        if category:
            for key, value in category_data.model_dump(exclude_unset=True).items():
                setattr(category, key, value)
            self.db.commit()
            self.db.refresh(category)
        return category
    
    def delete(self, category_id: int):
        category = self.get_by_id(category_id)
        if category:
            self.db.delete(category)
            self.db.commit()
            return True
        return False
    
    def has_products(self, category_id: int):
        category = self.get_by_id(category_id)
        return category and len(category.products) > 0