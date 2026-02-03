from ..repositories.user_repository import UserRepository
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from ..core.database import get_db
from ..schemas.user_schemas import UserCreate, UserUpdate
from ..models.user import User

class UserService():
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def get_users_service(db: Session = Depends(get_db)):
        return UserService(UserRepository(db))
    
    def get_all_users(self):
        return self.repository.get_all()
    
    def get_users_by_id(self, id: int):
        user = self.repository.get_by_id(id)
        if user:
            return user
        else: 
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
            
    def add_users(self, data: UserCreate):
        new_user = User(
            username = data.username,
            password = data.password,
            name = data.name,
            email = data.email
        )
        return self.repository.add_user(new_user)
    
    def update_users(self, id:int, data:UserUpdate):
        user = self.repository.get_by_id(id)
        if user:
            user.username = data.username
            user.password = data.password
            user.name = data.name
            user.email = data.email
            return self.repository.update_user(user)
        else:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
    
    def delete_user(self, id:int):
        user = self.repository.get_by_id(id)
        if user:
            self.repository.delete_user(user)
            return {"message" : "User deleted successfully"}
        else: 
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )