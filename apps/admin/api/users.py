import argo
import membership
def get_list(args):
    list=argo.membership.find(args.get("search_text",""),0,50)
    return list
def create(args):
    try:
        user=membership.create_user(args.get("username",""),args.get("password",""),args.get("email,"""))
    except membership.models.exception as ex:
        return {
            "error": ex.message
        }
    except Exception  as ex:
        return {
            "error":ex.message
        }

    return args