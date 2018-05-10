class query():
    _es=None
    def __init__(self,es):
        self._es=es
    def get_all_indexes(self):
        return self._es.indices.get_mapping().keys()
    def get_index(self,name):
        if not self._es.indices.exists(index=name):
            self._es.indices.create(index=name)
        else:
            self._es.indices.get(index=name)
        return self._es
    def search_all(self,index_name):
        ret_data=self._es.search(index=index_name)
        return dict(
            items=[x["_source"] for x in ret_data["hits"]["hits"]],
            total_items=ret_data["hits"]["total"],
            max_score=ret_data["hits"]["max_score"]
        )
    def search_text(self,index_name,text):
        ret_data=self._es.search(
            index=index_name,
            body={
                "query":
                    {
                        "query_string":
                            {
                                "query":
                                    text
                            }
                    }
            })
        return dict(
            items=[x["_source"] for x in ret_data["hits"]["hits"]],
            total_items=ret_data["hits"]["total"],
            max_score=ret_data["hits"]["max_score"]
        )
    def create(self,index_name,data,id):
        ret=self._es.index(index=index_name,doc_type='post', body=data,id=id)
        return ret

