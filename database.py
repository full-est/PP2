from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('postgresql+psycopg://postgres:postgres@localhost:5432/postgres')

session_local = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(engine)
