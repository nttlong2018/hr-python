from sqlalchemy.sql.functions import count

from helpers import expr,validators

from pymongo import MongoClient
from pymongo.errors import OperationFailure
import logging
import copy
import pymongo
import pytz
from bson.codec_options import CodecOptions

logger = logging.getLogger(__name__)
_db={}
def extract_data(data):
    ret={}
    for key in data.keys():
        if key.find(".")>-1:
            items=key.split('.')
            if not ret.has_key(items[0]):
                ret.update({
                    items[0]:{}
                })
            val=ret[items[0]]
            for x in items[1:items.__len__()-1]:
                if not val.has_key(x):
                    val.update({
                        x:{}
                    })
                val=val[x]
            val.update({
                items[items.__len__() - 1]:data[key]
            })

        else:
            ret.update({
                key:data[key]
            })
    return ret
class QR():
    db=None
    _entity=None
    _codec_options=None
    def __init__(self,config):
        self.db=config["database"]
        self._codec_options=config["codec_options"]
    def collection(self,name):
        "get collection from database. including methods: find_one,find,get_list,get_item,where,entity,aggregate "
        if name==None or name=="":
            raise Exception("'name' can not be null or empty")
        return COLL(self,name)
    def get_collection_names(self):
        return list(self.db.collection_names())
