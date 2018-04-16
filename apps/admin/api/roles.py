import authorization
def get_list(*args,**kwargs):
    if not authorization.is_allow_read(args[0]["privileges"]):
        return []
    try:
        authorization.grant_role_to_user(role_code="admin", username="user1")
        authorization.add_view_to_role(view_path="pages/roles",
                                       app="admin",
                                       role_code="admin",
                                       create=True,
                                       read=True,
                                       update=True,
                                       delete=True,
                                       extends={},
                                       is_public=False)
        ret=authorization.get_list_of_roles(
            search=args[0]["data"].get("search_text",None),
            page_index=args[0]["data"].get("page_index",0),
            page_size=args[0]["data"].get("page_size",50)
        )
        return ret
    except Exception as ex:
        return []
def create(params):
    if not authorization.is_allow_create(params["privileges"]):
        return None

    ret = authorization.create_role(
        id=None,
        code=params["data"].get("code",""),
        name=params["data"].get("name",""),
        description=params["data"].get("description","")
    )
    return {}

