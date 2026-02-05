from datetime import timedelta, datetime
from ..models.user import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.config import settings
from jose import jwt, JWTError
from .password import verify_password, hash_password



bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


def authenticate_user(username:str, password:str, db,):
    user = db.query(Users).filter(Users.username == username).first()
    if not user or not verify_password(password, user.password):
        return None
    return user

def create_access_token(username:str, user_id:int, expires_delta: timedelta):
    encode = {'sub' : username, 'id' : user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp' : expires})
    return jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

 