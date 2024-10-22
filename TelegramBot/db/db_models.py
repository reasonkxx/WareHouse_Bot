from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    size = Column(String(50), nullable=True)  
    color = Column(String(50), nullable=True)