from config import database, helpers, db_context
import datetime
_hasCreated=False

def auth_user():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "auth_user",
            "base",
            [["username"]],
            username=helpers.create_field("text",True),
            first_name=helpers.create_field("text"),
            last_name=helpers.create_field("text"),
            is_active=helpers.create_field("bool"),
            email=helpers.create_field("text"),
            is_superuser=helpers.create_field("bool"),
            is_staff=helpers.create_field("bool"),
            last_login=helpers.create_field("date"),
            password=helpers.create_field("text"),
            date_joined=helpers.create_field("date")
        )

        _hasCreated=True
    ret = db_context.collection("auth_user")

    return ret