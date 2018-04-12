import membership
def verify_user(request):

    if request.get_auth()["user"]==None:
        return False
    if not request.get_auth()["user"].get("IsSysAdmin",False):
        user=membership.get_user(request.get_auth()["user"]["username"])
        request.get_auth()["user"].update({"IsSysAdmin":user.isSysAdmin})
        if not user.isSysAdmin:
            return False
        else:
            return True
    else:
         return  True