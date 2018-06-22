from sqlalchemy.sql.functions import count
from  datetime import datetime
from helpers import expr,validators
from helpers import get_model,get_keys_of_model
from pymongo import MongoClient
from pymongo.errors import OperationFailure
import logging
import copy
import pymongo
import pytz
from bson.codec_options import CodecOptions
import helpers
from quicky import tenancy
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
    """
    Define queryable
    """

    def __init__(self,config):
        self.db = None
        self._entity = None
        self._codec_options = None
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
    """
        Define entity
    """
    def __init__(self, qr,coll, name):
        # type:(QR,COLL,str)->NotImplemented
        """
        Create new entity instance
        :param qr:query
        :param coll:COLLECTION
        :param name:model name
        """
        self.name = ""
        self.qr = None
        self._data = {}
        self._action = None
        self._expr = None
        self.qr = qr
        self.name = name
        self._coll=coll
    def insert_one(self,*args,**kwargs):
        # type: (tuple,dict) -> ENTITY
        """
        Insert one item example insert_one(a=1)
        :param args:
        :param kwargs:
        :return:
        """
        if args==():
            self._data=kwargs
        else:
            self._data = args[0]

        self._action="insert_one"

        return self
    def insert_many(self,data):
        # type: (tuple,dict) -> ENTITY
        """
        Insert many items
        :param data:
        :return:
        """
        self._action = "insert_many"
        self._data = data
        return self
    def update_one(self,data):
        # type: (dict) -> ENTITY
        """
        update one item
        :param data:
        :return:
        """
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
        # type: (tuple,dict) -> ENTITY
        """
        Update many items
        :param data:
        :param params:
        :return:
        """
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
        """
        Push data into collection
        :param data:
        :return:
        """
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
        """
        Create filter before update or delete
        :param expression:
        :param args:
        :param kwargs:
        :return:
        """
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
        """
        Commit actio. Example; insert_many then commit, update or delete require filter before
        :return:
        """
        _id=None
        if self._data.has_key("$set"):
            _id=self._data["$set"].get("_id",None)
            for key in self._data["$set"].keys():
                if key[0:1]=="$" or key == "_id":
                    self._data["$set"].pop(key)
        else:
            for key in self._data.keys():
                if key[0:1]=="$" or key == "_id":
                    self._data.pop(key)
                


        _coll=self.qr.db.get_collection(self.name).with_options(codec_options=self.qr._codec_options)
        model_events = helpers.events(self._coll._model.name)
        if self._action=="insert_one":
            ret_data={}
            try:
                self._data=extract_data(self._data)
                if model_events!=None:
                    for fn in model_events._on_before_insert:
                        fn(self._data)
                ret_validate_require=validators.validate_require_data(self._coll._model.name,self._data)
                if ret_validate_require.__len__()>0:
                    return dict(
                        error=dict(
                            fields=ret_validate_require,
                            code="missing"
                        )
                    )
                ret_validate_data_type=validators.validate_type_of_data(self._coll._model.name,self._data)
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
            if model_events:
                for item in self._data:
                    for fn in model_events._on_before_insert:
                        fn(item)
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
                if model_events:
                    for fn in model_events._on_before_update:
                        fn(self._data["$set"])
                ret_validate_require = validators.validate_require_data(self._coll._model.name, self._data["$set"], partial=True)
                if ret_validate_require.__len__() > 0:
                    return dict(
                        error=dict(
                            fields=ret_validate_require,
                            code="missing"
                        )
                    )
                ret_validate_data_type = validators.validate_type_of_data(self._coll._model.name, self._data["$set"])
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
                return { "deleted":ret.deleted_count}
