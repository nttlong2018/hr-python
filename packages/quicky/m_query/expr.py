import _ast
import re
import inspect
_operators=[
    dict(op="$eq",fn=_ast.Eq),
    dict(op="$ne",fn=_ast.NotEq),
    dict(op="$gt",fn=_ast.Gt),
    dict(op="$gte",fn=_ast.GtE),
    dict(op="$lt",fn=_ast.Lt),
    dict(op="$lte",fn=_ast.LtE),
    dict(op="$multi",fn=_ast.Mult),
    dict(op="$div",fn=_ast.Div),
    dict(op="$mode",fn=_ast.Mod),
    dict(op="$add",fn=_ast.Add),
    dict(op="$sub",fn=_ast.Sub),
    dict(op="$and",fn=_ast.And),
    dict(op="$or",fn=_ast.Or),
    dict(op="$not",fn=_ast.Not),
    dict(op="$in",fn=_ast.In),
    dict(op="$notin",fn=_ast.NotIn)
]
def get_comparators(cp):
    if cp._fields.count("elts")>0:
        if type(cp.elts[0]) is _ast.Num:
            return {
                "type":"get_params",
                "index":cp.elts[0].n
            }
    if cp._fields.count("func")>0:
        fn=cp.func
        if fn.id=="get_params":
            return {
                "type": fn.id,
                "index": cp.args[0].n
            }

    raise Exception("Invalid comparators {0}".format(cp))
def get_left(cp,*params):
    ret={}
    if type(cp) is _ast.Name:
        return {
            "type":"field",
            "id":cp.id
        }
    if type(cp) is _ast.Str:
        return {
            "type":"const",
            "value":cp.s
        }
    if type(cp) is _ast.Call:
        if cp.func.id=="contains":
            return {
                "function":cp.func.id,
                "params":[get_left(x,*params) for x in cp.args]
            }
        if cp.func.id=="get_params":
            return {
                "type":"function",
                "id":"get_params",
                "value":cp.args[0].n
            }
    if type(cp) is _ast.Set:
        return {
            "type":"const",
            "value":cp.elts[0].n
        }
    if type(cp) is _ast.Compare:
        if cp._fields.count("left"):
            ret.update({
                "left":get_left(cp.left,*params)
            })
        ret.update({
            "operator":find_operator(cp.ops[0])
        })
        if cp._fields.count("comparators"):
            ret.update({
                "right": get_right(cp.comparators)
            })
    if type(cp) is _ast.BoolOp:
        return {
            "operator":find_operator(cp.op),
            "expr":[get_left(x,*params) for x in cp.values]
        }
    if type(cp) is _ast.Attribute:
        _v=cp.value
        _field=cp.attr
        while not type(_v) is _ast.Name:
            if type(_v) is _ast.Attribute:
                _field=_v.attr+"."+_field

            if type(_v) is _ast.Subscript:
                if type(_v.slice) is _ast.Index:
                    if type(_v.slice.value) is _ast.Call and _v.slice.value.func.id=="get_params":
                        _field = "[" + _v.slice.value.args[0].n.__str__() + "]." + _field
                    else:
                        _field = "[" + _v.slice.value.n.__str__() + "]." + _field
                # if type(_v.slice) is _ast.Index:
                #     _field = "[" + _v.slice.value.n.__str__() + "]." + _field


            _v = _v.value

        _field=_v.id+"."+_field
        return _field.replace(".[","[")






        if cp.value._fields.count("slice")>0:
            return cp.value.value.id + "["+cp.value.slice.value.n.__str__()+"]." + cp.attr
        else:
            return cp.value.id + "." + cp.attr



    return ret;


