from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Integer, Text, Enum, BigInteger
from database import Base

class User(Base):
    __tablename__ = "User"
    fullname = Column(String(20))
    username = Column(String(20), primary_key = True)
    password = Column(String(20))
    email = Column(Text)
    phone = Column(BigInteger)

class Book(Base):
    __tablename__ = "Book"
    id_no = Column(Integer, primary_key=True, autoincrement= True)
    username = Column(String(20), ForeignKey(User.username))
    book_name = Column(String(20))
    rating = Column(Enum('1', '2', '3', '4', '5','6', '7', '8', '9', '10'))
    status = Column(Enum('Plan to read', 'Completed', 'Currently Reading', 'Paused', 'Dropped'))