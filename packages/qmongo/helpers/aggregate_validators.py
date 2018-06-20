import _ast
class validator:
    """
    This class is support for qmongo.database.COLL and qmongo.database.AGGREGATE
    """
    meta=None
    name=None
    fields=[]
    events=None
    def __init__(self,name,meta):
        """
        Init class
        :param name: the name of model
        :param meta: model fields describe
        """
        self.name=name
        self.meta=meta
        self.fields=[x for x in meta.keys()]
    def get_fields(self):
        #type: ()->list
        """
        Get list of field of model
        :return:
        """
        return self.fields
    def validate_expression(self,expr,fields=None,*params,**kwargs):
        # type: (str,list) -> list
        """
        Check if all fields in the expression is match with fields list
        :param expr:Expression for checking example "username=={0} and password== {1}
        :param fields: List of fields for checking, exanple; ["username","password"]
        :param params:
        :param kwargs:
        :return:list of unknown fields is collecion of fields where is not in fields param
        """
        _expr=expr
        if type(params) is tuple and params.__len__() > 0 :
            if type(params[0]) is dict:
                _params = []
                _expr = expr
                _index = 0;
                for key in params[0].keys():
                    _expr = _expr.replace("@" + key, "{" + _index.__str__() + "}")
                    _params.append(params[0][key])
                    _index += 1
                expr = _expr
                params = _params
            elif type(params[0]) is list:
                for x in params[0]:
                    _expr = _expr.replace("{" + params[0].index(x).__str__()+"}", "get_param("+params[0].index(x).__str__()+")")


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
        if fields==None:
            fields=self.fields
        fx = cmp = compile(_expr, '<unknown>', 'exec', 1024).body.pop()
        fields_in_expression=get_expression_fields(fx)
        ret_fields=[]
        for x in fields_in_expression:
            if x!="_id":
                if fields.count(x)==0:
                    ret_fields.append(x)

        return ret_fields
def get_field_name(fx):
    """This function will get full expression of field.
    The function just serve for package self
    """
    if type(fx.value) is _ast.Attribute:
        if hasattr(fx, "attr"):
            return get_field_name(fx.value)+"."+fx.attr
        else:
            return get_field_name(fx.value)
    else:
        if type(fx.value) is _ast.Subscript:
            return get_field_name(fx.value) + "." + fx.attr
        else:
            if hasattr(fx,"attr"):
                return fx.value.id+"."+fx.attr
            else:
                return fx.value.id


def get_expression_fields(fx):
    """
    This method will extract all fields in fx,
    Example: the fx parse from "username=={0} and password== {1} this method will return ["username","password"]
    :param fx:
    :return: list of fields
    """
    if type(fx) is _ast.Attribute:
        return [get_field_name(fx)]
    if type(fx) is _ast.Name:
        return [fx.id]
    if type(fx) is _ast.Expr:
        return get_expression_fields(fx.value)
    if type(fx) is _ast.Subscript:
        return get_expression_fields(fx.value)
    if type(fx) is _ast.Call:
        ret=[]
        for x in fx.args:
            ret_fields=get_expression_fields(x)
            for e in ret_fields:
                ret.append(e)
        return ret
    if type(fx) is _ast.BinOp:
        ret=[]
        ret_fields = get_expression_fields(fx.left)
        for e in ret_fields:
            ret.append(e)
        ret_fields = get_expression_fields(fx.right)
        for e in ret_fields:
            ret.append(e)
        return ret
    if type(fx) is _ast.Compare:
        ret=[]
        ret_fields = get_expression_fields(fx.left)
        for e in ret_fields:
            ret.append(e)
        ret_fields = get_expression_fields(fx.comparators[0])
        for e in ret_fields:
            ret.append(e)
        return ret
    return []



