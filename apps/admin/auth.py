def verify_user(request):
    if request.get_auth()["user"]==None:
        return False
    else:
        if request.get_auth()["user"].get("is_sys_admin",False):
            return True
        else:
            return False