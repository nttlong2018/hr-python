import json
import importlib
import serilize
class caller_param():
    request=None
    user=None
    view=None
    data=None
    language=""

    app=""  #Current application
    def __init__(self,_request):
        self.request=_request


def call(request):
    ret_data=None
    data=json.loads(request.body)
    if not data.has_key("path"):
        raise (Exception("'path' was not found in request.body"))
    path=data["path"]
    items=path.split("/");
    if items.__len__()<2:
        raise (Exception("'path' in request.body is invalid"))
    mdl=None
    fn=None
    try:
        mdl=importlib.import_module(items[0])
    except Exception as ex:
        raise (ex)
    if mdl==None:
        raise (Exception("'{0}' was not found".format(items[0])))
    if not hasattr(mdl,items[1]):
        raise (Exception("'{0}' was not found in '{1}'".format(items[1],items[0])))
    else:
        fn=getattr(mdl,items[1])
        if not callable(fn):
            raise (Exception("'{0}' in '{1}' is not a function".format(items[1], items[0])))

    param=caller_param(request)
    param.language=request.LANGUAGE_CODE
    param.user=request.user
    param.app=request.app
    if data.has_key("view"):
        param.view=data["view"]
    if data.has_key("data"):
        param.data=data["data"]
    if fn!=None:
        ret_data=fn(param)
    ret_json=serilize.to_json(ret_data)
    return ret_json