import membership
def verify_user(request):
    login_info=membership.validate_session(request.session.session_key)
    if login_info==None:
        return False
    user = login_info.user;


    if not user.isSysAdmin:
        return user.isStaff
    else:
        return True