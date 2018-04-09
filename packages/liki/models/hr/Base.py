from mongoengine import *
class Base(Document):
    CreatedBy = StringField(required=True)
    CreatedOn=DateTimeField(required=True)
    ModifiedBy = StringField()
    ModifiedOn = DateTimeField()
    Description=StringField()

