from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text
from database import Base

class User(Base):
    __tablename__ = "User"
    username = Column(String(20), primary_key = True)
    password = Column(String(20))