
from quicky import applications
from qmongo import helpers,database
import datetime
import threading
def on_before_insert(data):
    user = "application"
    if hasattr(threading.current_thread(),"user"):
        user = threading.current_thread().user.username
    if data.get('created_by',None)==None:
        data.update({
            "created_on":datetime.datetime.now(),
            "created_on_utc":datetime.datetime.utcnow(),
            "created_by":user
            })
def on_before_update(data):
    user = "application"
    if hasattr(threading.current_thread(),"user"):
        user = threading.current_thread().user.username
    if data.get('modified_by',None)==None:
        data.update({
            "modified_on":datetime.datetime.now(),
            "modified_on_utc":datetime.datetime.utcnow(),
            "modified_by":user
            })


helpers.define_model(
    "base",
    [],
    dict(
        created_on=helpers.create_field("date",True),
        created_on_utc=helpers.create_field("date",True),
        created_by=helpers.create_field("text",True),
        modified_on=helpers.create_field("date",True),
        modified_on_utc=helpers.create_field("date",True),
        modified_by=helpers.create_field("text",True)
    )
)