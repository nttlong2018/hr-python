from pymongo import MongoClient
_coll=None
_data=None
def set_config(*args,**kwargs):
    global _coll
    settings=kwargs
    if type(args) is dict:
        settings=args
    elif type(args) is tuple and args.__len__()>0:
        settings=args[0]
    if _coll==None:
        cnn=MongoClient(
            host=settings["host"],
            port=settings["port"]
        )
        db=cnn.get_database(settings["name"])
        if settings["user"]!=None and settings["user"]!="":
            if not db.authenticate(settings["user"],settings["password"]):
                raise(Exception("Can not authenticate data"))
        _coll=db.get_collection(settings["collection"])

def set_data(*args,**kwargs):
    global _data
    if _coll.count()==0:
        _coll.insert_one(kwargs)
        _data=kwargs
    else:
        data=_coll.find_one()
        _data=kwargs
        _data.update(data)
        updater={}
        for key in _data.keys():
            if key!="_id":
                updater.update({
                    key:_data[key]
                })
        _coll.update_one({
            "_id":_data["_id"]
        },{
            "$set":updater
        })

def get_data():
    return _data
def save():
    updater = {}
    for key in _data.keys():
        if key != "_id":
            updater.update({
                key: _data[key]
            })
    _coll.update_one({
        "_id": _data["_id"]
    }, {
        "$set": updater
    })
