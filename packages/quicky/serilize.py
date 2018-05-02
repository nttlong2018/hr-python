from bson.objectid import ObjectId
from datetime import datetime,date
import sqlalchemy
import json
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif type(obj) is ObjectId:
        return obj.__str__()
    elif obj.__class__.__class__ is sqlalchemy.ext.declarative.api.DeclarativeMeta:
        return obj.__dict__
    elif type(obj) is sqlalchemy.orm.state.InstanceState:
        return  None
    return obj.__str__()
def to_json(ret):
    if type(ret) is list:
        if ret.__len__()==0:
            ret_data="[]"
        else:
            if type(ret[0]) is dict:
                ret_data=json.dumps(ret,default=json_serial)
            else:
                ret_data=json.dumps([r.__dict__ for r in ret],default=json_serial)
    else:
        if ret==None:
            ret_data=None
        else:
            if type(ret) is dict:
                ret_data = json.dumps(ret, default=json_serial)
            else:
                ret_data = json.dumps(ret.__dict__, default=json_serial)
    return ret_data
