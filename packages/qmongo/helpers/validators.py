import threading
import datetime
global lock
lock=threading.Lock()
global _model_cache_
_model_cache_={
    "require_fields":{},
    "type_fields":{}
}
def get_value_by_path(path,data):
    if data.has_key(path):
        return data[path]
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
def validate_require_data(name,data,partial=False):
    if not partial:
        ret=[]
        for key in _model_cache_["require_fields"].get(name,[]):
            val=get_value_by_path(key,data)
            if val==None:
                ret.append(key)
        return ret
    else:
        if data=={}:
            return []
        path=""
        val=data
        ret=[]
        for key in data.keys():
            if key[0:1]!="$":
                find_fields = [x for x in _model_cache_["require_fields"].get(name, []) if x[0:key.__len__()] == key]
                if find_fields.__len__() > 0:
                    val = get_value_by_path(find_fields[0], data)
                    if val == None:
                        ret.append(find_fields[0])

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
def create_model(name,*args,**kwargs):
    params=kwargs
    if type(args) is tuple and args.__len__()>0:
        params=args[0]
    if not _model_cache_["type_fields"].has_key(name):
        lock.acquire()
        try:
            _model_cache_["type_fields"].update({
                name:params
            })
            lock.release()
        except Exception as ex:
            lock.release()
            raise ex
def validate_type_of_data(name,data):
    ret = []
    for key in _model_cache_["type_fields"].get(name, {}):
        val = get_value_by_path(key, data)

        if val != None:
            type_of_value = _model_cache_["type_fields"][name][key]
            if type_of_value == "text" and type(val) not in [str, unicode]:
                ret.append(key)
            if type_of_value == "numeric" and type(val) not in [
                type(int),
                type(float),
                type(long),
                type(complex)
            ]:
                ret.append(key)
            if type_of_value == "bool" and type(val) != bool:
                ret.append(key)
            if type_of_value == "date" and type(val) != datetime.datetime:
                ret.append(key)
            if type_of_value == "list" and type(val) != list:
                ret.append(key)

    return ret
