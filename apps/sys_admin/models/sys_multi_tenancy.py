# -*- coding: utf-8 -*-
from quicky import applications
from qmongo import helpers,database
_hasCreated=False
def sys_multi_tenancy():
    # type: () -> database.collection
    """
    this model is the flection on 'sys_multi_tenancy' in mongodb.
    Just have 2 fields, no more...
    :return:
    """
    import sys
    settings = sys.modules["settings"]
    global _hasCreated
    if not _hasCreated:

        helpers.define_model(
            settings.MULTI_TENANCY_CONFIGURATION["collection"],
            [
                ["code"],
                ["schema"]
             ],
            code= helpers.create_field("text",True),
            schema= helpers.create_field("text",True),
        )
        _hasCreated=True
    ret = applications.get_settings().database.collection(settings.MULTI_TENANCY_CONFIGURATION["collection"])
    ret.turn_never_use_schema_on()
    return ret
