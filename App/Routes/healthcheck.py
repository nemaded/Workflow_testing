from fastapi import APIRouter, FastAPI, HTTPException, Response, status, Depends
from psycopg2 import OperationalError
from ..database import engine
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


router = APIRouter(    
    tags=['health_check']
)


#to connect the and query to check if database is connected 
def middleware():
    try:
            connection=engine.connect()        
            test_query = text('SELECT 1')
            connection.execute(test_query)
           
            return True
    except OperationalError:
        return False


@router.get("/healthz",status_code=status.HTTP_200_OK)
def root():
    try:
         DATABASE_URL = "postgresql://{{ secrets.POSTGRES_USER }}:{{ secrets.POSTGRES_PASSWORD }}@localhost/mydatabase"
         engine = create_engine(DATABASE_URL)
         SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
         return True
    except:
         
        if middleware():
             headers = {"Cache-Control": "no-cache"}  
             return Response(headers=headers)
        else:
            return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    
