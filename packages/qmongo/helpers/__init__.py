from . import *
from . import expr
from . import validators
from filter_expression import filter_expression
from  aggregate_expression import aggregate_expression
import aggregate_validators as query_validator
import validators
from model_events import model_event
_model_caching_={}
_model_index_={}
_model_caching_params={}
_model_events={}
class data_field():
    data_type="text"
    is_require = False
    details=None
    def __init__(self,data_type="text",is_require=False,detail=None):
        self.is_require=is_require
        self.data_type=data_type
        self.details=detail

def filter(expression,*args,**kwargs):
    ret = filter_expression(expression,*args,**kwargs)
    return ret
def aggregate():
    ret=aggregate_expression()
    return ret
def find(*args,**kwargs):
    pass
def unwind_data(data,prefix=None):
    ret={}
    for key in data.keys():
        if type(data[key]) is dict:
            if prefix!=None:
                _prefix=prefix+"."+key
            else:
                _prefix = key
            ret_keys=unwind_data(data[key],_prefix)
            ret.update(ret_keys)
        elif isinstance(data[key],data_field):
            if data[key].data_type == "list":
                if prefix!=None:
                    ret.update({
                        prefix + "." + key: {
                            "require": data[key].is_require,
                            "type":data[key].data_type,
                            "details":data[key].details
                        }
                    })
                else:
                    ret.update({
                        key: {
                            "require": data[key].is_require,
                            "type":data[key].data_type,
                            "details":data[key].details
                        }
                    })
                if data[key].details != None and not type(data[key].details) is str:
                    ret_fields = unwind_data(data[key].details, key)
                    for fx in ret_fields.keys():
                        if prefix!=None:
                            ret.update({
                                prefix + "."+fx:  ret_fields[fx]
                            })
                        else:
                            ret.update({
                                fx: ret_fields[fx]
                            })
            else:
                if prefix!=None:
                    ret.update(
                        {
                            prefix + "." + key:{
                                "require":data[key].is_require,
                                "type":data[key].data_type
                            }
                        }
                    )
                else:
                    ret.update(
                        {
                            key: {
                                "require": data[key].is_require,
                                "type": data[key].data_type
                            }
                        }
                    )


    return ret
def define_model(_name,keys=None,*args,**kwargs):
    global _model_index_
    global _model_caching_params
    name=_name
    if _model_caching_.has_key(name):
        return _model_caching_[name]
    params=kwargs
    if type(args) is tuple and args.__len__()>0:
        params=args[0]
    _model_caching_params.update({
        name:params
    })
    list_of_fields=unwind_data(params)
    validators.set_require_fields(name,[
        x for x in list_of_fields.keys() if list_of_fields[x]["require"]
    ])
    validate_dict={}
    for x in list_of_fields.keys():
        validate_dict.update(
            {
                x:list_of_fields[x]["type"]
            }
        )
    validators.create_model(name,validate_dict)
    _model_caching_.update({
        name:query_validator.validator(name,validate_dict),

    })
    _model_index_.update({
        name:{
                "keys":keys,
                "has_created":False
            }
        })
    return _model_caching_[name]
def extent_model(name,from_name,keys=None,*args,**kwargs):
    source_model=get_model(from_name)
    source_model_params=_model_caching_params[from_name]
    if type(args) is tuple and args.__len__()>0:
        for key in source_model_params.keys():
            args[0].update({
                key:source_model_params[key]
            })
    if keys==None:
        keys=[]
    keys.extend(_model_index_[from_name]["keys"])
    define_model(name,keys,*args,**kwargs)
    from_event=events(from_name)

    if from_event!=None:
        model_event = events(name)
        for f in from_event._on_before_insert:
            model_event.on_before_insert(f)
        for f in from_event._on_after_insert:
            model_event.on_after_insert(f)
        for f in from_event._on_before_update:
            model_event.on_before_update(f)
        for f in from_event._on_after_update:
            model_event.on_after_update(f)




    model=define_model(name,keys,*args,**kwargs)

def get_keys_of_model(name):
    return _model_index_[name]
def get_model(name):
    if not _model_caching_.has_key(name):
        raise (Exception("It look like you forgot create model for '{0}'\n"
                         "How to define a model?\n"
                         "from quicky import helpers\n"
                         "helpers.define_model(\n"
                         "\tYour model name here,\n"
                         "\tlist of key fields here,\n"
                         "\tfield name =helpers.create_field(""text|bool|numeric|date|list"",require or not)\n"
                         "\tor field name =dict(neasted field),..,\n"
                         "\tfield name n =helpers.create_field(""text|bool|numeric|date|list"",require or not))".format(name)))
    return _model_caching_[name]

def create_field(data_type="text",is_require=False,detail=None):
    return data_field(data_type,is_require,detail)
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
def events(name):
    if _model_events.has_key(name):
        return _model_events[name]
    else:
        _model_events.update({
            name:model_event()
        })
        return _model_events[name]
