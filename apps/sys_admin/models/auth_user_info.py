from config import database, helpers, db_context
import datetime
_hasCreated=False

def auth_user_info():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "auth_user_info",
            "base",
            [["login_account"], ["email"]],
            login_account = helpers.create_field("text",True),
            username=helpers.create_field("text",True),
            display_name=helpers.create_field("text",True),
            role_code=helpers.create_field("text"),
            email=helpers.create_field("text"),
            is_system=helpers.create_field("bool"),
            never_expire=helpers.create_field("bool"),
            manlevel_from=helpers.create_field("numeric"),
            manlevel_to=helpers.create_field("numeric"),
            mobile=helpers.create_field("text"),
            description=helpers.create_field("text"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )

        _hasCreated=True
    ret = db_context.collection("auth_user_info")

    return ret