
from datetime import datetime
from . import *
import expr
class aggregate_expression():
    """
    this class is create pipeline for pymongo
    """

    def __init__(self):
        self._pipe=[]
    def select(self,*args,**kwargs):
        # type: (tuple,dict) ->aggregate_expression
        """
        create project mongdb pipeline
        Example:select(
                            FullName="toUpper(concat(FirstName,' ',LastName))",
                           Age="year(@time_now)- year(BirthDate)",
                           Username=1,
                           CreatedOn=1
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
        # type: (str,dict,str)->aggregate_expression
        # type: (str,dict,bool)->aggregate_expression
        # type: (str,dict,datetime)->aggregate_expression
        # type: (str,dict,int)->aggregate_expression
        # type: (str,dict,long)->aggregate_expression
        # type: (str,dict,float)->aggregate_expression
        # type: (str,dict,unicode)->aggregate_expression
        # type: (str,dict,list)->aggregate_expression
        # type: (str,dict,dict)->aggregate_expression
        # type: (dict,dict,str)->aggregate_expression
        # type: (dict,dict,bool)->aggregate_expression
        # type: (dict,dict,datetime)->aggregate_expression
        # type: (dict,dict,int)->aggregate_expression
        # type: (dict,dict,long)->aggregate_expression
        # type: (dict,dict,float)->aggregate_expression
        # type: (dict,dict,unicode)->aggregate_expression
        # type: (dict,dict,list)->aggregate_expression
        # type: (dict,dict,dict)->aggregate_expression

        """
        Create mongodb aggregate group
        :param _id: The _id in aggregate group see: https://docs.mongodb.com/manual/reference/operator/aggregation/group/
        :param selectors:dict of selector in group, example: dict(code=1,salary="BasicSalary*TotalDays")
        :param args: The parameters for group, example group(dict(code=1,salary="sum(BasicSalary*TotalDays,{0})",12000000)
        :param kwargs:
        :return:
        """
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
        # type: (int) -> aggregate_expression
        """
        Create skip mongodb aggregate
        :param len:
        :return:
        """
        self._pipe.append({
            "$skip":len
        })
        return self
    def limit(self,num):
        # type: (int) -> aggregate_expression
        """
        Create limit mongodb aggregate
        :param num:
        :return:
        """
        self._pipe.append({
            "$limit": num
        })
        return self
    def unwind(self,field_name):
        # type: (str) -> aggregate_expression
        """
        Create unwind mongodb aggregate
        :param field_name:
        :return:
        """
        if field_name[0:1]!="$":
            field_name="$"+field_name
        self._pipe.append({
            "$unwind":{"path":field_name,
                        "preserveNullAndEmptyArrays":True
                    }
        })
        return self
    def match(self,expression, *args,**kwargs):
        # type: (str,int) -> aggregate_expression
        # type: (str,bool) -> aggregate_expression
        # type: (str,str) -> aggregate_expression
        # type: (str,unicode) -> aggregate_expression
        # type: (str,datetime) -> aggregate_expression
        # type: (str,dict) -> aggregate_expression
        # type: (str,tuple) -> aggregate_expression
        # type: (str,list) -> aggregate_expression
        # type: (str,float) -> aggregate_expression

        """
          Create mongodb match aggregate
        Caution! You could not use any Aggregation Pipeline Operators, just use this function with Field Logic comparasion such as:
        and,or, contains,==,!=,>,<,..
        Exmaple match("username=={0} and password== {1}",'admin','1234)
        :param expression: Example "a=={0}" with 0 is index of params
        :param args:
        :param kwargs:
        :return:
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
        # type: (str,str,str,str) -> aggregate_expression
        """
        Create mongodb aggregate lookup refer to https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/
        :param source:source collection is 'from' in mongodb refer to https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/
        :param local_field:localField in mongodb refer to https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/
        :param foreign_field:foreignField in mongodb refer to https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/
        :param alias:as in mongodb refer to https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/
        :param args:
        :param kwargs:
        :return:
        """
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
        """
        Create mongdb aggregate sorting
        Example: sort(a=1,b=-1) that means is sort by "a" field asc and "b" desc. Refer:https://docs.mongodb.com/manual/reference/operator/aggregation/sort/
        :param args:
        :param kwargs:
        :return:
        """
        self._pipe.append({
            "$sort":kwargs
        })
        return self
    def count(self,alias):
        """
        Create a mongodb count aggregate. Refer: https://docs.mongodb.com/manual/reference/operator/aggregation/count/
        :param alias:
        :return:
        """
        self._pipe.append({
            "$count":alias
        })
        return self
    def get_pipe(self):
        """
        Get mongodb pipeline
        :return:
        """
        return self._pipe

