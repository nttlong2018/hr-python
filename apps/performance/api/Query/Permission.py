from .. import models
from .. import common
from .. import functionlist

def get_list_permission_by_role(role_code):
    db = common.get_db_context()
    ret = db.system_js.getListPermission(common.get_current_schema(), "PERF", role_code)
    return ret

def get_list_edit_permission(role_code):
    collection = common.get_collection('AD_Roles')
    ret = collection.aggregate([
        {"$match":{"role_code":role_code}},
        {"$unwind":{"path":"$permission", "includeArrayIndex": "arrayIndex", "preserveNullAndEmptyArrays":False}},
        {"$project":{
            "role_code":1,
            "function_id":"$permission.function_id",
            "read":"$permission.read",
            "create":"$permission.create",
            "write":"$permission.write",
            "delete":"$permission.delete",
            "export":"$permission.export",
            "import":"$permission.import",
            "copy":"$permission.copy",
            "attach":"$permission.attach",
            "download":"$permission.download"
            }},
        {"$lookup":{"from":common.get_collection_name_with_schema("SYS_FunctionList"), "localField":'function_id', "foreignField":'function_id', "as":'fnl'}},
        {"$unwind":{"path":"$fnl", "preserveNullAndEmptyArrays":False}},
        {"$project":{
            "function_id":1,
            "role_code":1,
            "default_name":"$fnl.default_name",
            "parent_id":"$fnl.parent_id",
            "read":1,
            "create":1,
            "write":1,
            "delete":1,
            "export":1,
            "import":1,
            "copy":1,
            "attach":1,
            "download":1
            }}
        ])
    list_per = list(ret)

    list_fnl = functionlist.get_list({})

    arr_per_func_id = [x["function_id"]for x in list_per]

    result = []

    for x in list_fnl:
        if x['function_id'] in arr_per_func_id:
            result.append(
                [ele for ele in list_per if ele['function_id'] == x['function_id']][0]
                )
        else:
            result.append({
            "function_id":x['function_id'],
            "role_code":role_code,
            "default_name":x['default_name'],
            "parent_id":x['parent_id'],
            "read":False,
            "create":False,
            "write":False,
            "delete":False,
            "export":False,
            "import":False,
            "copy":False,
            "attach":False,
            "download":False
            })

    return result

def remove_permission(role_code, func_id):
    collection  =  common.get_collection('AD_Roles')
    ret = collection.update(
                        {
                            "role_code": role_code
                        },
                        {
                            '$pull':{"permission" :{ "function_id": {'$in': func_id}}}
                        }, 
                        True
                        )

    return ret

def edit_permission(role_code, lst_per):
    collection  =  common.get_collection('AD_Roles')
    ret = collection.update(
        {
            "role_code": role_code,
        },
        {
            "$set": {
                'permission': lst_per
                }
        })
    return ret