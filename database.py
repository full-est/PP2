from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql+psycopg://postgres:postgres@localhost:5432/postgres')

session_local = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()
