from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from .config import settings



import os


# Check if we are running in GitHub Actions workflow environment
is_github_actions = os.getenv("CI") == "true"



POSTGRES_PASSWORD = os.getenv("PGPASSWORD")
POSTGRES_DB = os.getenv("PGDATABASE")
POSTGRES_HOST =os.getenv("PGHOST")


DATABASE_URL = f"postgresql://postgres:Darshan16@localhost/cloud_db"


engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()