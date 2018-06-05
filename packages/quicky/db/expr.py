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
    dict(op="$subtract",fn=_ast.Sub),
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
        elif cp.func.id=="get_params":
            return {
                "type":"function",
                "id":"get_params",
                "value":cp.args[0].n
            }
        else:
            return {
                "type": "function",
                "id": "$"+cp.func.id,
                "params":[
                    extract_json(x, *params) for x in cp.args
                ]
            }

    if type(cp) is _ast.Set:
        return {
            "type":"const",
            "value":cp.elts[0].n
        }
    if type(cp) is _ast.Compare:
        if cp._fields.count("left")>0:
            return {
                "operator":find_operator(cp.ops[0]),
                "left":get_left(cp.left,*params),
                "right":get_right(cp.comparators[0],*params)

            }
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
    if type(cp) is _ast.Num:
        return {
            "type":"const",
            "value":cp.n
        }




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
            "value":cp.n
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
    while type(params) is tuple and params.__len__()>0 and type(params[0]) is dict:
        params=params[0]
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
    elif type(params) is dict:
        _params = []
        _expr = expr
        _index = 0;
        for key in params.keys():
            _expr = _expr.replace("@" + key, "{" + _index.__str__() + "}")
            _params.append(params[key])
            _index += 1
        expr = _expr
        params = _params
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
    if type(cmp.value) is _ast.BoolOp:
        return {
            "operator": find_operator(cmp.value.op),
            "left": [get_left(x, *params) for x in cmp.value.values],
            "right": None
        }
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
        if type(cmp.value.values[1]) is _ast.Call:
            return {
                "operator": find_operator(cmp.value.op),
                "left": get_left(cmp.value.values[0], *params),
                "right": get_left(cmp.value.values[1], *params)
            }
        else:
            return {
                "operator": find_operator(cmp.value.op),
                "left": get_left(cmp.value.values[0], *params),
                "right": get_right(cmp.value.values[1], *params)
            }
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
                "operator": "$contains",
                "right": params[cmp.value.args[1].args[0].n]
            }
        else:
            return {
                "left":cmp.value.args[0].id,
                "operator":"$contains",
                "right":cmp.value.args[1].s
            }





    return ret
