import re
from  membership import models

from pymongo import MongoClient
import hashlib, uuid
import  datetime
from . import dbModels
_mongo_membership_connection_string=""
_mongo_membership_connection_client=None
_mongo_membership_database=None
_mongo_membership_config=None
_mongo_membership_session_cach={}
_is_use_elastic_search_=False
_elasticsearch_servers_=None
_ES_=None
def get_db():
    "get a sigleton instance of database"
    global _mongo_membership_database
    if(_mongo_membership_database==None):
        _config=_mongo_membership_config
        _client = MongoClient(
            _config.get("host"),_config.get("port")
        )
        _mongo_membership_database = _client.get_database(_config.get("name"))
        if(_config.has_key("user") and _config.get("user")!=""):
            _mongo_membership_database.authenticate(_config.get("user"),_config.get("password"))

    return _mongo_membership_database
def set_config(config):
    global _mongo_membership_config
    global _is_use_elastic_search_
    _mongo_membership_config=config
    if _mongo_membership_config.has_key("elasticsearch"):
        _is_use_elastic_search_=True
        _elasticsearch_servers_=_mongo_membership_config["elasticsearch"]
        from datetime import datetime
        from elasticsearch import Elasticsearch
        global _ES_
        if _ES_ == None:
            _ES_ = Elasticsearch(_elasticsearch_servers_,
                                 # sniff before doing anything
                                 sniff_on_start=True,
                                 # refresh nodes after a node fails to respond
                                 sniff_on_connection_fail=True,
                                 # and also every 60 seconds
                                 sniffer_timeout=60)


def get_connection_string():
    return _mongo_membership_connection_string
def set_connection_string(strCnn):
    global _mongo_membership_connection_string
    _mongo_membership_connection_string=strCnn
def create_user(username,password,email):
    count_user_by_username=get_db().get_collection("sys_users").find_one({
        "Username":re.compile("^"+username+"$",re.IGNORECASE)
    })
    if(count_user_by_username!=None):
        _exception=models.exception()
        _exception.message="user is already"
        _exception.types=models.error_types.DUPLICATE
        _exception.fields=["username"]
        raise _exception
    if email!=None:
        count_user_by_email=get_db().get_collection("sys_users").find_one({
            "Email":re.compile("^"+email+"$",re.IGNORECASE)
            })
        if count_user_by_email!=None:
            _exception = models.exception()
            _exception.message = "email is already"
            _exception.types = models.error_types.DUPLICATE
            _exception.fields = ["email"]
            raise _exception
    _user=dbModels.users()
    _user.Username=username
    _user.Email = email
    _user.PasswordSalt= uuid.uuid4().hex
    _user.Password=hashlib.sha512("uid="+username.lower()+";pwd="+password+_user.PasswordSalt).hexdigest()
    ret_db=get_db().get_collection("sys_users").insert_one(_user.__dict__)

    ret_user=models.user()
    ret_user=_user.tranfer_data_to(ret_user)
    ret_user.userId=ret_db.inserted_id.__str__()
    if not _ES_== None:
        res = _ES_.index(index="membership_user",
                         doc_type='tweet',
                         body=ret_user.__dict__,
                         id=ret_user.userId)
    return ret_user
def validate_account(username,password):
    user=get_db().get_collection("sys_users").find_one({
        "Username":re.compile("^"+username+"$",re.IGNORECASE),
        "IsActive":True
    })
    if user==None:
        exception=models.exception()
        exception.message="User was not found"
        exception.types=models.error_types.NOTFOUND
        raise  exception
    salt=user["PasswordSalt"]
    pwd=user["Password"]
    hash_pwd=hashlib.sha512("uid="+username.lower()+";pwd="+password+salt).hexdigest()
    if hash_pwd!=pwd:

        get_db().get_collection("sys_users").update_one({
            "Username": re.compile("^" + username + "$", re.IGNORECASE)
        },{
            "$set":{
                "LatestLoginFailOn":datetime.datetime.now(),
                "LatestLoginFailOnUCT": datetime.datetime.utcnow(),
            },
            "$inc":{
                "TotalLoginFail":1
            },
            "$push":{
                "LoginFailTimeList":{
                    "Time":datetime.datetime.now(),
                    "UTCTime":datetime.datetime.utcnow()
                }
            }
        })

        exception = models.exception()
        exception.message = "Usernam or password is incorrect"
        exception.types = models.error_types.INVALID
        exception.fields=["username","password"]
        raise exception
    ret_user=models.user()
    ret_user=dbModels.load_data_from_dict(ret_user,user)
    ret_user.userId=user["_id"]
    return  ret_user
