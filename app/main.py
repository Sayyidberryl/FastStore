from fastapi import FastAPI
from ..app.core.database import engine, Base
app = FastAPI()

Base.metadata.create_all(bind=engine)