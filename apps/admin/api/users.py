import argo
import membership
import authorization
def get_list(args):
    if authorization.is_allow_read(args["privileges"]):
        list=argo.membership.find(args.get("search_text",""),0,50)
        return list
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