class ENTITY():
    name = ""
    qr = None
    _data={}
    _action=None
    _expr=None
    def __init__(self, qr, name):
        self.qr = qr
        self.name = name
    def insert_one(self,*args,**kwargs):
        if args==():
            self._data=kwargs
        else:
            self._data = args[0]

        self._action="insert_one"

        return self
    def insert_many(self,data):
        self._action = "insert_many"
        self._data = data
        return self
    def update_one(self,data):
        self._action="update_one"
        if not self._data.has_key("$set"):
            self._data.update({
                "$set":data
            })
        else:
            x=self._data["$set"]
            for key in data.keys():
                x.update({
                    key:data[key]
                })
        return self
    def update_many(self,data,*params):
        self._action = "update_many"
        if not self._data.has_key("$set"):
            self._data.update({
                "$set": data
            })
        else:
            x = self._data["$set"]
            for key in data.keys():
                x.update({
                    key: data[key]
                })
        return self
    def push(self,data):
        if self._action==None:
            self._action="update_many"
        if not self._data.has_key("$push"):
            self._data.update({
                "$push": data
            })
        else:
            x = self._data["$push"]
            for key in data.keys():
                x.update({
                    key: data[key]
                })
        return self
    def pull(self,data):
        if self._action==None:
            self._action="update_many"
        if not self._data.has_key("$pull"):
            self._data.update({
                "$pull": data
            })
        else:
            x = self._data["$pull"]
            for key in data.keys():
                x.update({
                    key: data[key]
                })
        return self
    def inc(self,data):
        if self._action==None:
            self._action="update_many"
        if not self._data.has_key("$inc"):
            self._data.update({
                "$inc": data
            })
        else:
            x = self._data["$inc"]
            for key in data.keys():
                x.update({
                    key: data[key]
                })
        return self
    def dec(self,data):
        if self._action == None:
            self._action = "update_many"
        if not self._data.has_key("$dec"):
            self._data.update({
                "$dec": data
            })
        else:
            x = self._data["$dec"]
            for key in data.keys():
                x.update({
                    key: data[key]
                })
        return self
    def filter(self,expression,*args,**kwargs):
        self._expr = expression
        if type(expression) is str:
            expr_tr=expr.get_tree(expression,*args,**kwargs)
            self._expr = expr.parse_expression_to_json_expression(expression,*args,**kwargs)
        return self
    def delete(self):
        self._action="delete"
        return self
    def get_duplicate_error(self,ex):
        start = ex.message.find(" index:") + " index:".__len__()
        end = ex.message.find(" dup key:", start)
        key = ex.message[start:end]
        key = key.replace(" ", "")
        info = self.qr.db.get_collection(self.name).index_information()
        fields = info[key]["key"]
        ret_fields = []
        for item in fields:
            ret_fields.append(item[0])
        return dict(
            error=dict(
                fields=ret_fields,
                code="duplicate"
            )
        )
    def commit(self):
        _coll=self.qr.db.get_collection(self.name).with_options(codec_options=self.qr._codec_options)
        if self._action=="insert_one":
            ret_data={}
            try:
                self._data=extract_data(self._data)
                ret_validate_require=validators.validate_require_data(self.name,self._data)
                if ret_validate_require.__len__()>0:
                    return dict(
                        error=dict(
                            fields=ret_validate_require,
                            code="missing"
                        )
                    )
                ret_validate_data_type=validators.validate_type_of_data(self.name,self._data)
                if ret_validate_data_type.__len__()>0:
                    return dict(
                        error=dict(
                            fields=ret_validate_data_type,
                            code="invalid_data"
                        )
                    )
                ret = _coll.insert_one(self._data)
                ret_data = self._data.copy()
                ret_data.update({
                    "_id": ret.inserted_id
                })
                self._action = None
                self._data = {}
                return dict(
                    error=None,
                    data=ret_data
                )
            except pymongo.errors.DuplicateKeyError as ex:
                ret_data= self.get_duplicate_error(ex)
                ret_data.update({
                    "data":self._data
                })
                return ret_data

            except Exception as ex:
                raise ex


        elif self._action=="insert_many":
            ret = _coll.insert_many(self._data)
            self._action = None
            self._data = {}
            return ret
        else:
            if self._expr==None:
                raise Exception("Can not modified data without using filter")
            if self._action=="update_one":
                ret = _coll.update_one(self._expr,self._data)
                self._expr=None
                self._action = None
                self._data = {}
                return ret
            if self._action=="update_many":
                ret_validate_require = validators.validate_require_data(self.name, self._data["$set"], partial=True)
                if ret_validate_require.__len__() > 0:
                    return dict(
                        error=dict(
                            fields=ret_validate_require,
                            code="missing"
                        )
                    )
                ret_validate_data_type = validators.validate_type_of_data(self.name, self._data["$set"])
                if ret_validate_data_type.__len__() > 0:
                    return dict(
                        error=dict(
                            fields=ret_validate_data_type,
                            code="invalid_data"
                        )
                    )
                updater={}
                for key in self._data.keys():
                    if key=="$pull":
                        fx={}
                        for x in self._data["$pull"].keys():
                            if x.count(".")>0:
                                items=x.split('.')
                                index=0
                                c=fx
                                while index<items.__len__()-1:
                                    c.update({
                                        items[index]: {}
                                    })
                                    c = c[items[index]]
                                    index+=1
                                c.update({
                                    items[items.__len__()-1]:self._data["$pull"][x]
                                })

                            else:
                                fx.update({
                                    x:self._data["$pull"]
                                })
                        updater.update({
                            "$pull": fx
                        })

                    else:
                        updater.update({
                            key:self._data[key]
                        })
                try:

                    ret = _coll.update_many(self._expr,updater)
                    self._expr = None
                    self._action = None
                    self._data = {}
                    return dict(
                        error=None,
                        data=ret
                    )
                except pymongo.errors.DuplicateKeyError as ex:
                    ret_data = self.get_duplicate_error(ex)
                    ret_data.update({
                        "data": self._data
                    })
                    return ret_data
                except Exception as ex:
                    raise ex

            if self._action=="delete":
                ret = _coll.delete_many(self._expr)
                self._expr = None
                self._action = None
                self._data = {}
                return ret
