from mongoengine import *
from . import personal
class Employee(personal):
    FirstName = StringField(required=True)
    LastName=StringField(required=True)
    BirthDate=DateTimeField()

