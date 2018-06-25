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
        user = User.objects.get(username="root")
        user.is_staff = True
        user.is_admin = True
        user.save()
    except ObjectDoesNotExist as ex:
        user = User.objects.create_user(username='root',
                                        email='root@root.com',
                                        password='root')
        user.is_staff = True
        user.is_admin = True
        user.save()
        user.save()