class WHERE():
    name = ""
    _coll = None
    _where_list=[]
    _entity=None

    def _get_where(self):
        i = 0
        x = expr.get_tree(self._where_list[i]["expression"], *self._where_list[i].get("params", []))
        y = expr.get_expr(x, self._where_list[i].get("params", []))
        i += 1
        while i < self._where_list.__len__():
            item = self._where_list[i]
            _x = expr.get_tree(item["expression"], *item.get("params", []))
            _y = expr.get_expr(_x, *item.get("params", []))
            y = {
                "$" + item["type"]: [
                    y, _y
                ]
            }
            i += 1
        return y

    def __init__(self, coll):
        self._coll = coll
        self.name=coll.name
    def get_list(self):
        if self._where_list.__len__()==0:
            return self._coll.get_list()
        else:
            return self._coll.find(self._get_where())
    def get_item(self):
        if self._where_list.__len__() == 0:
            return self._coll.get_item()
        else:
            return self._coll.find_one(self._get_where())
    def to_entity(self):
        if self._entity==None:
            self._entity=ENTITY(self._coll.qr,self.name)
        return self._entity
    def where(self,expression,*params):
        self._where_list.append(dict(
            expression=expression,
            params=params,
            type=None
        ))
        return self
    def where_and(self,expression,*params):
        self._where_list.append(dict(
            expression=expression,
            params=params,
            type="and"

        ))
        return self
    def where_or(self,expression,*params):
        self._where_list.append(dict(
            expression=expression,
            params=params,
            type="or"

        ))
        return self
    def update(self,data):
        self.to_entity().filter(self._get_where())
        self.to_entity().update_one(data)
        return self
    def update_many(self,data):
        self.to_entity().filter(self._get_where())
        self.to_entity().update_many(data)
        return self
    def push(self,data):
        self.to_entity().filter(self._get_where())
        self.to_entity().push(data)
        return self
    def pull(self,data):
        self.to_entity().filter(self._get_where())
        self.to_entity().pull(data)
        return self
    def inc(self,data):
        self.to_entity().filter(self._get_where())
        self.to_entity().inc(data)
        return self
    def dec(self,data):
        self.to_entity().filter(self._get_where())
        self.to_entity().dec(data)
        return self
    def delete(self,data):
        self.to_entity().filter(self._get_where())
        self.to_entity().delete()
        return self
    def commit(self):
        return self.to_entity().commit()
class COLL():
    name=""
    qr=None
    _where=None
    _entity=None

    def __init__(self,qr,name):
        self.qr=qr
        self.name=name
    def get_collection(self):
        return self.qr.db.get_collection(self.name).with_options(codec_options=self.qr._codec_options)
    def find_one(self,exprression,*args,**kwargs):
        """find one item with conditional ex: find_one("Username={0}","admin"),
            find_one("Username='admin'"),
            find_one("Username=@username",username="admin")
         """
        if type(exprression) is dict:
            ret = self.get_collection().find_one(exprression)
            return ret
        elif type(exprression) is tuple:
            ret = self.get_collection().find_one(exprression[0])
            return ret
        else:
            if type(args) is tuple and args.__len__()>0 and kwargs=={}:
                kwargs=args[0]
            filter = expr.parse_expression_to_json_expression(exprression, kwargs)
            ret=self.get_collection().find_one(filter)
            return ret
    def find(self,exprression,*params):
        """find and get a list of items item with conditional ex: find("Username={0}","admin"),
                    find("Username='admin'"),
                    find("Username=@username",username="admin")
                 """
        if type(exprression) is dict:
            ret = self.get_collection().find(exprression)
            return list(ret)
        elif type(exprression) is tuple:
            ret = self.get_collection().find(exprression[0])
            return list(ret)
        else:
            x=expr.get_tree(exprression,params)
            y=expr.get_expr(x,params)
            ret=self.get_collection().find(y)
            return list(ret)
    def get_list(self):
        ret = self.get_collection().find()
        return list(ret)
    def get_item(self):
        ret = self.get_collection().find_one()
        return ret
    def where(self,exprression,*params):
        """Create filter expression before get data from mongo
            Ex:where("strLenCP(Username)<3").get_list(),
               where("strLenCP(Username)<@strong_number",strong_number=5).get_list()
               where("strLenCP(Username)<{0}",5).get_list()

        """
        if self._where==None:
            self._where=WHERE(self)
            self._where.where(exprression,params)
        return self._where
    def entity(self):
        if self._entity==None:
            self._entity=ENTITY(self.qr,self.name)
        return self._entity
    def aggregate(self):
        """create aggregate before create pipeline"""
        return AGGREGATE(self.qr,self.name)
    def entity(self):
        if self._entity==None:
            self._entity=ENTITY(self.qr,self.name)
        return self._entity
    def insert(self,*args,**kwargs):
        ac=self.entity().insert_one(*args,**kwargs)
        ret=ac.commit()
        return ret
    def update(self,data,filter,*args,**kwargs):
        if type(args) is tuple and args.__len__()>0 and kwargs=={}:
            kwargs=args[0]
        ac=self.entity().filter(filter,kwargs)
        ac.update_many(data)
        ret=ac.commit()
        return ret
    def create_unique_index(self,*args,**kwargs):
        for item in args:
            keys=[]
            partialFilterExpression={}
            coll = self.get_collection()
            for x in item:
                keys.append((x["field"],pymongo.ASCENDING))
                partialFilterExpression.update({
                    x["field"]:{
                        "$type":x["type"]
                    }
                })

            # collation = pymongo.collation.Collation(locale=x["locale"], strength=2)
            coll.create_index(keys,
                              unique=True,

                              partialFilterExpression=partialFilterExpression)

        return self
    def delete(self,filter,*args,**kwargs):
        ac=self.entity().filter(filter,kwargs)
        ac.delete()
        ret=ac.commit()
        return ret
    def get_filter_keys(self,keys):
        ret=""
        for key in keys:
            ret+="("+key+"==@"+key+")and"
        return ret[0:ret.__len__()-3]
    def save(self,data,keys):
        filter_key=self.get_filter_keys(keys)
        data_item=self.find_one(filter_key,data)
        ret={}
        if data_item!=None:
            ret_val=self.update(data,filter_key,data)
            ret.update({
                "action":"update",
                "_id":data_item["_id"],
                "error": ret_val["error"]
            })
        else:
            ret_val=self.insert(data)
            ret.update({
                "action": "update",
                "_id": ret_val["data"]["_id"],
                "error": ret_val["error"]
            })

        return data_item
