# -*- coding: utf-8 -*-
from config import database, helpers, db_context
import datetime
_hasCreated=False

def auth_user():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "auth_user",
            "base",
            [["login_account"]],
            login_account = helpers.create_field("text",True),
            username=helpers.create_field("text",True),
            display_name=helpers.create_field("text",True),
            first_name=helpers.create_field("text"),
            last_name=helpers.create_field("numeric"),
            is_active=helpers.create_field("text"),
            email=helpers.create_field("date"),
            is_superuser=helpers.create_field("text"),
            is_staff=helpers.create_field("date"),
            last_login=helpers.create_field("text"),
            password=helpers.create_field("text"),
            date_joined=helpers.create_field("text"),
            is_system=helpers.create_field("date"),
            never_expire=helpers.create_field("text"),
            manlevel_from=helpers.create_field("date"),
            manlevel_to=helpers.create_field("text"),
            mobile=helpers.create_field("text"),
            description=helpers.create_field("text")
        )

        def on_before_update(data):
            user = db_context.collection("auth_user").aggregate.match("username == @user_name",user_name=data['username'])
            if user['created_on'] == None:
                data["created_on"] = datetime.datetime.now()
                data["created_by"] = threading.current_thread().user.username

        helpers.events("HCSSYS_DataDomain").on_before_update(on_before_update)

        _hasCreated=True
    ret = db_context.collection("auth_user")

    return ret