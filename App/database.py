from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings



import os


# Check if we are running in GitHub Actions workflow environment

is_github_actions = os.getenv("CI") == "true"
print("git hub true")

if is_github_actions:

    POSTGRES_PASSWORD = os.getenv("PGPASSWORD")
    POSTGRES_HOST =os.getenv("PGHOST")
    DATABASE_URL = f"postgresql://postgres:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/cloud_bd"

else:
    DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"

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