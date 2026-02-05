from ..models.user import Users
from ..repositories.user_repository import UserRepository
from ..security.jwt import bcrypt_context,create_access_token, create_refresh_token
from sqlalchemy.orm import Session
from datetime import timedelta
from ..security.password import verify_password
from jose import jwt, JWTError
from app.core.config import settings
from fastapi import HTTPException
from starlette import status

class AuthService():
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
    def create_user(self, data):
        create_user_model = Users(
        username = data.username,
        password = bcrypt_context.hash(data.password[:72]),
        name = data.name,
        email = data.email,
        role=data.role) 
        self.user_repo.add_user(create_user_model)
        return  {"id": create_user_model.id,
                 "username": create_user_model.username,
                 "name": create_user_model.name,
                 "email": create_user_model.email,
                 "role" : create_user_model.role.value}
    
    def login(self, username:str, password:str):
        user = self.user_repo.get_by_username(username)
        if not user or not verify_password(password, user.password):
            return None
        
        access_token = create_access_token(
            username=user.username,
            user_id=user.id,
            expires_delta=timedelta(minutes=20)
        )
        refresh_token = create_refresh_token(
            data={"sub": user.username, "id": user.id},
            expires_delta=timedelta(days=7)
    )
        return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
    
    def refresh_token(self, token:str):
      try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        new_access_token = create_access_token(
            username=username,
            user_id=payload.get('id'),
            expires_delta=timedelta(minutes=20)
        )

        return {"access_token": new_access_token, "token_type": "bearer"}

      except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    def user_exists(self, username: str) -> bool:
        user = self.user_repo.get_by_username(username)
        return user is not None
    