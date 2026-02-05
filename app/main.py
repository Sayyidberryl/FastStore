from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
from app.core.database import engine, Base, get_db
from app.api import all_routers
from app.security import auth
from .security.security_dependencies import get_current_user
from sqlalchemy.orm import Session

app = FastAPI()

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
  