def sign_in(username,session_id,language_code):
    get_db().get_collection("sys_logins").update_many({
        "SessionId":session_id
    },{
        "$set":{
            "IsLogout":True,
            "LogoutOn":datetime.datetime.now(),
            "LogoutOnUTC":datetime.datetime.utcnow()
        }
    })
    user=get_db().get_collection("sys_users").find_one({
        "Username":re.compile("^"+username+"$",re.IGNORECASE)
    })
    if(user==None):
        exception=models.exception()
        exception.message="User was not found"
        exception.types=models.error_types.NOTFOUND
        raise  exception
    signin={
        "SessionId":session_id,
        "Username":username,
        "UserId":user.get("_id").__str__(),
        "SiginOn":datetime.datetime.now(),
        "SiginOnUTC":datetime.datetime.utcnow(),
        "Language":language_code,
        "IsLogOut":False
    }
    ret_db=get_db().get_collection("sys_logins").insert_one(signin)
    ret=models.sigin_info()
    ret.userId=user.get("_id").__str__()
    ret.token=ret_db.inserted_id.__str__()
    ret.siginOn=signin.get("SiginOn")
    ret.siginOnUTC = signin.get("SiginOnUTC")
    ret.language = signin.get("Language")
    ret.user = models.user()
    ret.user=dbModels.load_data_from_dict(ret.user,user)
    ret.user.userId=ret.userId
    get_db().get_collection("sys_users").update_one({
        "Username": re.compile("^" + username + "$", re.IGNORECASE)
    },{
        "$set":{
            "LatestLoginOn":datetime.datetime.now(),
            "LatestLoginOnUTC":datetime.datetime.utcnow()
        },
        "$inc":{
            "TotalLogin":1
        },
        "$push":{
            "LoginTimeList":{
                "Time":datetime.datetime.now(),
                "UTCTime":datetime.datetime.utcnow()
            }
        }
    })
    return  ret;
def validate_session(session_id):
    global _mongo_membership_session_cach
    if session_id==None:
        return None
    if _mongo_membership_session_cach.has_key(session_id):
        return _mongo_membership_session_cach[session_id]
    login=get_db().get_collection("sys_logins").find_one({
        "SessionId":session_id,
        "IsLogOut":False
    })
    if login==None:
        return None
    user=get_db().get_collection("sys_users").find_one({
        "Username":re.compile("^"+login["Username"]+"$",re.IGNORECASE),
        "IsActive":True
    })
    if user==None:
        return  None
    ret=models.sigin_info()
    ret.user=models.user()
    ret.user=dbModels.load_data_from_dict(ret.user,user)
    ret.user.userId=user["_id"].__str__()
    ret.siginOn=login["SiginOn"]
    ret.siginOnUTC = login["SiginOnUTC"]
    ret.token = login["_id"].__str__()
    ret.userId = user["_id"].__str__()
    ret.language=login["Language"]
    _mongo_membership_session_cach[session_id]=ret
    return  _mongo_membership_session_cach[session_id]
def active_user(username):
    ret=get_db().get_collection("sys_users").update_one({
        "Username":re.compile("^"+username+"$",re.IGNORECASE)
    },{
        "$set":{
            "IsActive":True,
            "ActivationOnUTC":datetime.datetime.utcnow(),
            "ActivationOn": datetime.datetime.now()

        },
        "$inc":{"ActivationCount":1},
        "$push": {
            "ActivationTimeList": {
                "Time": datetime.datetime.now(),
                "UTCTime": datetime.datetime.utcnow()
            }
        }

    })
    return True
