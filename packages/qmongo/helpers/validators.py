import threading
global lock
lock=threading.Lock()
global _model_cache_
_model_cache_={
    "require_fields":{}
}
def get_value_by_path(path,data):
    items=path.split(".")
    if items.__len__()==1:
        return data.get(items[0],None)
    else:
        val=data
        for x in items:
            if val==None:
                return None
            else:
                val=val.get(x,None)
        return val

def validate_require_data(name,data):
    ret=[]
    for key in _model_cache_["require_fields"].get(name,[]):
        val=get_value_by_path(key,data)
        if val==None:
            ret.append(key)
    return ret
def set_require_fields(name,*args,**kwargs):
        if _model_cache_["require_fields"].has_key(name):
            pass
        else:
            lock.acquire()
            try:
                params = kwargs
                if type(args) is tuple and args.__len__() > 0:
                    params = args[0]
                _model_cache_["require_fields"].update({
                    name:params
                })
                lock.release()

            except Exception as ex:
                lock.release()
                raise(ex)
