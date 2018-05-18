import models.hrm.categories
import quicky
login_url="../admin/login"
def authenticate(request):
    if not request.user.is_anonymous() and \
            (request.user.is_superuser or \
        request.user.is_staff) and \
        request.user.is_active:
        return True
    else:
        return False
Database=dict(
    host="localhost",
    port=27017,
    user="root",
    password="123456",
    name="hrm"
)
Database_=dict(
    host="172.16.7.63",
    port=27017,
    user="sys",
    password="123456",
    name="lv01_lms",
    tz_aware=quicky.get_django_settings_module().USE_TZ,
    timezone= "UTC"#quicky.get_django_settings_module().TIME_ZONE

)
models.hrm.categories.connect(Database)