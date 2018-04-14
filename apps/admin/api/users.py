import argo
import membership
def get_list(args):
    list=argo.membership.find(args.get("search_text",""),0,50)
    return list
def create(args):
    try:
        user=membership.create_user(args.get("username",""),args.get("password",""),args.get("email",""))
        user.description=args.get("description","")
        user.displayName = args.get("displayName", "")
        user.email=args.get("email,""")
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

    return args