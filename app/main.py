from fastapi import FastAPI
from app.all_routers import all_routers
from app.database import Base, engine

app = FastAPI()

app.include_router(all_routers)

Base.metadata.create_all(bind=engine)