from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

session_local = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(engine)
