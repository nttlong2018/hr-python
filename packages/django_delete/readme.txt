Contributor: new version for multi tenancy supporting.
Example:
    try:
        User.objects.set_schema_name("sys")
        user = User.objects.get(username="root")
        user.is_staff = True
        user.is_admin = True
        user.save()
        User.objects.set_schema_name(None)
    except ObjectDoesNotExist as ex:
        User.objects.set_schema_name("sys")
        user = User.objects.create_user(username='root',
                                        email='root@root.com',
                                        password='root')
        user.is_staff = True
        user.is_admin = True
        user.save()
        User.objects.set_schema_name(None)