def get_expr(fx,*params):
    while type(params) is tuple and params.__len__()>0 and type(params[0]) is tuple:
        params=params[0]
    while type(params) is tuple and params.__len__()>0 and type(params[0]) is dict:
        params = params[0]
    if type(params) is dict:
        params=[params[key] for key in params.keys()]

    if(type(fx) is str):
        return fx
    ret={}
    if fx.has_key("type") and fx["type"]=="const":
        return fx["value"]
    if fx.has_key("type") and fx["type"]=="field":
        return fx["id"]


    if fx.has_key("operator"):
        if fx["operator"]=="$contains":
            return {
                fx["left"]:re.compile(fx["right"],re.IGNORECASE)

            }

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
                        if fx["operator"]=="$eq" and type(val) is str:
                            if type(fx["left"]) is str:
                                return {
                                    fx["left"]: {
                                        "$regex":re.compile("^"+val+"$",re.IGNORECASE)
                                    }

                                }
                            if type(fx["left"]) is dict:
                                return {
                                    fx["left"]["id"]:{
                                        "$regex":re.compile("^"+val+"$",re.IGNORECASE)
                                    }

                                }

                        else:
                            if type(fx["left"]) is str:
                                return {
                                    fx["left"]:{
                                        fx["operator"]: val
                                    }

                                }
                            if type(fx["left"]) is dict:
                                return {
                                    fx["left"]["id"]: {
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
                        if fx["left"]=={}:
                            return val
                        elif fx["left"].has_key("id"):
                            return {
                                fx["left"]["id"]: {
                                    fx["operator"]: val
                                }
                            }
        else:
            if fx.has_key("right"):
                if fx["right"]!=None:
                    if fx["right"].get("type","") == "const":
                        val = fx["right"]["value"]
                        if fx["left"]=={}:
                            return val
                        else:
                            return {
                                get_expr(fx["left"], *params):{
                                    fx["operator"]:get_expr(fx["right"], *params)
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
                elif type(fx["left"]) is list:
                    ret_json={
                        fx["operator"]:[]
                    }
                    for item in fx["left"]:
                        _m=get_expr(item,*params)
                        ret_json[fx["operator"]].append(_m)
                    return ret_json
            if fx.has_key("operator") and fx.has_key("expr"):
                ret_json={
                    fx["operator"]:[]
                }
                for item in fx["expr"]:
                    _m=get_expr(item,*params)
                    ret_json[fx["operator"]].append(_m)
                return ret_json
                # return {
                #     fx["operator"]:[
                #         get_expr(x,*params) for x in fx["expr"]
                #     ]
                # }
    elif fx.has_key("function") and fx["function"].lower()=="contains":
        if fx["params"][1].has_key("value"):
            if fx["params"][1].has_key("type") and\
               fx["params"][1]["type"]=="function" and\
                fx["params"][1]["id"]=="get_params":
                return {
                    fx["params"][0]["id"]:{"$regex":re.compile(params[fx["params"][1]["value"]],re.IGNORECASE)}
                }
            else:
                return {
                    fx["params"][0]["id"]:{"$regex":re.compile(fx["params"][1]["value"],re.IGNORECASE)}
                }

    if fx.has_key("operator"):
        return {
            fx["operator"]:[
                get_expr(fx["left"],*params),
                get_expr(fx["right"],*params)
            ]
        };
    if fx.has_key("type") and fx["type"]=="function":
        return {
            fx["id"]:[fx["params"]]
        }
def get_calc_exprt_boolean_expression(fx,*params):
    p=get_right(fx,*params)
    if fx._fields.count("left")>0 and type(fx.left) is _ast.Call:
        field = get_left(fx.left.args[0])
        if p["right"]["type"]=="const":
            return {
                p["operator"]:[
                    {
                        "$" + fx.left.func.id:"$"+field["id"]
                    },p["right"]["value"]
                ]
            }
        if p["right"]["type"]=="params":
            return {
                p["operator"]: [
                    {
                        "$" + fx.left.func.id: "$" + (lambda x: x if type(x) is str else x["id"])(field)
                    }, params[p["right"]["value"]]
                ]
            }


    if type(fx) is _ast.Compare:
        return {
            find_operator(fx.ops[0]):[
                get_calc_exprt_boolean_expression(fx.left,*params),
                get_calc_exprt_boolean_expression(fx.comparators[0],*params)
            ]
        }

    if type(fx) is _ast.BoolOp:
        return {
            find_operator(fx.op): [
                [get_calc_exprt_boolean_expression(x,*params) for x in fx.values]

            ]
        }
def extract_json(fx,*params):
    if type(fx) is _ast.Name:
        p=get_left(fx,*params)
        return "$"+p["id"]
    if type(fx) is _ast.Num:
        return fx.n
    if type(fx) is _ast.Str:
        return fx.s

    if type(fx) is _ast.Call:
        if fx.func.id=="get_params":
            return params[fx.args[0].n]

        if fx.func.id=="iif":
            return {
                "$cond": { "if": get_calc_exprt_boolean_expression(fx.args[0],*params),
                           "then": extract_json(fx.args[1],*params),
                            "else": extract_json(fx.args[2],*params) }
            }
        elif fx.func.id=="dateToString":
            p_left = get_left(fx.args[0],*params)
            p_right = get_left(fx.args[1],*params)
            val=p_right["value"]
            if p_right["type"]=="function" and p_right["id"]=="get_params":
                val=params[val]
            # return { $dateToString: { format: "%Y-%m-%d", date: "$date" } }
            return {
                "$dateToString":{
                    "format":val,
                    "date":"$"+p_left["id"]

                }
            }
        elif fx.func.id=="dateFromString":
            p_left = get_left(fx.args[0], *params)
            p_right = get_left(fx.args[1], *params)
            val = p_right["value"]
            if p_right["type"] == "function" and p_right["id"] == "get_params":
                val = params[val]
            # return { $dateToString: { format: "%Y-%m-%d", date: "$date" } }
            return {
                "$dateToString": {
                    "timezone": val,
                    "dateString": "$" + p_left["id"]

                }
            }
        elif fx.func.id=="switch":
            branches=[]
            for item in fx.args:
                if fx.args.index(item)<fx.args.__len__()-1:

                    branches.append({
                        "case":extract_json(item.args[0],*params),
                        "then":extract_json(item.args[1],*params)

                    })

            return {
                "$switch":{
                    "branches":branches,
                    "default":extract_json(fx.args[fx.args.__len__()-1],*params)
                }
            }
            k=cmp
            pass

        else:
            return {
                "$"+fx.func.id:[
                    extract_json(x,*params) for x in fx.args

                ]
            }
    if type(fx) is _ast.BinOp:
        return {
            find_operator(fx.op):[
                extract_json(fx.left,*params),
                extract_json(fx.right,*params)
            ]
        }
    if type(fx) is _ast.Compare:
        return {
            find_operator(fx.ops[0]):[
                extract_json(fx.left, *params),
                extract_json(fx.comparators[0], *params)
            ]

        }
def get_calc_expr_boolean_expression_result(fx,*params):
    p = get_left(fx,*params)
    if p["type"]=="const":
        return p["value"]
    if p["type"]=="function" and p["id"]=="get_params":
        return params[p["value"]]


def get_calc_expr(expr,*params,**kwargs):
    if expr==1:
        return expr
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


    expr=vert_expr(expr,*params)
    cmp = compile(expr, '<unknown>', 'exec', 1024).body.pop()
    return extract_json(cmp.value,*params)






def get_calc_get_param(fx,*params):
    if type(fx) is _ast.Name:
        return "$"+get_calc_get_names(fx)
    if type(fx) is _ast.Str:
        return fx.s

    if type(fx) is _ast.Num:
        return fx.n
    if type(fx) is _ast.Attribute:
        return "$" + get_left(fx)

def get_calc_get_names(fx):
    return fx.id
def verify_match(fx):
    if not fx.has_key("left"):
        return None
    if fx["left"].has_key("type") and fx["left"]["type"] == "function":
        return "The left side of the expression is not a field of the document. " \
               "It look like you use function. function name is '{0}' ".format(fx["left"]["id"])

    if type(fx["left"]) is list:
        index=0
        msg=None
        while msg==None and index<fx["left"].__len__():
            msg = verify_match(fx["left"][index])
            index=index+1
        return msg


    if fx["left"].has_key("type") and  fx["left"]["type"] =="const":
        return "The left side of the expression is not a field of the document. " \
               "It look like constant or expression. Actually expression is '{0}'  "\
            .format(fx["left"]["value"])
    else:
        return verify_match(fx["left"])
def parse_expression_to_json_expression(expression,*params,**kwargs):
    expr_tree=get_tree(expression,*params,**kwargs)
    msg=verify_match(expr_tree)
    if msg!=None:
        raise(Exception(msg))
    return get_expr(expr_tree,*params,**kwargs)


