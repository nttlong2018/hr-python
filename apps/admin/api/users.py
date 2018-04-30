import argo
import quicky
import authorization
app=argo.applications.get_app_by_file(__file__)
database=quicky.db.database.connect(app.settings.Database)
def get_list(args):
    if authorization.is_allow_read(args["privileges"]):
        coll = database.collection("auth_user").aggregate()

        list=database.collection("auth_user").get_list()
        search_text=args["data"].get("searchText","")
        page_size=args["data"].get("pageSize",20)
        page_index=args["data"].get("pageIndex",0)

        if search_text!="":
            coll=coll.match("(contains(username,@search_text))or"
                                        "(contains(first_name,@search_text))or"
                                        "(contains(last_name,@search_text))",
                                        search_text=search_text)
        count=coll.copy()
        count.count("totalItems")
        totalItems=count.get_item().get("totalItems",0)

        coll.project(username=1,
                     first_name=1,
                     last_name=1,
                     is_active=1,
                     email=1,
                     is_supperuser=1,
                     is_staff=1,
                     last_logon=1,
                     date_joined=1)
        coll=coll.skip(page_index*page_size).limit(page_size)
        items=coll.get_list()
        return dict(
            pageSize=page_size,
            pageIndex=page_index,
            items=items,
            total=1000
        )

    else:
        return []
def create(args):
    try:
        user=membership.create_user(args.get("username",""),args.get("password",""),args.get("email",""))
        user.description=args.get("description","")
        user.displayName = args.get("displayName", "")
        user.email=args.get("email,""")
        user.isSysAdmin = args.get("isSysAdmin", False)
        user.isStaff = args.get("isStaff", False)
        membership.update_user(user)
        membership.active_user(user.username)

    except membership.models.exception as ex:
        return {
            "error": ex.message
        }
    except Exception  as ex:
        return {
            "error":ex.message
        }

    return {}
def update(args):
    user=membership.get_user(args.get("username",""))
    if user==None:
        return {
            "error":{
                "code":"user_not_found"
            }
        }
    user.description = args.get("description", "")
    user.displayName = args.get("displayName", "")
    user.isSysAdmin=args.get("isSysAdmin", False)
    user.isStaff=args.get("isStaff",False)
    user.email = args.get("email,""")
    membership.update_user(user)
    membership.active_user(user.username)
    return {}