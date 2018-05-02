from pymongo import MongoClient
import threading
import logging
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()
_view_cache={}
import datetime
_db=None
def set_config(*args,**kwargs):
    try:
        global _db
        if type(args) is tuple and args.__len__() > 0:
            args = args[0]
        else:
            args = kwargs
        if not args.has_key("host"):
            raise Exception("'host' was not found")
        if not args.has_key("port"):
            raise Exception("'port' was not found")
        if not args.has_key("name"):
            raise Exception("'name' was not found")
        if _db == None:
            cnn = MongoClient(host=args["host"], port=args["port"])
            _db = cnn.get_database(args["name"])
            if args.has_key("user") and (args["user"] != "" or args["user"] != None):
                _db.authenticate(args["user"], args["password"])
    except Exception as ex:
        logger.debug(ex)
        raise ex


def register_view(*args,**kwargs):
    try:
        if type(args) is tuple and args.__len__() > 0:
            args = args[0]
        else:
            args = kwargs
        if not args.has_key("app"):
            raise Exception("'app' was not found")
        if not args.has_key("view"):
            raise Exception("'view' was not found")
        key = "{0}/{1}".format(args["app"], args["view"]).lower()
        if not _view_cache.has_key(key):
            lock.acquire()
            try:
                item = _db.get_collection("sys_views").find_one({
                    "View": args["view"],
                    "App": args["app"]
                })
                ret_id = None
                if item == None:
                    ret = _db.get_collection("sys_views").insert_one({
                        "View": args["view"],
                        "App": args["app"],
                        "CreatedOn": datetime.datetime.now(),
                        "CreatedOnUTC": datetime.datetime.utcnow()
                    })
                    _view_cache.update({
                        key: ret.inserted_id.__str__()
                    })
                else:
                    _view_cache.update({
                        key: item["_id"].__str__()
                    })
                lock.release()
                return _view_cache[key]
            except Exception as ex:
                lock.release()
                logger.debug(ex)
    except Exception as ex:
        logger.debug(ex)
        raise ex

def get_view_of_user(*args,**kwargs):
    pass