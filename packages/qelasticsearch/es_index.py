class es_index():
    index_name=None
    _es=None
    def __init__(self,index_name, _es):
        self.index_name=index_name
        self._es=_es
    def search(self,*args,**kwargs):
        content_search=""
        fields=None
        if args==():
            content_search=kwargs["content"]
            fields=kwargs["fields"]
        elif type(args) in [unicode,str]:
            content_search=args
        if fields==None:
            ret_data=self._es.search(
                index=self.index_name,
                body={
                    "query":
                        {
                            "query_string":
                                {
                                    "query":content_search

                                }
                        }
                })
        else:
            ret_data = self._es.search(
                index=self.index_name,
                body={
                    "query":
                        {
                            "query_string":
                                {
                                    "fields":fields,
                                    "query": content_search

                                }
                        }
                })
        return dict(
            items=[x["_source"] for x in ret_data["hits"]["hits"]],
            total_items=ret_data["hits"]["total"],
            max_score=ret_data["hits"]["max_score"]
        )
    def create(self,id,data):
        ret=self._es.index(
            index=self.index_name,
            # doc_type="post",
            body=data,
            id=id
        )
        return ret
