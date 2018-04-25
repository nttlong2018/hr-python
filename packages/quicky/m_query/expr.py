import _ast
import re
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
def get_left(cp):
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
                "params":[get_left(x) for x in cp.args]
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
                "left":get_left(cp.left)
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
            "expr":[get_left(x) for x in cp.values]
        }


    return ret;


def get_right(cp):
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
            "left":get_left(cp.left),
            "operator":find_operator(cp.ops[0]),
            "right":get_right(cp.comparators)
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
                "left": get_left(cp.left)
            })
        if cp._fields.count("comparators"):
            ret.update({
                "left": get_left(cp.comparators[0])
            })
        if cp._fields.count("values")>0:
            ret.update({
                "right": get_right(cp.value.values[1])
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
def get_tree(expr,*params):
    ret={}

    str=vert_expr(expr,*params)
    cmp=compile(str, '<unknown>', 'exec', 1024).body.pop()
    if type(cmp.value) is _ast.Compare:
        return {
            "left":get_left(cmp.value.left),
            "operator":find_operator(cmp.value.ops[0]),
            "right":get_right(cmp.value.comparators)
        }

    if cmp.value._fields.count("left")>0:
        ret.update({
            "left":get_left(cmp.value.left)
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
            "left": get_left(cmp.value.values[0])
        })
        ret.update({
            "right": get_right(cmp.value.values[1])
        })
    if type(cmp.value) is _ast.BoolOp:
        return {
            "operator":find_operator(cmp.value.op),
            "left":get_left(cmp.value.values[0]),
            "right": get_left(cmp.value.values[1])
        }

    return ret
def get_expr(fx,*params):
    if(type(fx) is str):
        return fx
    ret={}
    if fx.has_key("operator"):
        if fx["operator"]=="$eq":
            if fx["right"]["type"]=="params":
                val=params[fx["right"]["value"]]
                if type(val) is str:
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

