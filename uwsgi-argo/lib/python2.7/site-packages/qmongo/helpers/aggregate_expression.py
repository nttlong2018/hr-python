from . import *
import expr
class aggregate_expression():
    _pipe=None
    def __init__(self):
        self._pipe=[]
    def select(self,*args,**kwargs):
        """
               Create project pipeline
               Ex:
                   project(
                       dict(
                           FullName="toUpper(concat(FirstName,' ',LastName))",
                           Age="year(@time_now)- year(BirthDate)",
                           Username=1,
                           CreatedOn=1
                       ),
                       time_now=datetime.now()
                   )
               :param args:
               :param kwargs:
               :return:
               """
        _project = {}
        if kwargs == {}:
            kwargs = args[0]
            if args.__len__() > 1:

                params = args[1]
            else:
                params = args[0]

        else:

            params = []
            if type(args) is tuple and args.__len__() > 1 and type(args[0]) is dict:

                params = [e for e in args if args.index(e) > 0]
                kwargs = args[0]
                args = []
            elif type(args) is tuple and args.__len__() == 1 and type(args[0]) is dict:
                params = kwargs
                kwargs = args[0]
            # for x in args:
            #     _project.update({
            #         x:1
            #     })
        for key in kwargs.keys():
            _project.update({
                key: expr.get_calc_expr(kwargs[key], params)
            })
        self._pipe.append({
            "$project": _project
        })
        return self
    def group(self,_id,selectors,*args,**kwargs):
        __id={}
        if type(_id) is dict:
            for key in _id.keys():
                __id.update({
                    key:expr.get_calc_expr(_id[key],*args,**kwargs)
                })
        else:
            __id="$"+_id
        _group = {
            "$group": {
                "_id": __id
            }
        }
        if not type(selectors) is dict:
            raise (Exception("'selectot' must be dict type"))


        for key in selectors.keys():
            _group["$group"].update({
                key:expr.get_calc_expr(selectors[key],*args,**kwargs)
            })
        self._pipe.append(_group)
        return self
    def skip(self,len):
        self._pipe.append({
            "$skip":len
        })
        return self
    def limit(self,num):
        self._pipe.append({
            "$limit": num
        })
        return self
    def unwind(self,field_name):
        if field_name[0:1]!="$":
            field_name="$"+field_name
        self._pipe.append({
            "$unwind":{"path":field_name,
                        "preserveNullAndEmptyArrays":True
                    }
        })
        return self
    def match(self,expression, *args,**kwargs):
        """Beware! You could not use any Aggregation Pipeline Operators, just use this function with Field Logic comparasion such as:
        and,or, contains,==,!=,>,<,..
        """
        if args==():
            args=kwargs

        if type(expression) is dict:
            self._pipe.append({
                "$match":expression
            })
            return self
        if type(expression) is str:
            self._pipe.append({
                "$match": expr.parse_expression_to_json_expression(expression,args)
            })
            return self

        pass
    def lookup(self,
               source=None,
               local_field=None,
               foreign_field=None,
               alias=None,
               *args,**kwargs):
        if args==() and kwargs=={}:
            _source=source
            kwargs.update(source=_source,
                          local_field=local_field,
                          foreign_field=foreign_field,
                          alias=alias)
        else:
            if not kwargs.has_key("source"):
                raise Exception("'source' was not found")
            if not kwargs.has_key("local_field"):
                raise Exception("'local_field' was not found")
            if not kwargs.has_key("foreign_field"):
                raise Exception("'foreign_field' was not found")
            if not kwargs.has_key("alias"):
                raise Exception("'alias' was not found")
        self._pipe.append({
            "$lookup":{
                "from":kwargs["source"],
                "localField":kwargs["local_field"],
                "foreignField":kwargs["foreign_field"],
                "as":kwargs["alias"]
            }
        })
        return self
    def sort(self,*args,**kwargs):
        _sort={

        }
        self._pipe.append({
            "$sort":kwargs
        })
        return self
    def count(self,alias):
        self._pipe.append({
            "$count":alias
        })
        return self
    def get_pipe(self):
        return self._pipe

