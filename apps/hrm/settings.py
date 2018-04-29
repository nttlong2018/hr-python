import argo
from argo import membership
login="~/login"
def authenticate(request):
    if not request.user.is_anonymous() and \
            (request.user.is_superuser or \
        request.user.is_staff) and \
        request.user.is_active:
        return True
    else:
        return False
DATABASE=dict(
    host="localhost",
    port=27017,
    user="rot",
    password="123456",
    name="hrm"
)