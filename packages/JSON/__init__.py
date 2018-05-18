from bson.objectid import ObjectId
from datetime import datetime,date
import sqlalchemy
import json
import re
from datetime import datetime
from datetime import timedelta
datetime_format = "%Y-%m-%dT%H:%M:%S.%f"
datetime_format_javascript = "%Y-%m-%dT%H:%M:%S.%fZ"
datetime_format_regex = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}$')
datetime_format_regex_from_javascript = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z$')

def json_serilize_dict(obj):
    ret={}
    for x in obj.keys():
        if type(obj[x]) is dict:
            ret.update({
                x:json_serial(obj[x])
            })
        elif not type(obj[x]) is sqlalchemy.orm.state.InstanceState:
            ret.update({
                x:obj[x]
            })
    return ret


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return (obj).isoformat()
    elif type(obj) is ObjectId:
        return obj.__str__()
    elif hasattr(obj, "__dict__"):
        return json_serilize_dict(obj.__dict__)
    elif type(obj) is sqlalchemy.orm.state.InstanceState:
        return None
    elif callable(obj):
        val=obj()
        return json_serial(val)

    return obj.__str__()
def datetime_parser(dct):

    if type(dct) in [unicode,str]:
        if datetime_format_regex.match(dct):
            return datetime.strptime(dict, datetime_format)
        elif datetime_format_regex_from_javascript.match(dct):
            return datetime.strptime(dict, datetime_format_javascript)
        else:
            return dct
    elif type(dct) is list:
        return [datetime_parser(x) for x in dct]
    elif type(dct) is dict:
        for k, v in dct.items():
            if (isinstance(v, str) or type(v) is unicode) and datetime_format_regex.match(v):
                dct[k] = datetime.strptime(v, datetime_format)
            elif (isinstance(v, str) or type(v) is unicode) and datetime_format_regex_from_javascript.match(v):
                dct[k] = datetime.strptime(v, datetime_format_javascript)
            else:
                dct[k]=datetime_parser(v)
    else:
        return dct


    return dct

def to_json(ret):

    if ret==None:
        return json.dumps(ret)
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
def from_json(data):
    ret_data=json.loads(data)
    ret_data=datetime_parser(ret_data)

    return ret_data