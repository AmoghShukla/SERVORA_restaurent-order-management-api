from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import os
from src.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()