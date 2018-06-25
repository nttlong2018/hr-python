
# -*- coding: utf-8 -*-
from quicky import applications
from qmongo import helpers,database
_hasCreated=False
def auth_user():
    global _hasCreated
    if not _hasCreated:
        helpers.define_model(
            "auth_user",
            [["username"]],
            username=helpers.create_field("text", True),
            first_name=helpers.create_field("text", True) , # link to 
            last_name=helpers.create_field("text", True),
            is_active=helpers.create_field("bool", True),
            email=helpers.create_field("text", True),
            is_superuser=helpers.create_field("bool", True),
            is_staff=helpers.create_field("bool", True),
	        last_login =helpers.create_field("date"),
            date_joined =helpers.create_field("date")
        )
        _hasCreated=True
    ret = applications.get_settings().database.collection("auth_user")

    return ret