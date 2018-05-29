from . import *
from . import expr
from . import validators
from filter_expression import filter_expression
from  aggregate_expression import aggregate_expression
import aggregate_validators as query_validator
import validators

_model_caching_={}
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
        if data[key].data_type=="list":
            if data[key].details!=None:
                ret_fields=unwind_data(data[key].details,key)
                for fx in ret_fields.keys():
                    ret.update({
                        fx:ret_fields[fx]
                    })

    return ret
def define_model(_name,keys=None,*args,**kwargs):
    name=_name
    if _model_caching_.has_key(name):
        return _model_caching_[name]
    params=kwargs
    if type(args) is tuple and args.__len__()>0:
        params=args[0]
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
        name:query_validator.validator(name,validate_dict)
    })
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