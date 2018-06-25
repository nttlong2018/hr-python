
# -*- coding: utf-8 -*-
from quicky import applications
from qmongo import helpers,database
from . import base
_hasCreated=False

def sys_customers():
    global _hasCreated
    if not _hasCreated:
        helpers.define_model(
            "sys_customers",
            [["code"]],
            
            code=helpers.create_field("text", True) , # link to  sys_multi_tenancy
            name=helpers.create_field("text", True),
            contact_info=dict(
                address=helpers.create_field("text", True),
                email=helpers.create_field("text", True),
                ),
            admin_user=helpers.create_field("text", True),# link to auth_user
        )
        _hasCreated=True
    ret = applications.get_settings().database.collection("sys_customers")
    ret.turn_never_use_schema_on()

    return ret