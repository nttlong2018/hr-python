from . import *
from . import expr
from . import validators
from filter_expression import filter_expression
from  aggregate_expression import aggregate_expression
class data_field():
    data_type="text"
    is_require = False
    def __init__(self,data_type="text",is_require=False):
        self.is_require=is_require
        self.data_type=data_type


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
    return ret
def define_model(name,keys=None,*args,**kwargs):
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


def create_field(data_type="text",is_require=False):
    return data_field(data_type,is_require)
