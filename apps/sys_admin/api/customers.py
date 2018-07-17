from .. models import sys_customers
from .. import query
import validator_params
from . import format_error
def get_list(args):
    """
    Get list of customer
    :param args:
    :return:
    """
    params=dict(
        page_size=0,
        page_index=50,
        search_text="",
        sort=dict(
            code=1
        )
    )
    params.update(args.get("data",{}))
    qr= query.qr_customers()
    qr.sort(params["sort"])
    ret=qr.get_page(params["page_size"],params["page_index"])
    return ret

def insert_item(args):
    """
    Update or insert customer
    :param args:
    :return:
    """
    validate_require_result=validator_params.require([
        "code",
        "name",
        "schema",
        "contact_info.email",
        "contact_info.address",
        "admin_user",
        "admin_user_password"
    ],args["data"])
    if validate_require_result.__len__()>0:
        return  dict(
            error=format_error.html_format(validate_require_result,args["request"],args["view"],'missing')
        )
    try:
        from django.contrib.auth.models import User
        user = User.objects.create_user(username=args["data"]["admin_user"],
                                        email=args["data"]["contact_info"]["email"],
                                        password=args["data"]["admin_user_password"],
                                        schema=args["data"]["schema"])
        user.is_staff = True
        user.is_admin = True
        user.save(schema=args["data"]["schema"])
    except Exception as ex:
        x=ex

    ret_insert=sys_customers().insert(args["data"])
    if ret_insert.get("error",None)!=None:
        sys_customers().qr.db.get_collection("{0}.auth_user".format(args["data"]["schema"])).drop()

        return dict(
            error=format_error.html_format(ret_insert["error"]['fields'], args["request"], args["view"], ret_insert['error']["code"])
        )



    return dict(
        result=ret_insert.data
    )
def get_item(args):
    item = sys_customers().find_one("code=={0}", args["data"]["code"])
    return item
def get_items(args):
    items = sys_customers().aggregate().project(
        code=1,
        name=1,
        _id=0
    ).get_list()
    import sys
    items.insert(0, {
        "code": "-",
        "name": "default"
    })
    from quicky import applications
    app=applications.get_app_by_file(__file__)
    items.append({
        "code":"system",
        "name":"system"
    })


    return items
def get_list_of_users_by_customer(args):
    from .. models import auth_user
    from .. models import sys_customers
    schema=None
    if args["data"]["customerCode"] == "-":
        import sys
        schema=sys.modules["settings"].MULTI_TENANCY_DEFAULT_SCHEMA
    elif args["data"]["customerCode"]== "system":
        from quicky import applications
        schema =applications.get_app_by_file(__file__).mdl.settings.DEFAULT_DB_SCHEMA
    else:
        customer_item=sys_customers().find_one("code=={0}",args["data"]["customerCode"])
        schema = customer_item["schema"]
        if customer_item == None:
            return {}

    data=auth_user()\
        .switch_schema(schema)\
        .aggregate()\
        .project(
        _id=0,
        username=1,
        first_name=1,
        last_name=1,
        is_active=1,
        is_superuser=1,
        is_staff=1,
        last_login=1,
        email=1,
        date_joined=1

    )\
        .get_page(
        page_size=args["data"].get("pageSize", 50),
        page_index=args["data"].get("pageIndex", 0)
    )
    return data
def sigin_as_user(args):
    schema = None
    code=args["data"]["code"]
    if code == "-":
        import sys
        schema = sys.modules["settings"].MULTI_TENANCY_DEFAULT_SCHEMA
    elif args["data"]["code"]== "system":
        from quicky import applications
        schema = applications.get_app_by_file(__file__).mdl.settings.DEFAULT_DB_SCHEMA
    else:
        customer_item=sys_customers().find_one("code=={0}",args["data"]["code"])
        schema = customer_item["schema"]
    from quicky import backends
    ret=backends.create_login_token(args["data"]["username"],schema)
    return dict(
        url=args["request"].get_abs_url()+"/"+schema+"?token="+ret
    )


def get_user_of_customer(args):
    data=args["data"]
    schema = None
    if data["customer"] == "-":
        import sys
        settings= sys.modules["settings"]
        schema =settings.MULTI_TENANCY_DEFAULT_SCHEMA
    else:
        cust_item = sys_customers().find_one("code=={0}", data["customer"])
        schema = cust_item["schema"]

    from ..models import auth_user

    ret_user=auth_user().switch_schema(schema).find_one("username=={0}",data["username"])
    # return ret_user

    from django.contrib.auth.models import User

    try:
        user=User.objects.get(username=data["username"], schema=schema)
        return  user
    except Exception as ex:
        return {}