def get_right(cp,*params):
    ret={}
    if type(cp) is list:
        if cp.__len__()>1 and\
            type(cp[0]) is _ast.Call and\
            type(cp[1]) is _ast.Num:
            return {
                "type":"function",
                "id":cp[0].func.id,
                "params":[cp[1].n]
            }
        if cp.__len__()==1 and\
            type(cp[0]) is _ast.Call and\
            cp[0].func.id=="get_params" and \
            type(cp[0].args[0]) is _ast.Num :
            return {
                "type":"params",
                "value":cp[0].args[0].n
            }
        if cp.__len__()==1 and type(cp[0]) is _ast.Str:
            return {
                "type":"const",
                "value":cp[0].s
            }



        if type(cp[0]) is _ast.Num:
            return {
                "type": "const",
                "value":cp[0].n
            }
    if type(cp) is _ast.Num:
        return {
            "type":"const",
            "value":cp[0].n
        }

    if type(cp) is _ast.Compare:
        return {
            "left":get_left(cp.left,*params),
            "operator":find_operator(cp.ops[0]),
            "right":get_right(cp.comparators,*params)
        }
    if type(cp) is list and\
            cp.__len__()==1 and \
            cp[0]._fields.count("func")>0 and \
            cp[0].func.id=="contains":

        return {
            "type":"function",
            "id":cp[0].func.id,
            "field":cp[0].args[0].s,
            "value":cp[0].args[1].s
        }
    if type(cp) is list and cp.__len__()==1 and \
        type(cp[0]) is _ast.Set and \
        cp[0]._fields.count('elts') > 0:
        return {
            "type":"const",
            "value":cp[0].elts[0].n
        }





    if cp._fields.count("ops")>0:
        ret.update({
            "operator": find_operator(cp.ops[0])
        })
        if cp._fields.count("left")>0:
            ret.update({
                "left": get_left(cp.left,*params)
            })
        if cp._fields.count("comparators"):
            ret.update({
                "left": get_left(cp.comparators[0],*params)
            })
        if cp._fields.count("values")>0:
            ret.update({
                "right": get_right(cp.value.values[1],*params)
            })
    if type(cp) is _ast.Call and cp.func.id.lower()=="contains":
        if cp.args[1]._fields.count("s")>0:
            return {
                "type":"function",
                "id":"contains",
                "field":cp.args[1].s
            }
        if cp.args[1]._fields.count("elts")>0:
            return {
                "type": "function",
                "id": "contains",
                "field": cp.args[1].s
            }
    if type(cp) is _ast.Call and cp.func.id.lower() == "get_params":
        return {
            "type":"params",
            "value":cp.args[0].n
        }






    return ret




def find_operator(op):
    for x in _operators:
        if type(op) is x["fn"]:
            return x["op"]
    raise Exception("Invalid comparators {0}".format(op))
def vert_expr(str,*params):
    ret=str
    index=0
    for p in params:
        ret=ret.replace("{"+index.__str__()+"}","get_params("+index.__str__()+")")
        index=index+1
    return ret
def get_tree(expr,*params,**kwargs):
    if type(params) is tuple and params.__len__()>0 and type(params[0]) is dict:
        _params=[]
        _expr=expr
        _index=0;
        for key in params[0].keys():
            _expr=_expr.replace("@"+key,"{"+_index.__str__()+"}")
            _params.append(params[0][key])
            _index+=1
        expr=_expr
        params=_params
    elif params==():
        _params = []
        _expr = expr
        _index = 0;
        for key in kwargs.keys():
            _expr = _expr.replace("@" + key, "{" + _index.__str__() + "}")
            _params.append(kwargs[key])
            _index += 1
        expr = _expr
        params = _params


    ret={}

    str=vert_expr(expr,*params)
    cmp=compile(str, '<unknown>', 'exec', 1024).body.pop()
    if type(cmp.value) is _ast.Compare:
        return {
            "left":get_left(cmp.value.left,*params),
            "operator":find_operator(cmp.value.ops[0]),
            "right":get_right(cmp.value.comparators,*params)
        }

    if cmp.value._fields.count("left")>0:
        ret.update({
            "left":get_left(cmp.value.left,*params)
        })
    if cmp.value._fields.count("right")>0:
        ret.update({
            "right":{
                "id":cmp.value.right.id,
                "type":"field"
            }
        })
    elif cmp.value._fields.count("comparators")>0:
        ret.update({
            "right": get_comparators(cmp.value.comparators[0])
        })
    if cmp.value._fields.count("ops")>0:
        ret.update({
            "operator": find_operator(cmp.value.ops[0])
        })
    if cmp.value._fields.count("op")>0:
        ret.update({
            "operator": find_operator(cmp.value.op)
        })
        ret.update({
            "left": get_left(cmp.value.values[0],*params)
        })
        ret.update({
            "right": get_right(cmp.value.values[1],*params)
        })
    if type(cmp.value) is _ast.BoolOp:
        return {
            "operator":find_operator(cmp.value.op),
            "left":get_left(cmp.value.values[0],*params),
            "right": get_left(cmp.value.values[1],*params)
        }
    if type(cmp.value) is _ast.Call and \
            cmp.value.func.id=="contains":
        if type(cmp.value.args[1]) is _ast.Call and \
                cmp.value.args[1].func.id=="get_params":
            return {
                "left": cmp.value.args[0].id,
                "operator": "$eq",
                "right": params[cmp.value.args[1].args[0].n]
            }
        else:
            return {
                "left":cmp.value.args[0].id,
                "operator":"$eq",
                "right":cmp.value.args[1].s
            }





    return ret