class WHERE():
    """
    This class define where for Entity will be remove on the next version
    """


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
        self.name = ""
        self._coll = None
        self._where_list = []
        self._entity = None
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
            self._entity=ENTITY(self._coll.qr,self._coll,self.name)
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
    """
    Define a collection
    """
    def __init__(self,qr,name):
        # type: (QR,str) -> NotImplemented
        """
        Create instance of COLL
        :param qr:
        :param name:
        """
        self.name = ""
        self.qr = None
        self._where = None
        self._entity = None
        self._none_schema_name = None
        self._none_schema_name=name
        import threading
        if hasattr(threading.currentThread(),"tenancy_code") and tenancy.get_schema()!="":
            self.name=tenancy.get_schema()+"."+name
        else:
            self.name = name
        self._model=get_model(name)
       

        self.qr=qr
    def descibe_fields(self,tabs,fields):
        """
        Return list of fields
        :param tabs:
        :param fields:
        :return:
        """
        _fields = ""
        for x in fields:
            _fields += tabs+ x + "\n"
        return  _fields
    def get_name(self):
        # type:() -> str
        """
        Get name of collection without schema
        :return:
        """
        return self._none_schema_name
    def get_collection(self):
        # type: () -> pymongo.collection.Collection
        """
        get mongodb collection, before get this method will run create unique key script according to 'key' in model
        :return:
        """
        ret_coll=self.qr.db.get_collection(self.name).with_options(codec_options=self.qr._codec_options)
        key_info=get_keys_of_model(self._none_schema_name)
        if key_info["keys"]!=None  and not key_info["has_created"]:
            for item in key_info["keys"]:
                keys=[]
                partialFilterExpression={}
                
                for field_name in item:
                    
                    keys.append((field_name,pymongo.ASCENDING))
                    if(self._model.meta[field_name]=="text"):
                        partialFilterExpression.update({
                            field_name:{
                                "$type":"string"
                            }
                        })
                if keys.__len__() > 0:
                    ret_coll.create_index(keys,
                                      unique=True,
                                      partialFilterExpression=partialFilterExpression)
            key_info["has_created"]=True
        return ret_coll
    def find_one(self,exprression,*args,**kwargs):
        # type: (str,dict) -> dict
        # type: (str,tuple) -> dict
        # type: (str,int) -> dict
        # type: (str,bool) -> dict
        # type: (str,float) -> dict
        # type: (str,datetime) -> dict
        # type: (str,list) -> dict
        """find one item with conditional ex: find_one("Username={0}","admin"),
            find_one("Username='admin'"),
            find_one("Username=@username",username="admin")
         """

        unknown_fields = self._model.validate_expression(exprression,None,*args,**kwargs)
        if unknown_fields.__len__() > 0:
            raise (Exception("What is bellow list of fields?:\n" + self.descibe_fields("\t\t", unknown_fields) +
                             " \n Your selected fields now is bellow list: \n" +
                             self.descibe_fields("\t\t\t", self._model.get_fields())))
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
    def find(self,exprression,*args,**kwargs):
        # type: (str,dict) -> dict
        # type: (str,tuple) -> dict
        # type: (str,int) -> dict
        # type: (str,bool) -> dict
        # type: (str,float) -> dict
        # type: (str,datetime) -> dict
        # type: (str,list) -> dict
        """find and get a list of items item with conditional ex: find("Username={0}","admin"),
                    find("Username='admin'"),
                    find("Username=@username",username="admin")
                 """
        unknown_fields = self._model.validate_expression(exprression,None,*args,**kwargs)
        if unknown_fields.__len__() > 0:
            raise (Exception("What is bellow list of fields?:\n" + self.descibe_fields("\t\t", unknown_fields) +
                             " \n Your selected fields now is bellow list: \n" +
                             self.descibe_fields("\t\t\t", self._model.get_fields())))
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
        # type: () -> list
        """
        get list of items from mongodb
        :return:
        """
        ret = self.get_collection().find()
        return list(ret)
    def get_item(self):
        # type : ()-> dict
        """
        Get one item from mongodb without filtering
        :return:
        """
        ret = self.get_collection().find_one()
        return ret
    def where(self,exprression,*params):
        # type: (str,dict) -> COLL
        # type: (str,tuple) -> COLL
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
        self.get_collection()
        if self._entity==None:
            self._entity=ENTITY(self.qr,self,self.name)
        return self._entity
    def aggregate(self):
        """create aggregate before create pipeline"""
        return AGGREGATE(self,self.qr,self.name)
    def insert(self,*args,**kwargs):
        # type: (dict) -> dict
        # type: (tuple) -> dict
        """
        insert item into database
        :param args:
        :param kwargs:
        :return: dict including data has been inserted and error
        """

        ac=self.entity().insert_one(*args,**kwargs)
        ret=ac.commit()
        return ret
    def update(self,data,filter,*args,**kwargs):
        # type: (dict,str,int) -> dict
        # type: (dict,str,bool) -> dict
        # type: (dict,str,datetime) -> dict
        # type: (dict,str,float) -> dict
        # type: (dict,str,dict) -> dict
        # type: (dict,str,tuple) -> dict
        # type: (dict,str,list) -> dict

        """
        Update data example: update({"password":"123"},"username=={0}","admin")
        :param data:dict data will be update
        :param filter:conditional text expression
        :param args:
        :param kwargs:
        :return: dict with data and error
        """
        unknown_fields = self._model.validate_expression(filter,None,*args,**kwargs)
        if unknown_fields.__len__() > 0:
            raise (Exception("What is bellow list of fields?:\n" + self.descibe_fields("\t\t", unknown_fields) +
                             " \n Your selected fields now is bellow list: \n" +
                             self.descibe_fields("\t\t\t", self._model.get_fields())))
        if type(args) is tuple and args.__len__()>0 and kwargs=={}:
            kwargs=args[0]
        ac=self.entity().filter(filter,kwargs)
        ac.update_many(data)
        ret=ac.commit()
        return ret
    def create_unique_index(self,*args,**kwargs):
        """
        Create unique key refer to link : https://docs.mongodb.com/manual/reference/method/db.collection.createIndex/
        :param args:
        :param kwargs:
        :return:
        """
        if type(args) is tuple and args.__len__()>0:
            args=args[0]
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
        # type: (str,int) -> dict
        # type: (str,bool) -> dict
        # type: (str,float) -> dict
        # type: (str,datetime) -> dict
        # type: (str,str) -> dict
        # type: (str,unicode) -> dict
        # type: (str,dict) -> dict
        # type: (str,tuple) -> dict
        # type: (str) -> dict
        """
        Delete data according to filter expression. Example detele("IsInactive=={0},True)
        :param filter:
        :param args:
        :param kwargs:
        :return:
        """
        unknown_fields = self._model.validate_expression(filter,None,*args,**kwargs)
        if unknown_fields.__len__() > 0:
            raise (Exception("What is bellow list of fields?:\n" + self.descibe_fields("\t\t", unknown_fields) +
                             " \n Your selected fields now is bellow list: \n" +
                             self.descibe_fields("\t\t\t", self._model.get_fields())))
        ac=self.entity().filter(filter,*args,**kwargs)
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
    """
    This class is a utility for mongodb aggregation framework. For more detail refer to :https://docs.mongodb.com/manual/aggregation/

    """

    def __init__(self,coll, qr, name):
        # type: (COLL,QR,str) -> AGGREGATE
        """
        Create instance of AGGREGATE
        :param coll: instance of COLL
        :param qr: instance of QR, this param will be use when get data from mongodb
        :param name: collecion name without schema
        """
        self._coll=coll
        self._selected_fields = None
        self.qr = qr
        self.name = name
        self._pipe=[]
    def get_selected_fields(self):
        # type: () -> list
        """
        Get current selected fields of aggregate pipeline
        :return:
        """
        if self._selected_fields==None:
            self._selected_fields=self._coll._model.get_fields()
        return self._selected_fields
    def descibe_fields(self,tabs,fields):
        # type: (str,list) -> str
        """
        Create well form text for list of fields
        :param tabs: indent tab of each field must be a string contains only '\t'
        :param fields: list of fields
        :return: well form text
        """
        _fields = ""
        for x in fields:
            _fields += tabs+ x + "\n"
        return  _fields
    def check_fields(self,field):
        # type: (str) -> bool
        """
        Check a field if it is in list of current selected fields
        :param field:
        :return: if field was found return True else False
        """
        ret=[x for x in self.get_selected_fields() if x==field]
        return ret.__len__()>0

    def project(self,*args,**kwargs):
        # type: (dict) -> AGGREGATE
        # type: (tuple) -> AGGREGATE
        """
        Create project pipeline (refer to :https://docs.mongodb.com/manual/reference/operator/aggregation/project/)
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
            or
            project (
                username=1,
                password=1,
                myConst="titeral(1)",
                total_salary="BasicSalary + MonthlySalary"
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
        _next_step_fields=[]
        for key in kwargs.keys():
            if kwargs[key]==1:
                if not self.check_fields(key):
                    raise (Exception("What is '" + key + "'?:\n" +
                                     " \n Your selected fields now is bellow list: \n" +
                                     self.descibe_fields("\t\t\t", self.get_selected_fields())))
                _project.update({
                    key: 1
                })
                _next_step_fields.append(key)
            else:
                unknown_fields = self._coll._model.validate_expression(kwargs[key],self.get_selected_fields())
                if unknown_fields.__len__()>0:
                    raise (Exception("What is bellow list of fields?:\n"+self.descibe_fields("\t\t",unknown_fields)+
                                     " \n Your selected fields now is bellow list: \n"+
                                     self.descibe_fields("\t\t\t",self.get_selected_fields())))
                _project.update({
                    key: expr.get_calc_expr(kwargs[key],params)
                })
                _next_step_fields.append(key)
        self._selected_fields=_next_step_fields
        self._pipe.append({
            "$project":_project
        })
        return self
    def group(self,_id,selectors,*args,**kwargs):
        # type: (dict,dict) -> AGGREGATE
        # type: (dict,tuple) -> AGGREGATE
        # type: (tuple,dict) -> AGGREGATE
        # type: (tuple,tuple) -> AGGREGATE
        """
        Create a group pipeline for mongodb aggregate (refer to: https://docs.mongodb.com/manual/reference/operator/aggregation/group/)
        Example: group(_id=dict(
                                month="month(MyDate)",
                                day="dayOfMonth(MydDate)",
                                year="year(MyDate)"),
                        selectors=dict(
                                   totalPrice="sum(price*quantity+{0})),
                                   12)

        :param _id:
        :param selectors:
        :param args:
        :param kwargs:
        :return:
        """
        _next_step_fields=[]
        __id={}
        if type(_id) is dict:
            for key in _id.keys():
                unknown_fields = self._coll._model.validate_expression(_id[key], self.get_selected_fields())
                if unknown_fields.__len__()>0:
                    raise (Exception("What is bellow list of fields?:\n"+self.descibe_fields("\t\t",unknown_fields)+
                                     " \n Your selected fields now is bellow list: \n"+
                                     self.descibe_fields("\t\t\t",self.get_selected_fields())))
                _next_step_fields.append("_id")
                _next_step_fields.append("_id."+key)
                __id.update({
                    key:expr.get_calc_expr(_id[key],*args,**kwargs)
                })
        else:
            if not self.check_fields(_id):
                raise (Exception("What is '"+_id+"'?:\n"  +
                                 " \n Your selected fields now is bellow list: \n" +
                                 self.descibe_fields("\t\t\t", self.get_selected_fields())))

            __id="$"+_id
            _next_step_fields.append("_id")
            _next_step_fields.append("_id."+_id)

        _group = {
            "$group": {
                "_id": __id
            }
        }
        if not type(selectors) is dict:
            raise (Exception("'selectors' must be dict type"))


        for key in selectors.keys():
            unknown_fields = self._coll._model.validate_expression(selectors[key], self.get_selected_fields())
            if unknown_fields.__len__() > 0:
                raise (Exception("What is bellow list of fields?:\n" + self.descibe_fields("\t\t", unknown_fields) +
                                 " \n Your selected fields now is bellow list: \n" +
                                 self.descibe_fields("\t\t\t", self.get_selected_fields())))
            _group["$group"].update({
                key:expr.get_calc_expr(selectors[key],*args,**kwargs)
            })
            _next_step_fields.append(key)
        self._selected_fields = _next_step_fields
        self._pipe.append(_group)
        return self
    def skip(self,len):
        # type: (int) ->AGGREGATE
        """
        Skip aggregate
        :param len:
        :return:
        """
        self._pipe.append({
            "$skip":len
        })
        return self
    def limit(self,num):
        # type: (int) ->AGGREGATE
        """
        Limit aggregate
        :param num:
        :return:
        """
        self._pipe.append({
            "$limit": num
        })
        return self
    def unwind(self,field_name):
        # type: (str) -> AGGREGATE
        """
        Unwin aggregate
        :param field_name: the field name for "unwind" without prefix "$"
        :return:
        """
        if self.get_selected_fields().count(field_name)==0:
            msg_detail=""
            for x in self.get_selected_fields():
                msg_detail+=x+"\n"
            raise (Exception("What is '{0}'? \n Your selected fields now are: \n {1}".format(field_name,msg_detail)))
        if field_name[0:1]!="$":
            field_name="$"+field_name
        self._pipe.append({
            "$unwind":{"path":field_name,
                        "preserveNullAndEmptyArrays":True
                    }
        })
        return self
    def match(self,expression, *args,**kwargs):
        # type: (str,int) -> AGGREGATE
        # type: (str,bool) -> AGGREGATE
        # type: (str,datetime) -> AGGREGATE
        # type: (str,str) -> AGGREGATE
        # type: (str,unicode) -> AGGREGATE
        # type: (str,float) -> AGGREGATE
        # type: (str,dict) -> AGGREGATE
        # type: (str,tuple) -> AGGREGATE
        # type: (str,list) -> AGGREGATE

        """
        Mathc aggregate Example:
            macth("userame=={0} and is_active=={1}",'admin',True)
        :param expression:
        :param args:
        :param kwargs:
        :return:
        """
        """Beware! You could not use any Aggregation Pipeline Operators, just use this function with Field Logic comparasion such as:
        and,or, contains,==,!=,>,<,..
        """
        unknown_fields=self._coll._model.validate_expression(expression,self.get_selected_fields(), *args,**kwargs)
        if unknown_fields.__len__() > 0:
            err_msg = ""
            for x in unknown_fields:
                err_msg += x + "\n"
            err_msg_fields = ""
            for x in self.get_selected_fields():
                err_msg_fields += x + "\n"
            raise (Exception(
                "What is bellow list of fields?:\n" + err_msg + " \n Your selected fields now is bellow list: \n" + err_msg_fields))
        by_params=False
        if args==():
            args=kwargs
            by_params=True

        if type(expression) is dict:
            self._pipe.append({
                "$match":expression
            })
            return self
        if type(expression) in [str,unicode]:
            import helpers
            self._pipe.append({
                "$match": (lambda :  helpers.filter(expression, args)._pipe if by_params else helpers.filter(expression, *args,**kwargs)._pipe)()
            })
            return self

        pass
    def lookup(self,
               source=None,
               local_field=None,
               foreign_field=None,
               alias=None,
               *args,**kwargs):
        # type: (str,str,str,str) -> AGGREGATE
        # type: (COLL,str,str,str) -> AGGREGATE
        """
        Create lookup aggregate
        :param source: where this collection will lookup for mongodb that is 'from'
        :param local_field:which is the field in this collection serve for lookup? for mongodb that is 'localField'
        :param foreign_field:which is the field from source collection serve for lookup? for mongodb that is 'foreignField'
        :param alias:The alias after lookup for mongdb that is 'as'
        :param args:
        :param kwargs:
        :return:
        """
        if self.get_selected_fields().count(local_field)==0:
            msm_details=""
            for x in self.get_selected_fields():
                msm_details+=x+"\n"
            raise (Exception("What is '{0}'?, Your selected fields are:\n {1}".format(local_field,msm_details)))


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
        source_model=None
        if isinstance(source,COLL):
            source_model =source._model
        else:
            source_model = get_model(source)

        self._selected_fields = self.get_selected_fields()
        self._selected_fields.append(alias)
        if source_model.get_fields().count(foreign_field)==0:
            msm_details=""
            for x in source_model.get_fields():
                msm_details+=x+"\n"
            raise (Exception("What is '{0}'?\n '{0}'  is not in '{1}'.\n All fields of '{1}' are bellow:\n {2}".format(foreign_field,source,msm_details)))
        for x in source_model.get_fields():
            self._selected_fields.append(alias+"."+x)
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
        if args==() and kwargs=={}:
            raise (Exception("It look like you forgot set sort fields\nHow to sort?\n"
                             ".sort(\n"
                             "\tfield name=1 or -1\n,"
                             "\t..\n"
                             "\tfield name n=1 or -1"))
        _sort={

        }
        for key in kwargs.keys():
            if self.get_selected_fields().count(key)==0:
                msg_detail=""
                for x in self.get_selected_fields():
                    msg_detail+=x+"\n"
                raise (Exception("\n"
                                 "What is '{0}'?\n"
                                 "Your selected fields are:\n"
                                 "{1}".format(key,msg_detail)))
        _sort = (lambda x, y: y if y != {} else x[0])(args, kwargs)
        self._pipe.append({
            "$sort":_sort
        })
        return self
    def count(self,alias):
        """
        Create count aggregate pipeline
        :param alias: Alias field will hold count value
        :return:
        """
        self._pipe.append({
            "$count":alias
        })
        return self
    def get_item(self):
        """
        Get one item from mongdb
        :return:
        """
        ret=self.get_list()
        if ret.__len__()==0:
            return None
        else:
            return ret[0]
    def get_all_documents(self):
        # type: () -> list
        """
        get all items from mongodb
        Caution: this method will return what is collection store. For example the collection maybe store different schema in each doc
        :return:
        """
        coll = self.qr.db.get_collection(self.name).with_options(codec_options=self.qr._codec_options)
        coll_ret = coll.aggregate(self._pipe)
        ret=list(coll.aggregate(self._pipe))
        return ret
    def get_list(self):
        # type: () -> list
        """
        Get list of item in mongodb
        Caution: this method will return the same schema for each item even the collection contains different schema for each item
        :return:
        """
        # try:
        #     return self.qr.db.get_collection(self.name).aggregate(self._pipe,explain=False)["cursor"]["firstBatch"]
        # except Exception as ex:
        #     return list(self.qr.db.get_collection(self.name).aggregate(self._pipe))
        coll=self.qr.db.get_collection(self.name).with_options(codec_options=self.qr._codec_options)
        coll_ret=coll.aggregate(self._pipe)

        ret=[]
        for doc in coll_ret:
            for key in self.get_selected_fields():
                if not doc.has_key(key):
                    doc.update({
                        key:None
                    })
            ret.append(doc)

        # ret=list(coll.aggregate(self._pipe))
        self._pipe=[]
        self._selected_fields=[]
        return ret
    def get_page(self,page_index,page_size):
        # type: (int,int) -> dict
        """
        get page of item according to page_index and page_size
        Caution: this method will return the same schema for each item even the collection contains different schema for each item
        :param page_index:
        :param page_size:
        :return: dict including: page_size, page_index, total_items, items
        """
        _tmp_pipe = [x for x in self._pipe]
        _count_pipe=[x for x in self._pipe if self._pipe.index(x)<self._pipe.__len__() and x.keys()[0]!="$sort"]
        self._pipe = _count_pipe
        _sel_fields=self._selected_fields
        total_items=self.count("total_items").get_item()
        self._selected_fields=_sel_fields
        self._pipe=_tmp_pipe
        items=self.skip(page_index*page_size).limit(page_size).get_list()
        return dict(
            page_size=page_size,
            page_index=page_index,
            total_items= (lambda x: x["total_items"] if x != None else 0) (total_items),
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
