from pymongo import MongoClient
_db=None
_coll=None
def load(config):
    global  _db
    global _coll
    if _db==None:
        _client = MongoClient(
            config["HOST"], config["PORT"]
        )
        _db=_client.get_database(config["NAME"])
        _coll=_db.get_collection(config["COLLECTION"])

    print(config)

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