def get_expr(fx,*params):
    while type(params) is tuple and params.__len__()>0 and type(params[0]) is tuple:
        params=params[0]
    if(type(fx) is str):
        return fx
    ret={}
    if fx.has_key("operator"):
        if fx["operator"]=="$eq":
            if type(fx["right"]) is str:
                return {
                    fx["left"]: {
                        "$regex": re.compile(fx["right"], re.IGNORECASE)
                    }
                }
            else:
                if fx["right"]["type"]=="params":
                    val=params[fx["right"]["value"]]
                    if type(val) is str:
                        if type(fx["left"]) is str:
                            return {
                                fx["left"]: {
                                    "$regex": re.compile("^" + val + "$", re.IGNORECASE)
                                }
                            }
                        else:
                            return {
                                fx["left"]["id"]:{
                                    "$regex":re.compile("^"+val+"$",re.IGNORECASE)
                                }
                            }
                    else:
                        return {
                            fx["left"]:{
                                fx["operator"]: val
                            }

                        }
                if fx["right"]["type"]=="const":
                    val = fx["right"]["value"]
                    if type(val) is str:
                        return {
                            fx["left"]["id"]: {
                                "$regex": re.compile("^" + val + "$", re.IGNORECASE)
                            }
                        }
                    else:
                        return {
                            fx["left"]["id"]: {
                                fx["operator"]: val
                            }

                        }
        else:
            if fx.has_key("right"):
                if fx["right"].get("type","") == "const":
                    val = fx["right"]["value"]
                    return {
                        fx["left"]: {
                            fx["operator"]: val
                        }
                    }
                if fx["right"].get("type","") == "params":
                    val =params[fx["right"]["value"]]
                    return {
                        fx["left"]: {
                            fx["operator"]: val
                        }
                    }
                if fx["right"].get("function","") == "contains":
                    if fx.has_key("params"):
                       if fx["params"][1].get("type","")=="const":
                            return {
                                fx["params"][0]["id"]:fx["params"][1]["value"]
                            }
                       if fx["params"][1].get("type", "") == "params":
                           return {
                               fx["params"][0]["id"]:params[fx["params"][1]["value"]]
                           }
                    if fx.has_key("operator"):
                        return {
                            fx["operator"]:[
                                get_expr(fx["left"],*params),
                                get_expr(fx["right"], *params)
                            ]
                        }
            if fx.has_key("operator") and fx.has_key("expr"):
                return {
                    fx["operator"]:[
                        get_expr(x,*params) for x in fx["expr"]
                    ]
                }
    elif fx.has_key("function") and fx["function"].lower()=="contains":
        if fx["params"][1].has_key("value"):
            if fx["params"][1].has_key("type") and\
               fx["params"][1]["type"]=="function" and\
                fx["params"][1]["id"]=="get_params":
                return {
                    fx["params"][0]["id"]: params[fx["params"][1]["value"]]
                }
            else:
                return {
                    fx["params"][0]["id"]: fx["params"][1]["value"]
                }
    ret.update({
        fx["operator"]:[
            get_expr(fx["left"],*params),
            get_expr(fx["right"],*params)
        ]
    })
    return ret;
def get_calc_expr_if(ifexpr):
    pass
def get_calc_expr(expr,*params,**kwargs):
    if type(params) is tuple and params.__len__() > 0 and type(params[0]) is dict:
        _params = []
        _expr = expr
        _index = 0;
        for key in params[0].keys():
            _expr = _expr.replace("@" + key, "{" + _index.__str__() + "}")
            _params.append(params[0][key])
            _index += 1
        expr = _expr
        params = _params
    elif params == ():
        _params = []
        _expr = expr
        _index = 0;
        for key in kwargs.keys():
            _expr = _expr.replace("@" + key, "{" + _index.__str__() + "}")
            _params.append(kwargs[key])
            _index += 1
        expr = _expr
        params = _params
    if callable(expr):
        field_name=inspect.getsource(expr).split('=')[0]
        expr=inspect.getsource(expr)[field_name.__len__()+1:inspect.getsource(expr).__len__()]



    cmp = compile(expr, '<unknown>', 'exec', 1024).body.pop()
    if type(cmp.value) is _ast.Tuple and cmp.value._fields.count("elts")>0 and type(cmp.value.elts[0]) is _ast.Lambda:
        if type(cmp.value.elts[0].body) is _ast.IfExp:
            return get_calc_expr_if(cmp.value.elts[0].body)


    if type(cmp.value) is _ast.Call:
        return {
            "$"+cmp.value.func.id:[
                get_calc_get_param(x) for x in cmp.value.args

            ]
        }
    if type(cmp.value) is _ast.BinOp:
        return {
            find_operator(cmp.value.op):[
                get_calc_get_param(cmp.value.left),
                get_calc_get_param(cmp.value.right)
            ]
        }
def get_calc_get_param(fx):
    if type(fx) is _ast.Name:
        return "$"+get_calc_get_names(fx)
    if type(fx) is _ast.Str:
        return fx.s

    if type(fx) is _ast.Num:
        return fx.n

def get_calc_get_names(fx):
    return fx.id
def parse_expression_to_json_expression(expression,*params,**kwargs):
    expr_tree=get_tree(expression,*params,**kwargs)
    return get_expr(expr_tree,*params,**kwargs)


