
login_url="../admin/login"
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
    user="root",
    password="123456",
    name="hrm"
)