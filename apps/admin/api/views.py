import authorization
def get_list(params):
    return authorization.get_list_of_views(
        search=params.get("search_text",""),
        page_index=params.get("page_index",0),
        page_size=params.get("page_index",50))

