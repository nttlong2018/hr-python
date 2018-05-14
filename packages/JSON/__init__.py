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

class json_serilizer():
    time_offset_minutes=None
    def __init__(self,time_offset_minutes):
        self.time_offset_minutes=time_offset_minutes
    def json_serial(self,obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime, date)):
            return (obj-timedelta(minutes=self.time_offset_minutes)).isoformat()
        elif type(obj) is ObjectId:
            return obj.__str__()
        elif hasattr(obj, "__dict__"):
            return obj.__dict__
        elif type(obj) is sqlalchemy.orm.state.InstanceState:
            return None
        return obj.__str__()



def datetime_parser(dct,time_offset_minutes):

    if type(dct) in [unicode,str]:
        if datetime_format_regex.match(dct):
            return datetime.strptime(dict, datetime_format)
        elif datetime_format_regex_from_javascript.match(dct):
            return datetime.strptime(dict, datetime_format_javascript)
        else:
            return dct
    elif type(dct) is list:
        return [datetime_parser(x,time_offset_minutes) for x in dct]
    elif type(dct) is dict:
        for k, v in dct.items():
            if (isinstance(v, str) or type(v) is unicode) and datetime_format_regex.match(v):
                dct[k] = datetime.strptime(v, datetime_format)
            elif (isinstance(v, str) or type(v) is unicode) and datetime_format_regex_from_javascript.match(v):
                dct[k] = datetime.strptime(v, datetime_format_javascript)-timedelta(minutes=time_offset_minutes)
            else:
                dct[k]=datetime_parser(v,time_offset_minutes)
    else:
        return dct


    return dct

def to_json(ret,time_offset_minutes):
    serilizer= json_serilizer(time_offset_minutes)
    if ret==None:
        return json.dumps(ret)
    if type(ret) is list:
        if ret.__len__()==0:
            ret_data="[]"
        else:
            if type(ret[0]) is dict:
                ret_data=json.dumps(ret,default=serilizer.json_serial)
            else:
                ret_data=json.dumps([r.__dict__ for r in ret],default=serilizer.json_serial)
    else:
        if ret==None:
            ret_data=None
        else:
            if type(ret) is dict:
                ret_data = json.dumps(ret, default=serilizer.json_serial)
            else:
                ret_data = json.dumps(ret.__dict__, default=serilizer.json_serial)
    return ret_data
def from_json(data,time_offset_minutes):
    ret_data=json.loads(data)
    ret_data=datetime_parser(ret_data,time_offset_minutes)

    return ret_data