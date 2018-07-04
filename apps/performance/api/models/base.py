from config import helpers
import datetime
import threading
def on_before_insert(data):
    user = "application"
    if hasattr(threading.current_thread(),"user"):
        user = threading.current_thread().user.username
    if data.get('created_by',None)==None:
        data.update({
            "created_on":datetime.datetime.now(),
            "created_by":user
            })
def on_before_update(data):
    user = "application"
    if hasattr(threading.current_thread(),"user"):
        user = threading.current_thread().user.username
    if data.get('modified_by',None)==None:
        data.update({
            "modified_on":datetime.datetime.now(),
            "modified_by":user
            })

helpers.define_model(
    "base",
    [],
    dict(
        _id=helpers.create_field("text"),
        created_on=helpers.create_field("date",True),
        created_by=helpers.create_field("text",True),
        modified_on=helpers.create_field("date"),
        modified_by=helpers.create_field("text")
    )
)

helpers.events("base").on_before_insert(on_before_insert).on_before_update(on_before_update)