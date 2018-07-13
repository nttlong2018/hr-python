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