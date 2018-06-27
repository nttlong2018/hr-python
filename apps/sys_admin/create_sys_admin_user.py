from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
def create_sys_admin_user():
    # type: () -> object
    """
    Create sys admin user if ir was not existing. The sys admin user use to use for maintian system
    whenever you need. The username of Sys admin user in system is 'root' with default password is 'root'
    :return:
    """
    try:
        # User.objects.set_db_schema("sys")
        obj_users=User.objects
        user = obj_users.get(username="root",schema = "sys")
        user.is_staff = True
        user.is_admin = True
        user.save(schema="sys")
        # User.objects.set_db_schema(None)
    except ObjectDoesNotExist as ex:
        User.objects.set_db_schema("sys")
        user = User.objects.create_user(username='root',
                                        email='root@root.com',
                                        password='root',
                                        schema="sys")
        user.is_staff = True
        user.is_admin = True
        user.save(schema="sys")
        User.objects.set_db_schema(None)

