from pymongo import MongoClient
from hrm import settings
_db=None
def coll(name):
    global _db
    if _db==None:
        cnn=MongoClient(
            host=settings.DATABASE["host"],
            port=settings.DATABASE["port"]
            )
        _db=cnn.get_database(settings.DATABASE["name"])
        if settings.DATABASE.has_key("user"):
            _db.authenticate(settings.DATABASE["user"],settings["password"])
    return _db.get_collection(name)