class AGGREGATE():
    name = ""
    qr = None
    _pipe=[]

    def __init__(self, qr, name):
        self.qr = qr
        self.name = name
        self._pipe=[]
    def project(self,*args,**kwargs):
        """
        Create project pipeline
        Ex:
            project(
                dict(
                    FullName="toUpper(concat(FirstName,' ',LastName))",
                    Age="year(@time_now)- year(BirthDate)",
                    Username=1,
                    CreatedOn=1
                ),
                time_now=datetime.now()
            )
        :param args:
        :param kwargs:
        :return:
        """
        _project = {}
        if kwargs=={}:
            kwargs = args[0]
            if args.__len__()>1:

                params=args[1]
            else:
                params = args[0]

        else:

            params=[]
            if type(args) is tuple and args.__len__()>1 and type(args[0]) is dict:

                params=[e for e in args if args.index(e)>0]
                kwargs = args[0]
                args=[]
            elif type(args) is tuple and args.__len__()==1 and type(args[0]) is dict:
                params=kwargs
                kwargs=args[0]
            # for x in args:
            #     _project.update({
            #         x:1
            #     })
        for key in kwargs.keys():
            _project.update({
                key: expr.get_calc_expr(kwargs[key],params)
            })
        self._pipe.append({
            "$project":_project
        })
        return self
    def group(self,_id,selectors,*args,**kwargs):
        __id={}
        if type(_id) is dict:
            for key in _id.keys():
                __id.update({
                    key:expr.get_calc_expr(_id[key],*args,**kwargs)
                })
        else:
            __id="$"+_id
        _group = {
            "$group": {
                "_id": __id
            }
        }
        if not type(selectors) is dict:
            raise (Exception("'selectot' must be dict type"))


        for key in selectors.keys():
            _group["$group"].update({
                key:expr.get_calc_expr(selectors[key],*args,**kwargs)
            })
        self._pipe.append(_group)
        return self
    def skip(self,len):
        self._pipe.append({
            "$skip":len
        })
        return self
    def limit(self,num):
        self._pipe.append({
            "$limit": num
        })
        return self
    def unwind(self,field_name):
        if field_name[0:1]!="$":
            field_name="$"+field_name
        self._pipe.append({
            "$unwind":{"path":field_name,
                        "preserveNullAndEmptyArrays":True
                    }
        })
        return self
    def match(self,expression, *args,**kwargs):
        """Beware! You could not use any Aggregation Pipeline Operators, just use this function with Field Logic comparasion such as:
        and,or, contains,==,!=,>,<,..
        """
        if args==():
            args=kwargs

        if type(expression) is dict:
            self._pipe.append({
                "$match":expression
            })
            return self
        if type(expression) is str:
            self._pipe.append({
                "$match": expr.parse_expression_to_json_expression(expression,args)
            })
            return self

        pass
    def lookup(self,
               source=None,
               local_field=None,
               foreign_field=None,
               alias=None,
               *args,**kwargs):
        if args==() and kwargs=={}:
            _source=source
            if source.__class__ is COLL:
                _source=source.name

            kwargs.update(source=_source,
                          local_field=local_field,
                          foreign_field=foreign_field,
                          alias=alias)
        else:
            if not kwargs.has_key("source"):
                raise Exception("'source' was not found")
            if not kwargs.has_key("local_field"):
                raise Exception("'local_field' was not found")
            if not kwargs.has_key("foreign_field"):
                raise Exception("'foreign_field' was not found")
            if not kwargs.has_key("alias"):
                raise Exception("'alias' was not found")
        self._pipe.append({
            "$lookup":{
                "from":kwargs["source"],
                "localField":kwargs["local_field"],
                "foreignField":kwargs["foreign_field"],
                "as":kwargs["alias"]
            }
        })
        return self
    def sort(self,*args,**kwargs):
        _sort={

        }
        self._pipe.append({
            "$sort":kwargs
        })
        return self
    def count(self,alias):
        self._pipe.append({
            "$count":alias
        })
        return self
    def get_item(self):
        ret=self.get_list()
        if ret.__len__()==0:
            return None
        else:
            return ret[0]
    def get_list(self):
        # try:
        #     return self.qr.db.get_collection(self.name).aggregate(self._pipe,explain=False)["cursor"]["firstBatch"]
        # except Exception as ex:
        #     return list(self.qr.db.get_collection(self.name).aggregate(self._pipe))
        coll=self.qr.db.get_collection(self.name).with_options(codec_options=self.qr._codec_options)
        ret=list(coll.aggregate(self._pipe))
        self._pipe=[]
        return ret
    def get_page(self,page_index,page_size):
        _tmp_pipe=copy.copy(self._pipe)
        total_items=self.count("total_items").get_item()
        self._pipe=_tmp_pipe
        items=self.skip(page_index*page_size).limit(page_size).get_list()
        return dict(
            page_size=page_size,
            page_index=page_index,
            total_items=total_items["total_items"],
            items=items
        )
    def __copy__(self):
        ret=AGGREGATE(self.qr,self.name)
        ret._pipe=[x for x in self._pipe]
        return ret
    def copy(self):
        return self.__copy__()
