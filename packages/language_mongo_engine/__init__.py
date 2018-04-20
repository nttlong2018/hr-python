from pymongo import MongoClient
_db=None
_coll=None
def load(config):
    global  _db
    global _coll
    if _db==None:
        _client = MongoClient(
            host=config["host"],
            port=config["port"]
        )
        _db=_client.get_database(config["name"])
        if config.has_key("user") and config.get("user","")!="":
            if not _db.authenticate(config["user"],config["password"]):
                raise Exception("Can not connect to mongodb at language provider")
        _coll=_db.get_collection(config["collection"])



def get_language_item(language,app,view,key,caption):
    item=_coll.find_one({
        "language":language,
        "app":app,
        "view":view,
        "key":key
    })
    if item!=None:
        return item["value"]
    else:
        _coll.insert_one({
            "language": language,
            "app": app,
            "view": view,
            "key": key,
            "value":caption
        })
        return caption