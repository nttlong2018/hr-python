import django
import quicky
import authorization
from qmongo import database
from django.contrib.auth.models import User
app=quicky.applications.get_app_by_file(__file__)
database=db=database.connect(app.settings.Database)
def get_app_res(key):
    language=django.utils.translation.get_language()
    return quicky.get_settings().LANGUAGE_ENGINE.get_language_item(language,app.name,"-",key,key)
def get_res(view,key):
    language=django.utils.translation.get_language()
    return quicky.get_settings().LANGUAGE_ENGINE.get_language_item(language,app.name,view,key,key)
def get_global_res(key):
    language=django.utils.translation.get_language()
    return quicky.get_settings().LANGUAGE_ENGINE.get_language_item(language,"-","-",key,key)

def get_list(args):
    from django.contrib.auth.models import User
    # from models import  test

    page_size=args["data"].get("pageSize",20)
    page_index = args["data"].get("pageIndex", 0)
    total_items=0

    if authorization.is_allow_read(args["privileges"]):
        users = User.objects.all()
        total_items=users.__len__()
        from_index=page_index*page_size
        to_index=(page_index+1)*page_size
        if to_index>users.__len__():
            to_index=users.__len__()
        total=users.__len__()
        items=users[from_index:to_index]


        return dict(
            pageSize=page_size,
            pageIndex=page_index,
            items=items,
            totalItems=total_items
        )

    else:
        return []
def create(args):
    data=args.get("data",{})
    if data.get("username",None)==None:
        return dict(
            error=dict(
                message=get_app_res("Please enter Username"),
                code="miss_param",
                field="username"
            )
        )
    if data.get("password",None)==None:
        return dict(
            error=dict(
                message=get_app_res("Please enter Password"),
                code="miss_param",
                field="password"
            )
        )

    user = User.objects.create_user(data.get("username",""),
                                    data.get("email",data["username"]),
                                    data.get("password",""))
    user.is_superuser=data.get("is_superuser",False)
    user.is_staff=data.get("is_staff",False)
    user.is_active=data.get("is_active",False)
    user.save()
    return user

def update(args):
    data=args["data"]
    user=User.objects.get(username=data["username"])
    user.is_superuser = data.get("is_superuser", False)
    user.is_staff = data.get("is_staff", False)
    user.is_active = data.get("is_active", False)
    user.save()
    return {}
def get_item(args):
    data=args["data"]
    user=None
    try:
        user=User.objects.get(username=data["username"])
    except Exception as ex:
        x=ex
        return None
    return user
