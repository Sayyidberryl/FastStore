from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from ..models.user import Roles
from typing import Optional


class UserBase(BaseModel):
    username: str = Field(...,min_length=6, max_length=16)
    name: str = Field(...,min_length=6, max_length=16)
    email : EmailStr
    role: Optional[Roles] = Roles.user
    
class UserCreate(UserBase):
    password: str =  Field(min_length=6)
 

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=6, max_length=16)
    password: Optional[str] = Field(None, min_length=6, max_length=16)
    name: Optional[str] = Field(None, min_length=6, max_length=16)
    email: Optional[EmailStr]
    role: Optional[Roles] = Roles.user
    
class UserResponse(UserBase):
    id:int
    class Config:
        from_attributes= True