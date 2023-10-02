from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr 
    password: str

class UserOut(BaseModel):
    first_name: str
    last_name: str
    email: str
    
class UserCredentials(BaseModel):
    first_name: str
    password: str

class AssignmentCreate(BaseModel):
    name: str
    points: int
    num_of_attempts: int
    deadline: str

class AssignmentResponse(BaseModel):
    id: str
    name: str
    points: int
    num_of_attempts: int
    deadline: datetime
    owner_id: int
    owner:UserOut
    assignment_created: datetime
    assignment_updated: datetime
   