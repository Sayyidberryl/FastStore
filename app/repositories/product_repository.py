from sqlalchemy.orm import Session
from ..models.product import Product
from ..models.category import Category
from ..schemas.product_schemas import ProductCreate, ProductUpdate

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self):
        return self.db.query(Product).all()
    
    def get_by_id(self, product_id: int):
        return self.db.query(Product).filter(Product.id == product_id).first()
    
    def create(self, product_data: ProductCreate):
        product = Product(**product_data.model_dump())
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def update(self, product_id: int, product_data: ProductUpdate):
        product = self.get_by_id(product_id)
        if product:
            for key, value in product_data.model_dump(exclude_unset=True).items():
                setattr(product, key, value)
            self.db.commit()
            self.db.refresh(product)
        return product
    
    def delete(self, product_id: int):
        product = self.get_by_id(product_id)
        if product:
            self.db.delete(product)
            self.db.commit()
            return True
        return False
    
    def category_exists(self, category_id: int):
        return self.db.query(Category).filter(Category.id == category_id).first() is not None