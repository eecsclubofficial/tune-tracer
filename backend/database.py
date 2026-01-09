from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Trying to see alternative to enter username and password, kind of risky to enter in public. Try for .env and then import.
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost:5432/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind = engine, autocommit = False, autoflush= False)

Base = declarative_base()
