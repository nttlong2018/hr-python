from pymongo import MongoClient
import datetime
_db=None
def set_config(*args,**kwargs):
    global _db
    if type(args) is tuple and args.__len__()>0:
        args=args[0]
    else:
        args=kwargs
    if not args.has_key("host"):
        raise Exception("'host' was not found")
    if not args.has_key("port"):
        raise Exception("'port' was not found")
    if not args.has_key("name"):
        raise Exception("'name' was not found")
    if _db==None:
        cnn=MongoClient(host=args["host"],port=args["port"])
        _db=cnn.get_database(args["name"])
        if args.has_key("user") and (args["user"]!="" or args["user"]!=None):
            _db.authenticate(args["user"],args["password"])

def register_view(*args,**kwargs):
    if type(args) is tuple and args.__len__()>0:
        args=args[0]
    else:
        args=kwargs
    if not args.has_key("app"):
        raise Exception("'app' was not found")
    if not args.has_key("view"):
        raise Exception("'view' was not found")
    ret=_db.get_collection("sys_views").insert_one({
            "View":args["view"],
            "App":args["app"],
            "CreatedOn":datetime.datetime.now(),
            "CreatedOnUTC":datetime.datetime.utcnow()
        }
    )
    return ret.inserted_id.__str__()