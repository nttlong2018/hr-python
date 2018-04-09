from mongoengine import *
from . import Base
class Personal(Base):
    FirstName = StringField(required=True)
    LastName=StringField(required=True)
    BirthDate=DateTimeField()
