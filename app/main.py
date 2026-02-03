from fastapi import FastAPI
from app.core.database import engine, Base
from app.api import all_routers

app = FastAPI()

Base.metadata.create_all(bind=engine)
for router in all_routers:
    app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "API is running"}