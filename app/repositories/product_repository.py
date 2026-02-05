from sqlalchemy.orm import Session
from ..models.product import Product
from ..models.category import Category
from ..schemas.product_schemas import ProductCreate, ProductUpdate, ProductCreateForm, ProductUpdateForm
from typing import Optional

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self):
        return self.db.query(Product).all()
    
    def get_by_id(self, product_id: int):
        return self.db.query(Product).filter(Product.id == product_id).first()
    
    def create(self, product_data: ProductCreate, image_url: Optional[str] = None):
        product_dict = product_data.model_dump()
        if image_url:
            product_dict["image_url"] = image_url
        product = Product(**product_dict)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def create_from_form(self, form_data: ProductCreateForm, image_url: Optional[str] = None):
        product = Product(
            name=form_data.name,
            description=form_data.description,
            price=form_data.price,
            stock=form_data.stock,
            category_id=form_data.category_id,
            image_url=image_url
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def update(self, product_id: int, product_data: ProductUpdate, image_url: Optional[str] = None):
        product = self.get_by_id(product_id)
        if product:
            for key, value in product_data.model_dump(exclude_unset=True).items():
                setattr(product, key, value)
            if image_url is not None:
                product.image_url = image_url
            self.db.commit()
            self.db.refresh(product)
        return product
    
    def update_from_form(self, product_id: int, form_data: ProductUpdateForm, image_url: Optional[str] = None):
        product = self.get_by_id(product_id)
        if product:
            if form_data.name is not None:
                product.name = form_data.name
            if form_data.description is not None:
                product.description = form_data.description
            if form_data.price is not None:
                product.price = form_data.price
            if form_data.stock is not None:
                product.stock = form_data.stock
            if form_data.category_id is not None:
                product.category_id = form_data.category_id
            if image_url is not None:
                product.image_url = image_url
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