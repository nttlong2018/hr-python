
import django
import quicky
import authorization
from django.contrib.auth.models import User
app=quicky.applications.get_app_by_file(__file__)
database=quicky.db.database.connect(app.settings.Database)
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
    if authorization.is_allow_read(args["privileges"]):
        coll = database.collection("auth_user").aggregate()

        list=database.collection("auth_user").get_list()
        search_text=args["data"].get("searchText","")
        page_size=args["data"].get("pageSize",20)
        page_index=args["data"].get("pageIndex",0)

        if search_text!="":
            coll=coll.match("(contains(username,@search_text))or"
                                        "(contains(first_name,@search_text))or"
                                        "(contains(last_name,@search_text))",
                                        search_text=search_text)
        count=coll.copy()
        count.count("totalItems")
        totalItems=count.get_item().get("totalItems",0)

        coll.project(username=1,
                     first_name=1,
                     last_name=1,
                     is_active=1,
                     email=1,
                     is_supperuser=1,
                     is_staff=1,
                     last_logon=1,
                     date_joined=1,
                     displayName="concat(first_name,' ',last_name)",
                     description=1)
        coll=coll.skip(page_index*page_size).limit(page_size)
        items=coll.get_list()
        return dict(
            pageSize=page_size,
            pageIndex=page_index,
            items=items,
            total=1000
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
    # user=membership.get_user(args.get("username",""))
    # if user==None:
    #     return {
    #         "error":{
    #             "code":"user_not_found"
    #         }
    #     }
    # user.description = args.get("description", "")
    # user.displayName = args.get("displayName", "")
    # user.isSysAdmin=args.get("isSysAdmin", False)
    # user.isStaff=args.get("isStaff",False)
    # user.email = args.get("email,""")
    # membership.update_user(user)
    # membership.active_user(user.username)
    return {}