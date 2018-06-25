from django.http import HttpResponse
import quicky
from datetime import datetime;
import uuid
from performance.lv_core import db 


def generate_token(args):
    "Generate export token"
    paramerter = args['data'].get('params', None)
    path = args['data'].get('path', None)
    function_id = args['data'].get('function', "_")

    ret_link = ""
    if not (paramerter is None or path is None):
        req_id = str(uuid.uuid4())
        request_token = db.get_collection("HCSSYS_RequestToken").insert_one({
                '_id': req_id,
                'function_id': function_id,
                'parameter': paramerter,
                'is_expired': False,
                'created_on': datetime.utcnow(),
                'created_by': args["user"].username,
                'modified_on': None,
                'modified_by': None
            })
        ret_link = path + "?tk=" + req_id

    return {'link' : ret_link }

def get_parameter(request, token):
    "Get parameter from export token"
    ret_data = list(db.get_collection('HCSSYS_RequestToken').aggregate([{
        '$match': {
            '_id': token, 
            'created_by':  request.user.username
        }
    }]))

    msg_not_exists = "Link does not exist!"
    msg_expired = "Link has expired!"
    if len(ret_data)>0:
        if(ret_data[0]["is_expired"]):
            return {
                'error': msg_expired
            }
        else:
            ret_data[0]["is_expired"] = True
            db.get_collection("HCSSYS_RequestToken").update_one(
                {'_id': token }, 
                { '$set' : {
                        'is_expired': True,
                        'modified_on': datetime.utcnow(),
                        'modified_by': request.user.username
                    }
                }
            )
            return { 
                'data' : ret_data[0]["parameter"]
            }
    return {
        'error': msg_not_exists  
    }