def get_user(username):
    ret_db=get_db().get_collection("sys_users").find_one({
        "Username": re.compile("^" + username + "$", re.IGNORECASE)
    })
    if ret_db==None:
        return  None
    ret=models.user()
    dbModels.load_data_from_dict(ret,ret_db)
    ret.userId=ret_db["_id"].__str__()

    return  ret

def sign_out(session_id):
    login = get_db().get_collection("sys_logins").update_many({
        "SessionId": session_id
    },{
        "$set":{
            "IsLogOut":True,
            "SigoutOn":datetime.datetime.now(),
            "SigoutOnUTC": datetime.datetime.utcnow(),
        },
        "$push":{
            "SignoutTimeList":{
                "Time":datetime.datetime.now(),
                "UTCTime":datetime.datetime.utcnow()
            }
        }
    })
    if _mongo_membership_session_cach.has_key(session_id):
        _mongo_membership_session_cach.__delitem__(session_id)
def change_password(username,password):
    PasswordSalt = uuid.uuid4().hex
    Password = hashlib.sha512("uid=" + username.lower() + ";pwd=" + password + PasswordSalt).hexdigest()
    get_db().get_collection("sys_users").update_one({
        "Username":re.compile("^"+username+"$",re.IGNORECASE)
    },{
        "$set":{
            "PasswordSalt":PasswordSalt,
            "Password":Password,
            "LatestChangePasswordOn":datetime.datetime.now(),
            "LatestChangePasswordOnUTC": datetime.datetime.utcnow()
        },
        "$inc":{
            "ChangePasswordCount":1
        },
        "$push":{
            "ChangePasswordTimeList":{
                "Time":datetime.datetime.now(),
                "UTCTime":datetime.datetime.utcnow()
            }
        }
    })
def find(search_text,page_index,page_size):
    if  _is_use_elastic_search_:
        res = _ES_.search(index="membership_user_index",
                          doc_type="tweet",
                          body={"query": {"match": {"content": search_text}},
                                "from":page_size*page_index,
                                "size":page_size
                                })
        ret={
            "pager":{},
            "items":[]
        }
        ret_items=[]
        for item in res["hist"]["hits"]:
            ret_items.append(ret["hits"]["hits"]["_source"])
        ret.update({
            "items":ret_items
        })
        ret.update({
            "pager":{
                "index":page_index,
                "size":page_size,
                "total":res["hits"]["total"]
            }
        })
        return  ret
    else:

        _match={
            "$or":[
                    {"Username":{
                        "$regex":r".*"+search_text+r"*."
                    }},
                    {"Email":{
                        "$regex":r".*"+search_text+r"*."
                    }},
                    {
                        "DisplayName":{
                            "$regex":r".*"+search_text+r"*."
                        }
                    },
                    {
                        "Description": {
                            "$regex": r".*" + search_text + r"*."
                        }
                    }

                ]
        }
        total_items = get_db().get_collection("sys_users").aggregate([
            _match,{
                "$count":"$_id"
            }
        ])

        items=get_db().aggregate([
            _match,{
                "$skip":page_size*page_index
            },{
                "$limit":page_size
            }
        ])
        return {
            "items":items,
            "pager":{
                "size":page_size,
                "index":page_index,
                "total":total_items
            }
        }
def update_user(usr):
    user_doc=dbModels.users()
    user_doc=dbModels.load_data_from_dict(user_doc,usr.__dict__)
    updater={
        "Description":usr.description,
        "Email":usr.email,
        "IsSysAdmin":usr.isSysAdmin,
        "DisplayName":usr.displayName
    }

    get_db().get_collection("sys_users").update_one({
        "Username":re.compile("^"+usr.username+"$",re.IGNORECASE)
    },{
        "$set":updater
    })
    if _ES_ !=None:
        # _ES_.bulk(body=someBody, request_timeout=30)
        res = _ES_.update(index="membership_user",
                         doc_type='tweet',
                         body={"doc":{}},
                         id=usr.userId)














