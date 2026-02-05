from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.database import engine, Base, get_db
from app.api import all_routers
from app.security import auth
from .security.security_dependencies import get_current_user
from sqlalchemy.orm import Session
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)

app = FastAPI(
    title="FastStore API", 
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Exception handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

Base.metadata.create_all(bind=engine)

for router in all_routers:
    app.include_router(router, prefix="/api")
    
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get("/", status_code=200)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication failed"
        )
    return {'User': user}
  

@app.get("/")
def root():
    return {"message": "FastStore API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)