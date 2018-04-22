import argo
from argo import membership
login="~/login"
def authenticate(request):
    user=request.get_user()
    if user==None:
        _login=membership.validate_session(request.session.session_key)
        if _login==None:
            return False
        else:
            request.set_auth(user=dict(
                id=_login.user.userId,
                username=_login.user.username,
                isSysAdmin=_login.user.isSysAdmin
                ))
    if user.get("isSysAdmin")==None:
        _login = membership.validate_session(request.session.session_key)
        request.set_auth(user=dict(
            id=_login.user.userId,
            username=_login.user.username,
            isSysAdmin=_login.user.isSysAdmin
        ))
    user = request.get_user()
    return user.get("isSysAdmin")==True
DATABASE=dict(
    host="localhost",
    port=27017,
    user_="sys",
    password_="123456",
    name="hrm"
)