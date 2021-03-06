from sqlalchemy import Column, String
from sqlalchemy import Integer
from app.models.base import Base



class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String(50),nullable=False)
    author = Column('author', String(200),default='未名')
    binding = Column(String(20)) #装帧
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15),nullable=False,unique=True)#保持唯一
    summary = Column(String(3000)) #简介
    image = Column(String(50))

