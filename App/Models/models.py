from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, Integer, String, TIMESTAMP, func, CheckConstraint
from sqlalchemy.orm import relationship

from sqlalchemy.sql.expression import null
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator, String as StringType
import uuid  # Import the UUID module




from datetime import datetime
from ..database import Base


Base = declarative_base()


class Assignment(Base):
    __tablename__ = 'assignments'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), unique=True, index=True)
    name = Column(String, nullable=False)
    points = Column(Integer,CheckConstraint('points >= 1 AND points <= 10'),  nullable=False)
    num_of_attempts = Column(Integer, CheckConstraint('num_of_attempts <= 3'),nullable=False)
    deadline = Column(DateTime, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    assignment_created = Column(DateTime, nullable=False, default=datetime.utcnow)
    assignment_updated = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner = relationship("User")



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    account_created = Column(DateTime , nullable=False, default=datetime.utcnow())  # Store timestamp as ISO 8601 string
    account_updated = Column(DateTime , nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow())  # Store timestamp as ISO 8601 string







    
