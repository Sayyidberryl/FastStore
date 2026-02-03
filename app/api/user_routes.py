from fastapi import APIRouter, Depends, HTTPException
from ..core.database import get_db
from sqlalchemy.orm import Session
from ..schemas.user_schemas import UserCreate, UserUpdate, UserResponse
from ..services.user_service import UserService
from ..repositories.user_repository import UserRepository
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

def get_user_service(db: Session = Depends(get_db)):
    return UserService(UserRepository(db))

@router.get("/", response_model = List[UserResponse])
def get_all_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users(
    )
@router.get("/{id}", response_model = UserResponse)
def get_user_by_id( id:int,service: UserService = Depends(get_user_service)):
    user = service.get_users_by_id(id)
    if user:
        return user
    else:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
@router.post("/", response_model=UserResponse,status_code=201)
def add_user( payload: UserCreate, service:UserService = Depends(get_user_service)):
    return service.add_users(payload)

@router.patch("/{id}", response_model=UserResponse)
def update_user(id:int, user_update: UserUpdate, service:UserService = Depends(get_user_service )):
    user = service.update_users(id, user_update)
    if user:
        return user
    else:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
        
@router.delete("/{id}", status_code=204)
def delete_user(id:int, service:UserService = Depends(get_user_service)):
    user = service.delete_user(id)
    if not user:
        raise HTTPException (
            status_code=404,
            detail="User not found"
        )
    