def connect(*args,**kwargs):
    """
    Create db instance <br/>
    Ex:query.get_query(host="ip address",\n
                        name="database name",\n
                        port=,\n
                        user=,\n
                        password=,\n
                        tz_aware=True/False,\n
                        timezone='refer to link https://en.wikipedia.org/wiki/List_of_tz_database_time_zones'\n
                        )\n
     \n Why 'tz_aware' is the most important for your mongodb connection?\n
     Please refer to http://api.mongodb.com/python/current/examples/datetimes.html\n
     If you are using Django framwork this information maybe in 'USE_TZ' of setting.py\n
      Why 'timezone' is the most important for your mongodb connection?\n
      Please refer to http://api.mongodb.com/python/current/examples/datetimes.html\n
       If you are using Django framwork this information maybe in 'USE_TZ' of setting.py\n

    """
    try:
        global _db
        if args.__len__()==0:
            args=kwargs
        else:
            args=args[0]
        if not args.has_key("host"):
            raise (Exception("This look like you forgot set 'host' param.\n Where is your mongodb hosting?"))
        if not args.has_key("port"):
            raise (Exception("This look like you forgot set 'port' param.\n What is your mongodb port? Is it '27017'"))
        if not args.has_key("name"):
            raise (Exception("This look like you forgot set 'name' (The name of database) param.\n Which is your mongodb database?"))

        if args.has_key("user") and args.get("user",None)!=None:
            if not args.has_key("password") or args.get("password", "") == "":
                raise (Exception("This look like you forgot set 'user' and 'password' params.\n How is your mongodb authorization?"))
        key="host={0};port={1};user={2};pass={3};name={4}".format(
            args["host"],
            args["port"],
            args.get("user","none"),
            args.get("password","none"),
            args["name"],
            args.get("tz_aware",False),
            args.get("timezone",None)
        )
        if not _db.has_key(key):
            cnn=MongoClient(
                host=args["host"],
                port=args["port"]
            )
            db=cnn.get_database(args["name"])
            if args["user"]!=None:
                db.authenticate(args["user"],args["password"])
            if args.get("tz_aware",False):
                codec_options = CodecOptions(
                    tz_aware=True,
                    tzinfo=pytz.timezone(args["timezone"])
                )
            else:
                codec_options = CodecOptions(
                    tz_aware=False
                )

            _db[key]={
                "database":db,
                "codec_options":codec_options
            }
        return QR(_db[key])
    except OperationFailure as ex:
        logger.debug(ex)
        raise ex
    except Exception as ex:
        logger.debug(ex)
        raise ex
