from pymongo import MongoClient
_db=None
def set_connection(*args,**kwargs):
    print args
    print kwargs
    global _db
    if _db==None:
        _db=MongoClient(host=kwargs["host"],port=kwargs["port"]).get_database(kwargs["name"])
        if args[0].has_key("user"):
            _db.authenticate(kwargs["user"],kwargs["password"])
def coll(name):
    return _db.get_collection(name)

