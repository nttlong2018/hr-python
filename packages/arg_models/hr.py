from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float
Base = declarative_base()
class Employee(Base):
    __tablename__ = 'employees'
    #: This is a class attribute
    id = Column(Integer, primary_key=True)
    """test cai coi"""

x=Employee()
