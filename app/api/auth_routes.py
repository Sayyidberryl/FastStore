from fastapi import APIRouter, Depends, HTTPException
from ..schemas.auth_schemas import TokenRequest, RefreshTokenRequest
from ..schemas.user_schemas import UserCreate
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..services.auth_service import AuthService
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status



router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(db)

@router.post("/register", status_code=201)
def register(payload: UserCreate, service: AuthService = Depends(get_auth_service)):
    if service.user_exists(payload.username):
        raise HTTPException(
        status_code=400,
        detail="Username already exists"
    )
    service.create_user(payload)
    return {"message": "user created"}

@router.post("/login", response_model=TokenRequest)
def login (form: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends(get_auth_service)):
    token = service.login(form.username, form.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return token


@router.post("/refresh", response_model=TokenRequest)
def refresh(payload: RefreshTokenRequest, service: AuthService = Depends(get_auth_service)):
    return service.refresh_token(payload.refresh_token)
