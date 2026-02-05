from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from fastapi import Form, UploadFile, File

class ProductBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    stock: int = Field(..., ge=0)
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductCreateForm:
    def __init__(
        self,
        name: str = Form(..., min_length=3, max_length=200),
        description: Optional[str] = Form(None),
        price: float = Form(..., ge=0),
        stock: int = Form(..., ge=0),
        category_id: int = Form(...),
        image: Optional[UploadFile] = File(None)
    ):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.category_id = category_id
        self.image = image

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    stock: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = None

class ProductUpdateForm:
    def __init__(
        self,
        name: Optional[str] = Form(None, min_length=3, max_length=200),
        description: Optional[str] = Form(None),
        price: Optional[float] = Form(None, ge=0),
        stock: Optional[int] = Form(None, ge=0),
        category_id: Optional[int] = Form(None),
        image: Optional[UploadFile] = File(None)
    ):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.category_id = category_id
        self.image = image

class ProductResponse(ProductBase):
    id: int
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True