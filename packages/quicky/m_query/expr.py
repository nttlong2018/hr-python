import _ast
_operators=[
    dict(op="$eq",fn=_ast.Eq),
    dict(op="$ne",fn=_ast.NotEq),
    dict(op="$gt",fn=_ast.Gt),
    dict(op="$gte",fn=_ast.GtE),
    dict(op="$and",fn=_ast.And),

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
        return cp.id

    if type(cp) is _ast.Call:
        return {
            "function":cp.func.id,
            "params":[x.id for x in cp.args]
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
    return ret

