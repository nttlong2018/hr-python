import expr
from pymongo import MongoClient
_db={}
class QR():
    db=None
    def __init__(self,_db):
        self.db=_db
    def collection(self,name):
        return COLL(self,name)
class ENTITY():
    name = ""
    qr = None
    def __init__(self, qr, name):
        self.qr = qr
        self.name = name
    def insert_one(self,data):
        ret=self.qr.db.get_collection(self.name).insert_one(data)
        data.update({
            "_id":ret.inserted_id
        })
        return ret
    def insert_many(self,data):
        ret = self.qr.db.get_collection(self.name).insert_one(data)
        return ret



class COLL():
    name=""
    qr=None
    def __init__(self,qr,name):
        self.qr=qr
        self.name=name
    def find_one(self,exprression,*params):
        x=expr.get_tree(exprression,params)
        y=expr.get_expr(x,params)
        ret=self.qr.db.get_collection(self.name).find_one(y)
        return ret
    def find(self,exprression,*params):
        x=expr.get_tree(exprression,params)
        y=expr.get_expr(x,params)
        ret=self.qr.db.get_collection(self.name).find(y)
        return list(ret)






def get_query(*args,**kwargs):
    global _db
    if args.__len__()==0:
        args=kwargs
    else:
        args=args[0]
    key="host={0};port={1};user={2};pass={3};name={4}".format(
        args["host"],
        args["port"],
        args["user"],
        args["password"],
        args["name"]
    )
    if not _db.has_key(key):
        cnn=MongoClient(
            host=args["host"],
            port=args["port"]
        )
        db=cnn.get_database(args["name"])
        if args["user"]!="":
            db.authenticate(args["user"],args["password"])
        _db[key]=db
    return QR(_db[key])
